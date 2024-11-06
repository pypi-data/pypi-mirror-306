"""Test the CLI."""

import os
import pathlib
import subprocess
import sys

import pytest
from typer.testing import CliRunner

from .. import typer


@pytest.mark.parametrize("feature", ["univariate", "bivariate", "multivariate"])
def test_app(feature: str, tmp_path: pathlib.Path) -> None:
    """Test the app."""
    runner = CliRunner(mix_stderr=False)
    path = tmp_path / "file.csv"
    path.write_bytes(b"column\nvalue")
    result = runner.invoke(typer.app, [f"{feature}-analysis", os.fsdecode(path)])
    assert result.stderr == ""
    assert result.stdout == "\n"
    assert result.exit_code == 0


@pytest.mark.parametrize("feature", ["univariate", "bivariate", "multivariate"])
def test_subprocess(feature: str, tmp_path: pathlib.Path) -> None:
    """Test the app by running it in a subprocess."""
    path = tmp_path / "file.csv"
    path.write_bytes(b"column\nvalue")
    result = subprocess.run(
        [sys.executable, "-m", typer.__spec__.name, f"{feature}-analysis", os.fsdecode(path)],
        capture_output=True,
        check=True,
    )
    assert result.stderr == b""
    assert result.stdout == b"\n"
