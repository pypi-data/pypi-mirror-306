"""pytest conftest."""

import pytest


@pytest.fixture
def anyio_backend() -> str:
    """Configure the backend."""
    return "asyncio"
