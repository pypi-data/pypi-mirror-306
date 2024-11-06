"""Utils for fairground."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, assert_never

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle

if TYPE_CHECKING:
    from matplotlib.axes import Axes


def plot_selection_rate(df: pd.DataFrame, groupby: str | list[str], outcome_column: str) -> None:
    """Plot the selection rate for each group."""
    if isinstance(groupby, str):
        groupby_for_label: str | NonEmptyList[str] = groupby
    else:
        groupby_for_label_temp = NonEmptyList.create(groupby)
        if groupby_for_label_temp is None:
            message = "Invalid groupby"
            raise ValueError(message)
        groupby_for_label = groupby_for_label_temp
        # Combine multiple groupby columns with " - " separator
        df = df.copy()  # noqa: PD901
        df["combined_groups"] = df[groupby].astype(str).agg(" - ".join, axis=1)
        groupby = "combined_groups"

    selection_rate = df.groupby(groupby)[outcome_column].mean().reset_index()
    group_sizes = df.groupby(groupby).size()
    # https://github.com/pandas-dev/pandas-stubs/blob/f71224c6211ff436424be614ba47f494f64c4618/pandas-stubs/core/groupby/groupby.pyi#L239
    # return type depends on `as_index` for dataframe groupby
    assert isinstance(group_sizes, pd.Series)
    group_sizes = group_sizes.reset_index(name="count")

    selection_rate = selection_rate.merge(group_sizes, on=groupby).sort_values(
        by=[outcome_column, groupby],
        ascending=[False, True],
    )

    num_of_groups = len(df[groupby].unique())
    colors = sns.color_palette("husl", n_colors=num_of_groups)

    plt.figure(
        figsize=(10, max(4, len(df[groupby].unique()) * 0.5)),
    )  # Dynamic height based on groups

    ax = sns.barplot(
        data=selection_rate,
        x=outcome_column,
        y=groupby,
        hue=groupby,
        palette=colors,
        dodge=False,
        zorder=3,
        orient="h",
    )

    # Add labels with group sizes
    for i, (_, row) in enumerate(selection_rate.iterrows()):
        ax.text(
            row[outcome_column],
            i,
            f'(n={row["count"]:,})',
            ha="left",
            va="center",
            fontsize=9,
            zorder=4,
            bbox={
                "facecolor": "white",
                "alpha": 0,
                "edgecolor": "none",
                "pad": 2,
            },
        )

    plt.title(_plot_title("Total Selection Rate", groupby_for_label))
    plt.xlabel("Total Selection Rate (%)")
    plt.ylabel(_group_label(groupby_for_label))
    plt.grid(True, linestyle="--", linewidth=0.5, zorder=0)
    plt.tight_layout()


def plot_job_selection_rate(df: pd.DataFrame, groupby: str, job: str, outcome_column: str) -> None:
    """Plot the selection rate for each group for each job."""
    plot_data = df[[job, groupby, outcome_column]].copy()
    plot_data = (
        plot_data.groupby([job, groupby])[outcome_column]
        .mean()
        .reset_index()
        .rename(columns={outcome_column: "selection_rate"})
    )

    plot_data["selection_rate"] = plot_data["selection_rate"] * 100

    num_of_groups = len(df[groupby].unique())
    colors = sns.color_palette("husl", n_colors=num_of_groups)

    # Create faceted plot
    g = sns.FacetGrid(
        plot_data,
        col=job,
        col_wrap=2,
        height=4,
        aspect=1,
    )

    # Add bars to each subplot
    g.map_dataframe(
        sns.barplot,
        x=groupby,
        y="selection_rate",
        hue=groupby,
        palette=colors,
    )

    g.set_titles("Job: {col_name}")
    g.set_axis_labels(
        groupby.capitalize(),
        "Normalised Selection Rate (%)",
    )

    # Rotate x-axis labels
    for ax in g.axes.flat:
        for label in ax.get_xticklabels():
            label.set_rotation(45)
            label.set_ha("right")
        # Add grid to each subplot
        ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.3, zorder=0)

    # Adjust layout
    plt.suptitle(f"Selection Rate by {groupby} by {job}")
    plt.subplots_adjust(top=0.9, hspace=0.4)
    plt.tight_layout()


def parity_difference(
    df: pd.DataFrame,
    groupby: str,
    outcome_column: str,
) -> dict[str, pd.Series[float]]:
    """
    Calculate the parity difference.

    Calculate the parity difference for each unique value in a group (e.g.
    protected characteristics), using each unique value as a baseline.
    """
    selection_rates = df.groupby(groupby)[outcome_column].mean()
    return {
        baseline_group: selection_rates - values  # type:ignore[misc]
        for baseline_group, values in selection_rates.items()
    }


def plot_parity_difference(df: pd.DataFrame, groupby: str, outcome_column: str) -> None:
    """Plot the parity difference for each group."""
    parity_diffs = parity_difference(df, groupby, outcome_column)
    groups = list(parity_diffs.keys())
    num_of_groups = len(groups)
    assert num_of_groups > 1

    # Calculate group sizes
    group_sizes = df[groupby].value_counts().to_dict()

    fig, axes = plt.subplots(num_of_groups, 1, figsize=(10, 3 * num_of_groups), sharex=True)
    title = f"Parity Difference Analysis by {groupby}"
    fig.suptitle(title, fontsize=16, y=0.98)

    colors = sns.color_palette("husl", n_colors=num_of_groups)

    for ax, (baseline_group, parity_diff) in zip(axes, parity_diffs.items(), strict=False):
        plot_data = pd.DataFrame(
            {
                "Group": parity_diff.index,
                "Parity Difference": parity_diff.to_numpy(),
            },
        )
        # Create horizontal bars
        sns.barplot(
            data=plot_data,
            y="Group",
            x="Parity Difference",
            hue="Group",
            legend=False,
            ax=ax,
            palette=colors,
            orient="h",
            alpha=0.8,
        )

        # Add group size labels
        for idx, (group, value) in enumerate(parity_diff.items()):
            size_label = f"n={group_sizes[group]:,}"
            if value >= 0:
                x_pos = value  # Place label at end of positive bar
                ha = "left"
                x_offset = 0.01  # Small offset to not overlap with bar
            else:
                x_pos = value  # Place label at end of negative bar
                ha = "right"
                x_offset = -0.01

            ax.text(
                x=x_pos + x_offset * (ax.get_xlim()[1] - ax.get_xlim()[0]),  # Place at start of bar
                y=idx,
                s=size_label,
                va="center",
                ha=ha,
                fontsize=9,
                color="black",
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.7, "pad": 0.5},
            )

        # Customize plot
        ax.axvline(x=0, color="red", linestyle="--", linewidth=0.5)
        ax.set_title(f"Baseline: {baseline_group}", pad=10)
        ax.set_xlabel("Parity Difference" if ax == axes[-1] else "")
        ax.set_ylabel(groupby)

        # Set limits with padding
        max_abs_val = max(abs(parity_diff.min()), abs(parity_diff.max()))
        ax.set_xlim(
            min(-max_abs_val * 1.2, parity_diff.min() * 1.2),
            max(max_abs_val * 1.2, parity_diff.max() * 1.2),
        )

    plt.tight_layout()


def plot_parity_difference_scatter(
    df: pd.DataFrame,
    groupby: str | list[str],
    outcome_column: str,
) -> None:
    """Plot the parity difference in a scatterplot heatmap."""
    if isinstance(groupby, str):
        groupby_for_label: str | NonEmptyList[str] = groupby
    else:
        # Combine multiple groupby columns
        groupby_for_label_temp = NonEmptyList.create(groupby)
        if groupby_for_label_temp is None:
            message = "Invalid groupby"
            raise ValueError(message)
        groupby_for_label = groupby_for_label_temp
        df = df.copy()  # noqa: PD901
        df["combined_groups"] = df[groupby].astype(str).agg(" - ".join, axis=1)
        groupby = "combined_groups"

    parity_diffs = parity_difference(df, groupby, outcome_column)

    # Convert to matrix format
    plot_df = pd.DataFrame(
        {
            "baseline": baseline_key,
            "comparison": comparison,
            "parity_diff": baseline[comparison],
        }
        for baseline_key, baseline in parity_diffs.items()
        for comparison in parity_diffs
    )

    g = sns.relplot(
        data=plot_df,
        x="baseline",
        y="comparison",
        hue="parity_diff",
        size="parity_diff",
        palette="vlag",
        hue_norm=(-1, 1),
        edgecolor=".7",
        height=10,
        aspect=0.9,
        sizes=(100, 500),
        size_norm=(-0.2, 0.8),
    )

    g.ax.grid(True, linestyle="--", alpha=0.7)

    g.set(xlabel="Baseline Group", ylabel="Comparison Group", aspect="equal")
    g.ax.margins(0.02)

    for label in g.ax.get_xticklabels():
        label.set_rotation(90)

    plt.suptitle(_plot_title("Parity Difference Matrix", groupby_for_label))


def disparate_impact_ratio(
    df: pd.DataFrame,
    groupby: str | list[str],
    outcome_column: str,
) -> pd.Series[float]:
    """Calculate the disparate impact ratio for different groups."""
    selection_rates: pd.Series[float] = df.groupby(groupby)[outcome_column].mean()
    max_rate = selection_rates.max()
    impact_ratios = selection_rates / max_rate
    return impact_ratios.sort_values(ascending=True)


def _plot_title(x: str, groupby: str | NonEmptyList[str]) -> str:
    match groupby:
        case str():
            return f"{x} by {groupby}"
        case NonEmptyList([first], second):
            return f"{x} by {first} and {second}"
        case NonEmptyList(rest, last):
            return f"{x} by {', '.join(rest)}, and {last}"
        case _ as unreachable:
            assert_never(unreachable)


def _group_label(groupby: str | NonEmptyList[str]) -> str:
    match groupby:
        case str():
            return groupby
        case NonEmptyList(rest, last):
            return f"{', '.join(rest)}, and {last}"
        case _ as unreachable:
            assert_never(unreachable)


@dataclass(frozen=True)
class NonEmptyList[T]:
    """A list that is guarantee to have an item."""

    rest: list[T]
    last: T

    @classmethod
    def create(cls, items: list[T]) -> Self | None:
        """Optionally return a NonEmptyList from a regular list."""
        if not items:
            return None
        *rest, last = items
        return cls(rest=rest, last=last)


def plot_selection_rate_deviation_with_disparate_impact_ratio_value(
    df: pd.DataFrame,
    groupby: str | list[str],
    outcome_column: str,
) -> None:
    """Plot the disparate impact ratio for different groups."""
    if isinstance(groupby, str):
        group_sizes = df.groupby(groupby).size()
        selection_rates = df.groupby(groupby)[outcome_column].mean()
        impact_ratios = disparate_impact_ratio(df, groupby, outcome_column)
        selection_rates = selection_rates[impact_ratios.index]
        group_sizes = group_sizes[impact_ratios.index]

        impact_df = pd.DataFrame(
            {
                "group": impact_ratios.index,
                "impact_ratio": impact_ratios.to_numpy(),
                "selection_rate": selection_rates.to_numpy(),
                "group_size": group_sizes.to_numpy(),
            },
        )
        groupby_for_label: str | NonEmptyList[str] = groupby

    else:
        groupby_for_label_temp = NonEmptyList.create(groupby)
        if groupby_for_label_temp is None:
            message = "Invalid groupby"
            raise ValueError(message)
        groupby_for_label = groupby_for_label_temp

        group_sizes = df.groupby(groupby).size()
        selection_rates = df.groupby(groupby)[outcome_column].mean()
        impact_ratios = disparate_impact_ratio(df, groupby, outcome_column)
        selection_rates = selection_rates[impact_ratios.index]
        group_sizes = group_sizes[impact_ratios.index]

        impact_df = pd.DataFrame(
            {
                "group": impact_ratios.index.map(" - ".join),
                "impact_ratio": impact_ratios.to_numpy(),
                "selection_rate": selection_rates.to_numpy(),
                "group_size": group_sizes.to_numpy(),
            },
        )

    impact_df["selection_rate_percentage"] = impact_df["selection_rate"] * 100
    num_of_groups = len(impact_df)
    equal_treatment_percentage = 100 / num_of_groups
    impact_df["deviation"] = impact_df["selection_rate_percentage"] - equal_treatment_percentage

    # Sort by percentage
    impact_df = impact_df.sort_values(
        ["selection_rate_percentage", "group"],
        ascending=[False, True],
    )
    colors = sns.color_palette("husl", n_colors=num_of_groups)

    fig, ax = plt.subplots(figsize=(14, max(8, num_of_groups * 0.5)))

    bars = sns.barplot(
        data=impact_df,
        y="group",
        x="deviation",
        hue="group",
        palette=colors,
        ax=ax,
        zorder=3,
        orient="h",
        legend=False,
    )

    for patch in bars.patches:
        assert isinstance(patch, Rectangle)
        patch.set_x(patch.get_x() + equal_treatment_percentage)

    # Calculate DIR threshold (80% of max)
    dir_threshold = (impact_df["selection_rate"].max()) * 0.8 * 100
    # Calculate axis limits, do it here instead of later to adjust dynamic paddings for labels
    min_rate = min(equal_treatment_percentage, impact_df["selection_rate_percentage"].min())
    max_rate = max(
        equal_treatment_percentage,
        impact_df["selection_rate_percentage"].max(),
        dir_threshold,
    )
    total_range = max_rate - min_rate

    _add_bar_labels(impact_df, equal_treatment_percentage, ax, total_range * 0.005)

    # Add vertical lines
    ax.axvline(
        equal_treatment_percentage,
        color="red",
        linestyle="--",
        label="Equal Treatment Percentage",
        zorder=2,
    )
    ax.axvline(dir_threshold, color="blue", linestyle="--", label="DIR Threshold (80%)", zorder=2)

    main_title = _plot_title("Selection Rate Deviation", groupby_for_label)
    fig.suptitle(main_title, fontsize=16, y=0.98)

    # Set labels and grid
    ax.set_xlabel("Selection Rate (%)")
    ax.set_ylabel(_group_label(groupby_for_label))
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.3, zorder=0)

    # Set axis limits
    plot_padding = total_range * 0.15
    ax.set_xlim(min_rate - plot_padding, max_rate + plot_padding)

    # Add legend
    ax.legend(title="Thresholds", fontsize="x-small", title_fontsize="x-small")

    plt.tight_layout()


def _add_bar_labels(
    impact_df: pd.DataFrame,
    equal_treatment_percentage: float,
    ax: Axes,
    dynamic_padding: float,
) -> None:
    for idx, row in enumerate(impact_df.itertuples()):
        assert isinstance(row.deviation, float)
        bar_end = equal_treatment_percentage + row.deviation
        label = f"(n={row.group_size:,}) (DIR: {row.impact_ratio:.2f})"
        if row.deviation >= 0:
            x_pos = bar_end
            ha = "left"
            padding = dynamic_padding
        else:
            x_pos = bar_end
            ha = "right"
            padding = -dynamic_padding
        ax.text(
            x_pos + padding,
            idx,
            label,
            va="center",
            ha=ha,
            fontsize=8,
        )
