"""Test the utils."""

import importlib.resources

import pandas as pd
import pytest

from ..utils import (
    plot_job_selection_rate,
    plot_parity_difference,
    plot_parity_difference_scatter,
    plot_selection_rate,
    plot_selection_rate_deviation_with_disparate_impact_ratio_value,
)
from .image_comparison import image_comparison


def _shuffle(df: pd.DataFrame) -> pd.DataFrame:
    return df.sample(frac=1).reset_index(drop=True)


def _get_test_df(input_file: str) -> pd.DataFrame:
    with importlib.resources.as_file(importlib.resources.files() / input_file) as f:
        return _shuffle(pd.read_csv(f))


@image_comparison
def test_parity_difference() -> None:
    """Test the plot of parity difference."""
    plot_parity_difference(_get_test_df(input_file="excel2csv_v2.csv"), "Gender", "Outcome")


@image_comparison
def test_selection_rate() -> None:
    """Test the plot of selection rate."""
    plot_selection_rate(_get_test_df(input_file="excel2csv_v2.csv"), "Gender", "Outcome")


def test_selection_rate_empty_list() -> None:
    """Test the plot of selection rate."""
    input_df = _get_test_df(input_file="excel2csv_v2.csv")
    with pytest.raises(ValueError, match=r"Invalid groupby"):
        plot_selection_rate(input_df, [], "Outcome")


@image_comparison
def test_selection_rate_multiple() -> None:
    """Test the plot of selection rate."""
    plot_selection_rate(
        _get_test_df(input_file="excel2csv_v2.csv"),
        ["Gender", "Race", "Age"],
        "Outcome",
    )


@image_comparison
def test_parity_difference_more_than_3() -> None:
    """Test the plot of selection rate with more than 3 unique values in a category."""
    plot_parity_difference(
        _get_test_df(input_file="excel2csv_v2_more_than_3.csv"),
        "Race",
        "Outcome",
    )


@image_comparison
def test_parity_difference_more_than_3_scatter_multiple() -> None:
    """Test the plot of selection rate with more than 3 unique values in a category."""
    plot_parity_difference_scatter(
        _get_test_df(input_file="excel2csv_v2_more_than_3.csv"),
        ["Race", "Gender"],
        "Outcome",
    )


def test_parity_difference_empty_list() -> None:
    """Test the plot of selection rate with more than 3 unique values in a category."""
    with pytest.raises(ValueError, match=r"Invalid groupby"):
        plot_parity_difference_scatter(
            _get_test_df(input_file="excel2csv_v2_more_than_3.csv"),
            [],
            "Outcome",
        )


@image_comparison
def test_parity_difference_more_than_3_scatter() -> None:
    """Test the plot of selection rate with more than 3 unique values in a category."""
    plot_parity_difference_scatter(
        _get_test_df(input_file="excel2csv_v2_more_than_3.csv"),
        "Race",
        "Outcome",
    )


@image_comparison
def test_disparate_impact_ratio() -> None:
    """Test the plot of disparate impact ratio."""
    plot_selection_rate_deviation_with_disparate_impact_ratio_value(
        _get_test_df(input_file="excel2csv_v2.csv"),
        "Race",
        "Outcome",
    )


@image_comparison
def test_disparate_impact_ratio_multi_combinations() -> None:
    """Test the plot of disparate impact ratio for multiple combinations."""
    plot_selection_rate_deviation_with_disparate_impact_ratio_value(
        _get_test_df(input_file="excel2csv_v2.csv"),
        ["Race", "Age", "Gender"],
        "Outcome",
    )


def test_disparate_impact_ratio_empty_list() -> None:
    """Test the plot of disparate impact ratio for multiple combinations."""
    input_df = _get_test_df(input_file="excel2csv_v2.csv")
    with pytest.raises(ValueError, match=r"Invalid groupby"):
        plot_selection_rate_deviation_with_disparate_impact_ratio_value(input_df, [], "Outcome")


@image_comparison
def test_job_selection_rate() -> None:
    """Test the plot of selection rate."""
    plot_job_selection_rate(
        _get_test_df(input_file="excel2csv_v4.csv"),
        "Gender",
        "Job Role",
        "Outcome",
    )
