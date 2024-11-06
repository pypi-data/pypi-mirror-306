"""Typer for intersectional."""

import sys
from typing import Any

import pandas as pd
import typer

from .intersectional import bivariate, multivariate, univariate

app = typer.Typer()


@app.command("univariate-analysis")
def n_equals_one(file: str) -> None:
    """Perform univariate analysis."""
    uni_df = pd.read_csv(file)
    result = univariate(uni_df)
    typer.echo(result)


@app.command("bivariate-analysis")
def n_equals_two(file: str) -> None:
    """Perform bivariate analysis."""
    bi_df = pd.read_csv(file)
    result = bivariate(bi_df)
    typer.echo(result)


@app.command("multivariate-analysis")
def n_equals_three(file: str) -> None:
    """Perform multivariate analysis."""
    multi_df = pd.read_csv(file)
    result = multivariate(multi_df)
    typer.echo(result)


def main() -> Any:
    """Call app()."""
    return app()


if __name__ == "__main__":
    sys.exit(main())
