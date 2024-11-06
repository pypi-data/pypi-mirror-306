"""Test permutation."""

import hashlib
import importlib
import io
import textwrap

import numpy as np
import pandas as pd

from ..permutations import (
    family_wise_permutation_analysis,
    plot_family_wise_permutation_analysis,
    simple_permutation_analysis,
)
from .image_comparison import image_comparison

type OneDimFloat64 = np.ndarray[tuple[int], np.dtype[np.float64]]


def _rng(v: str) -> np.random.Generator:
    return np.random.default_rng(
        int.from_bytes(hashlib.sha512(v.encode()).digest(), "big"),
    )


def _get_test_df(input_file: str) -> pd.DataFrame:
    with importlib.resources.as_file(importlib.resources.files() / input_file) as f:
        return pd.read_csv(f)


def _read_csv_dedent(v: str) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(textwrap.dedent(v)))


def test_simple_permutation_analysis_single() -> None:
    """Test the output of simple permutation analysis."""
    input_df = _read_csv_dedent(
        """\
        Candidate,Outcome,Race,Gender,Age,Job Role
        Barbara Anderson,0,White,Female,Younger,HR Business Partner
        Betty Taylor,0,White,Female,Younger,HR Business Partner
        Alfonse Cotton,0,Black,Male,Older,HR Business Partner
        Kenji Liu,0,Asian,Male,Younger,HR Business Partner
        Kenji Zhang,1,Asian,Male,Younger,Senior Finance Business Partner
        Quang Kang,0,Asian,Male,Younger,Senior Finance Business Partner
        Chen Choi,0,Asian,Male,Younger,Retail Store Manager
        Deshaun Blanco,0,Black,Male,Older,Retail Store Manager
        Rebecca Wilson,0,White,Female,Younger,Retail Store Manager
        Tesfaye Parker,1,Black,Male,Older,Retail Store Manager
        """,
    )
    expected_df = _read_csv_dedent(
        """\
        Race,Gender,Race2,Gender2,naive_pvalue,observed_diff,pair_name
        Asian,Male,Black,Male,1.0,-0.08333333333333331,T1: Asian-Male vs Black-Male
        Asian,Male,White,Female,1.0,0.25,T2: Asian-Male vs White-Female
        Black,Male,White,Female,1.0,0.3333333333333333,T3: Black-Male vs White-Female
        """,
    )
    pd.testing.assert_frame_equal(
        simple_permutation_analysis(input_df, ["Race", "Gender"], "Outcome"),
        expected_df,
    )


@image_comparison(tolerance=0.1)
def test_plot_family_wise_permutation_analysis() -> None:
    """Test the plot of disparate impact ratio for multiple combinations."""
    input_df = _get_test_df(input_file="excel2csv_v4.csv")
    result_df, dist = family_wise_permutation_analysis(
        input_df,
        ["Gender", "Race", "Age"],
        "Outcome",
        seed=_rng("plot family-wise permutation analysis"),
    )
    plot_family_wise_permutation_analysis(
        result_df,
    )
