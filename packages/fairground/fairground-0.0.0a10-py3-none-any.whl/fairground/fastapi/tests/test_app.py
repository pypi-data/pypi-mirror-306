"""Example test."""

from __future__ import annotations

import contextlib
import io
import signal
import sys
from typing import TYPE_CHECKING

import anyio.abc
import httpx
import pytest
import stamina
from asgi_lifespan import LifespanManager

from .. import app

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from anyio.abc import TaskStatus


@contextlib.asynccontextmanager
async def _client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with (
        LifespanManager(app.create_app()) as manager,
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=manager.app),
            base_url="http://testserver",
        ) as client,
    ):
        yield client


@pytest.mark.anyio
async def test_data() -> None:
    """Test the /data endpoint."""
    async with _client() as client:
        response = await client.get("http://testserver/data")
        response.raise_for_status()
        assert response.json() == [
            {
                "dob": "1980-01-01",
                "firstName": "John",
                "lastName": "Doe",
                "progress": 50,
                "status": "Active",
                "visits": 10,
            },
            {
                "dob": "1985-02-15",
                "firstName": "Jane",
                "lastName": "Smith",
                "progress": 80,
                "status": "Inactive",
                "visits": 5,
            },
            {
                "dob": "1970-03-20",
                "firstName": "Bob",
                "lastName": "Johnson",
                "progress": 75,
                "status": "Active",
                "visits": 20,
            },
            {
                "dob": "1982-04-25",
                "firstName": "Alice",
                "lastName": "Williams",
                "progress": 60,
                "status": "Active",
                "visits": 15,
            },
            {
                "dob": "1988-05-30",
                "firstName": "Charlie",
                "lastName": "Brown",
                "progress": 40,
                "status": "Inactive",
                "visits": 8,
            },
            {
                "dob": "1988-05-30",
                "firstName": "Eva",
                "lastName": "Davis",
                "progress": 90,
                "status": "Active",
                "visits": 12,
            },
            {
                "dob": "1988-05-30",
                "firstName": "Frank",
                "lastName": "Miller",
                "progress": 85,
                "status": "Active",
                "visits": 25,
            },
        ]


@pytest.mark.anyio
async def test_process_empty() -> None:
    """Test we can send an empty list of Person."""
    async with _client() as client:
        response = await client.post("http://testserver/process", json=[])
        response.raise_for_status()
        assert response.json() == []


@pytest.mark.anyio
async def test_process_one() -> None:
    """Test we can process one Person."""
    async with _client() as client:
        response = await client.post(
            "http://testserver/process",
            json=[
                {
                    "dob": "1988-05-30",
                    "firstName": "Frank",
                    "lastName": "Miller",
                    "progress": 85,
                    "status": "Active",
                    "visits": 25,
                },
            ],
        )
        response.raise_for_status()
        assert response.json() == [
            {
                "dob": "<ANONYMIZED DATE OF BIRTH>",
                "firstName": "<ANONYMIZED PERSON>",
                "lastName": "<ANONYMIZED PERSON>",
                "progress": 85,
                "status": "Active",
                "visits": 25,
            },
        ]


@pytest.mark.parametrize("feature", ["univariate", "bivariate", "multivariate"])
@pytest.mark.anyio
async def test_analyse_one(feature: str) -> None:
    """Test we can process one Person."""
    async with _client() as client:
        response = await client.post(
            f"http://testserver/analyse_as_{feature}",
            files={"file": io.BytesIO(b"column\nvalue")},
        )
        response.raise_for_status()
        assert response.json() == {"result": ""}


@pytest.mark.anyio
async def test_main() -> None:
    """Test the __name__ == __main__."""

    @stamina.retry(on=httpx.ConnectError, attempts=10)
    async def post(client: httpx.AsyncClient) -> httpx.Response:
        return await client.post("http://localhost:8000/process", json=[])

    async def run(
        *,
        task_status: TaskStatus[anyio.abc.Process] = anyio.TASK_STATUS_IGNORED,
    ) -> None:
        async with await anyio.open_process(
            [sys.executable, "-m", app.__spec__.name],
            stdin=None,
            stdout=None,
            stderr=None,
        ) as process:
            task_status.started(process)
            await process.wait()
            assert process.returncode == 0

    async with httpx.AsyncClient() as client, anyio.create_task_group() as tg:
        process = await tg.start(run)
        response = await post(client)
        response.raise_for_status()
        assert response.json() == []
        process.send_signal(signal.SIGINT)
