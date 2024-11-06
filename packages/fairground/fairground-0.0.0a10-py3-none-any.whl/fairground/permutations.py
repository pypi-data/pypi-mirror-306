"""Permutation testing analysis for fairground."""

from collections.abc import Iterable
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import fisher_exact, permutation_test

type OneDimFloat64 = np.ndarray[tuple[int], np.dtype[np.float64]]


def simple_permutation_analysis(
    df: pd.DataFrame,
    groupby: list[str],
    outcome_column: str,
    n_permutations: int = 10000,
) -> pd.DataFrame:
    """
    Run simple permutation analysis.

    Args:
        df: Input DataFrame
        groupby: List of characteristics to analyze
        outcome_column: Name of the outcome column
        n_permutations: Number of permutations to run

    Returns:
        Results DataFrame
    """
    # Group the data
    groups = list(df.groupby(groupby))
    group_pairs = list(combinations(range(len(groups)), 2))

    def _diff_in_means(
        x: OneDimFloat64,
        y: OneDimFloat64,
    ) -> np.float64:
        return np.mean(x) - np.mean(y)

    def _kebab(v: Iterable[object]) -> str:
        return "-".join(str(x) for x in v)

    def _process_pairs(pair_id: int, i: int, j: int) -> dict[str, object]:
        group1 = groups[i][1][outcome_column].to_numpy()
        group2 = groups[j][1][outcome_column].to_numpy()

        res = permutation_test(
            (group1, group2),
            # https://github.com/jorenham/scipy-stubs/pull/143
            statistic=_diff_in_means,  # type: ignore[arg-type]
            n_resamples=n_permutations,
            alternative="two-sided",
        )

        return {
            **dict(zip(groupby, groups[i][0], strict=True)),
            **{f"{col}2": val for col, val in zip(groupby, groups[j][0], strict=True)},
            "naive_pvalue": res.pvalue,
            "observed_diff": res.statistic,
            "pair_name": f"T{pair_id}: {_kebab(groups[i][0])} vs {_kebab(groups[j][0])}",
        }

    return pd.DataFrame(
        _process_pairs(pair_id, i, j) for pair_id, (i, j) in enumerate(group_pairs, start=1)
    ).sort_values("naive_pvalue")


def family_wise_permutation_analysis(
    df: pd.DataFrame,
    groupby: list[str],
    outcome_column: str,
    n_permutations: int = 10000,
    *,
    seed: np.random.Generator,
) -> tuple[pd.DataFrame, OneDimFloat64]:
    """
    Conduct a family-wise permutation analysis using Fisher's exact test.

    Args:
        df: Input DataFrame containing the data
        groupby: Column name(s) to group by in the format of list of strings.
        outcome_column: Name of the column containing the outcome variable
        n_permutations: Number of permutations to run

    Returns:
        DataFrame containing the results with adjusted p-values
    """
    # Group the data
    groups = list(df.groupby(groupby))
    group_pairs = list(combinations(range(len(groups)), 2))

    # Calculate observed p-values using Fisher's exact test
    observed_p = np.array(
        [
            fisher_exact(
                np.asarray(
                    [
                        [
                            sum(groups[i][1][outcome_column]),
                            len(groups[i][1]) - sum(groups[i][1][outcome_column]),
                        ],
                        [
                            sum(groups[j][1][outcome_column]),
                            len(groups[j][1]) - sum(groups[j][1][outcome_column]),
                        ],
                    ],
                    dtype=np.int64,
                ),
            ).pvalue
            for i, j in group_pairs
        ],
    )

    # Initialise array for min p-values
    min_p_dist = np.zeros(n_permutations)

    # Perform permutations
    group_data = [group[1][outcome_column].to_numpy() for group in groups]
    group_sizes = [len(g) for g in group_data]

    for perm in range(n_permutations):
        # Randomly permute all data
        all_data = np.concatenate(group_data)
        seed.shuffle(all_data)

        # Split permuted data into groups
        perm_groups = np.split(all_data, np.cumsum(group_sizes)[:-1])

        # Calculate p-values for permuted data
        perm_p = np.array(
            [
                fisher_exact(
                    np.asarray(
                        [
                            [sum(perm_groups[i]), len(perm_groups[i]) - sum(perm_groups[i])],
                            [sum(perm_groups[j]), len(perm_groups[j]) - sum(perm_groups[j])],
                        ],
                        dtype=np.int64,
                    ),
                ).pvalue
                for i, j in group_pairs
            ],
        )

        min_p_dist[perm] = np.min(perm_p)

    # Calculate adjusted p-values
    adjusted_p = np.mean(min_p_dist[:, np.newaxis] <= observed_p, axis=0)

    def _kebab(v: Iterable[object]) -> str:
        return "-".join(str(x) for x in v)

    return pd.DataFrame(
        {
            **dict(zip(groupby, groups[i][0], strict=True)),
            **{f"{col}2": val for col, val in zip(groupby, groups[j][0], strict=True)},
            "observed_p": obs_p,
            "adjusted_p": adj_p,
            "observed_diff": np.mean(group_data[i]) - np.mean(group_data[j]),
            "pair_name": f"T{pair_id}: {_kebab(groups[i][0])} vs {_kebab(groups[j][0])}",
        }
        for pair_id, ((i, j), obs_p, adj_p) in enumerate(
            zip(group_pairs, observed_p, adjusted_p, strict=True),
            start=1,
        )
    ).sort_values("observed_p"), min_p_dist


def plot_family_wise_permutation_analysis(
    df: pd.DataFrame,
    p_threshold: float = 0.1,
) -> None:
    """Plot permutation testing analysis."""
    observed = pd.DataFrame(
        {
            "p_value": df["observed_p"],
            "type": "Observed P",
            "pair_name": df["pair_name"],
            "significant": df["observed_p"] < p_threshold,
        },
    )

    adjusted = pd.DataFrame(
        {
            "p_value": df["adjusted_p"],
            "type": "Adjusted P",
            "pair_name": df["pair_name"],
            "significant": df["adjusted_p"] < p_threshold,
        },
    )

    plot_data = pd.concat([observed, adjusted])

    plt.figure(figsize=(15, 6))

    # Plot significant points
    sns.swarmplot(
        data=plot_data[plot_data["significant"]],
        x="p_value",
        y="type",
        size=5,
        color="#d62728",
    )
    sns.swarmplot(
        data=plot_data[~plot_data["significant"]],
        x="p_value",
        y="type",
        size=5,
    )

    plt.title("Distribution of Observed and Adjusted P-values", pad=20)
    plt.xlabel("P-value")
    plt.ylabel("")

    # Add gridlines
    plt.grid(True, axis="x", linestyle="--", alpha=0.7)

    # Set x-axis limits from 0 to 1
    plt.xlim(-0.05, 1.05)

    # Add a vertical line at p=0.05 for reference
    plt.axvline(x=p_threshold, color="red", linestyle="--", alpha=0.5, label=f"p={p_threshold}")

    # Add legend
    plt.legend()

    # Adjust layout
    plt.tight_layout()
