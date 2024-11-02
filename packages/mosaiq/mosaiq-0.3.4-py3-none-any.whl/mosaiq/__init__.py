import altair as alt
import pandas as pd
import numpy as np
from narwhals.typing import FrameT
import narwhals as nw

@nw.narwhalify
def _pandas(df):
    return df.to_pandas()

def mosaiq(dataframe: FrameT, field1: str, field2: str, max_bins=6, color="category20", na_top_label="NA_TOP"):
    """
    Create a mosaic plot using Altair, automatically handling numeric fields
    and consolidating low-frequency categories into a "NA_TOP" category.
    Uses a single color scheme for both numeric and categorical bins.

    Args:
        dataframe: pandas DataFrame containing the data.
        field1: str, first field (categorical or numeric, shown on x-axis).
        field2: str, second field (categorical or numeric, shown as blocks).
        max_bins: int, maximum number of bins or categories to show.
        color: str, color scheme to apply to all bins.
        na_top_label: str, label for consolidated NA bin.

    Returns:
        altair.Chart: A compound chart containing the mosaic plot.
    """
    df = _pandas(dataframe)


    # Process field1
    df[f"{field1}_binned"] = _create_bins(df[field1], max_bins)
    field1_name = f"{field1}_binned" if pd.api.types.is_numeric_dtype(df[field1]) else field1

    # Process field2
    df[f"{field2}_binned"] = _create_bins(df[field2], max_bins)
    field2_name = f"{field2}_binned" if pd.api.types.is_numeric_dtype(df[field2]) else field2

    base = (
        alt.Chart(df)
        .transform_aggregate(
            count_="count()",
            groupby=[field1_name, field2_name]
        )
        .transform_stack(
            stack="count_",
            as_=["stack_count_1", "stack_count_2"],
            offset="normalize",
            sort=[alt.SortField(field1_name, "ascending")],
            groupby=[],
        )
        .transform_window(
            x="min(stack_count_1)",
            x2="max(stack_count_2)",
            rank_field2="dense_rank()",
            distinct_field2=f"distinct({field2_name})",
            groupby=[field1_name],
            frame=[None, None],
            sort=[alt.SortField(field2_name, "ascending")],
        )
        .transform_window(
            rank_field1="dense_rank()",
            frame=[None, None],
            sort=[alt.SortField(field1_name, "ascending")],
        )
        .transform_stack(
            stack="count_",
            groupby=[field1_name],
            as_=["y", "y2"],
            offset="normalize",
            sort=[alt.SortField(field2_name, "ascending")],
        )
        .transform_calculate(
            ny="datum.y + (datum.rank_field2 - 1) * datum.distinct_field2 * 0.01 / 3",
            ny2="datum.y2 + (datum.rank_field2 - 1) * datum.distinct_field2 * 0.01 / 3",
            nx="datum.x + (datum.rank_field1 - 1) * 0.01",
            nx2="datum.x2 + (datum.rank_field1 - 1) * 0.01",
            xc="(datum.nx+datum.nx2)/2",
            yc="(datum.ny+datum.ny2)/2",
        )
    )

    # Create the rectangles
    rect = base.mark_rect().encode(
        x=alt.X("nx:Q", axis=None),
        x2="nx2",
        y="ny:Q",
        y2="ny2",
        color=alt.Color(f"{field1_name}:N", legend=None, scale=alt.Scale(scheme=color)),
        opacity=alt.Opacity(f"{field2_name}:O", legend=None),
        tooltip=[
            alt.Tooltip(field1_name, title=field1),
            alt.Tooltip(field2_name, title=field2),
            alt.Tooltip("count_:Q", title="Count")
        ],
    )

    # Add text labels for field2 values
    text = base.mark_text(baseline="middle", size=10).encode(
        x=alt.X("xc:Q", axis=None),
        y=alt.Y("yc:Q", title=field2),
        text=f"{field2_name}:N"
    )

    # Create the mosaic plot
    mosaic = rect + text

    # Add labels for field1
    field1_labels = base.mark_text(baseline="middle", align="center", angle=0).encode(
        x=alt.X(
            "min(xc):Q",
            axis=alt.Axis(title=field1, orient="top"),
        ),
        color=alt.Color(field1_name, legend=None, scale=alt.Scale(scheme=color)),
        text=field1_name
    )

    # Combine all elements and configure
    return (
        (field1_labels & mosaic)
        .resolve_scale(x="shared")
        .configure_view()
        .configure_concat(spacing=10)
        .configure_axis(domain=False, ticks=False, labels=False, grid=False)
    )

def _create_bins(series, num_bins=6, na_label="NA_TOP"):
    if pd.api.types.is_numeric_dtype(series):
        bins = np.histogram_bin_edges(series.dropna(), bins=num_bins)
        labels = [f"{bins[i]:.1f}-{bins[i+1]:.1f}" for i in range(len(bins)-1)]
        binned = pd.cut(series, bins=bins, labels=labels, include_lowest=True)
        return binned
    elif series.nunique() > num_bins:
        # Handle categorical data by keeping only the top categories
        top_categories = series.value_counts().nlargest(num_bins - 1).index
        series = series.where(series.isin(top_categories), na_label)
    return series
