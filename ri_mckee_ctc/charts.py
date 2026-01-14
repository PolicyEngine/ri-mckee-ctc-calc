"""Chart generation for RI Governor McKee's CTC analysis."""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ri_mckee_ctc.household import calculate_net_income_changes
from ri_mckee_ctc.statewide import (
    DECILE_OUTCOMES,
    OVERALL_OUTCOMES,
    AVG_BENEFIT_BY_DECILE,
    OUTCOME_CATEGORIES,
)

# PolicyEngine color palette
COLORS = {
    "primary": "#319795",  # Teal
    "primary_dark": "#285E61",
    "positive": "#319795",  # Teal for gains
    "negative": "#718096",  # Gray for losses
    "neutral": "#A0AEC0",
    "gain_more": "#2C7A7B",
    "gain_less": "#38B2AC",
    "no_change": "#CBD5E0",
    "loss_less": "#A0AEC0",
    "loss_more": "#718096",
    "background": "#FFFFFF",
    "grid": "#E2E8F0",
    "text": "#2D3748",
}

# Watermark configuration
WATERMARK = dict(
    source="https://policyengine.org/assets/logos/policyengine/teal-square.png",
    xref="paper",
    yref="paper",
    x=1.0,
    y=-0.15,
    sizex=0.1,
    sizey=0.1,
    xanchor="right",
    yanchor="bottom",
    opacity=0.5,
)


def _get_layout(title: str, xaxis_title: str, yaxis_title: str) -> dict:
    """Get standard layout configuration."""
    return dict(
        title=dict(
            text=title,
            font=dict(family="Roboto", size=18, color=COLORS["text"]),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            title=xaxis_title,
            titlefont=dict(family="Roboto", size=14, color=COLORS["text"]),
            tickfont=dict(family="Roboto", size=12, color=COLORS["text"]),
            gridcolor=COLORS["grid"],
            showgrid=True,
        ),
        yaxis=dict(
            title=yaxis_title,
            titlefont=dict(family="Roboto", size=14, color=COLORS["text"]),
            tickfont=dict(family="Roboto", size=12, color=COLORS["text"]),
            gridcolor=COLORS["grid"],
            showgrid=True,
        ),
        plot_bgcolor=COLORS["background"],
        paper_bgcolor=COLORS["background"],
        font=dict(family="Roboto"),
        images=[WATERMARK],
        margin=dict(l=60, r=40, t=60, b=80),
    )


def create_net_income_change_chart(num_children: int = 2) -> go.Figure:
    """Create chart showing net income change by employment income.

    Args:
        num_children: Number of qualifying children

    Returns:
        Plotly figure
    """
    incomes, changes = calculate_net_income_changes(
        min_income=0,
        max_income=300_000,
        step=1_000,
        num_children=num_children,
    )

    # Convert to thousands for display
    incomes_k = [i / 1000 for i in incomes]

    fig = go.Figure()

    # Add the line
    fig.add_trace(
        go.Scatter(
            x=incomes_k,
            y=changes,
            mode="lines",
            line=dict(color=COLORS["primary"], width=3),
            name="Net income change",
            hovertemplate="Income: $%{x:.0f}k<br>Change: $%{y:.0f}<extra></extra>",
        )
    )

    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color=COLORS["neutral"], opacity=0.7)

    # Add phase-out threshold annotation
    fig.add_vline(
        x=261,
        line_dash="dot",
        line_color=COLORS["neutral"],
        opacity=0.7,
        annotation_text="Phase-out starts ($261k)",
        annotation_position="top",
    )

    fig.update_layout(
        **_get_layout(
            title=f"Change in net income for a married couple with {num_children} children",
            xaxis_title="Employment income ($k)",
            yaxis_title="Change in annual net income ($)",
        )
    )

    return fig


def create_winners_by_decile_chart() -> go.Figure:
    """Create stacked bar chart showing winners/losers by income decile.

    Returns:
        Plotly figure
    """
    # Prepare data
    deciles = ["All"] + [str(i) for i in range(1, 11)]

    category_colors = {
        "GAIN_MORE_THAN_5PCT": COLORS["gain_more"],
        "GAIN_LESS_THAN_5PCT": COLORS["gain_less"],
        "NO_CHANGE": COLORS["no_change"],
        "LOSS_LESS_THAN_5PCT": COLORS["loss_less"],
        "LOSS_MORE_THAN_5PCT": COLORS["loss_more"],
    }

    category_names = {
        "GAIN_MORE_THAN_5PCT": "Gain more than 5%",
        "GAIN_LESS_THAN_5PCT": "Gain less than 5%",
        "NO_CHANGE": "No change",
        "LOSS_LESS_THAN_5PCT": "Lose less than 5%",
        "LOSS_MORE_THAN_5PCT": "Lose more than 5%",
    }

    fig = go.Figure()

    for category in OUTCOME_CATEGORIES:
        values = [OVERALL_OUTCOMES[category]]
        for decile in range(1, 11):
            values.append(DECILE_OUTCOMES[decile][category])

        fig.add_trace(
            go.Bar(
                name=category_names[category],
                x=deciles,
                y=values,
                marker_color=category_colors[category],
                hovertemplate="%{x}<br>%{y:.1f}%<extra>" + category_names[category] + "</extra>",
            )
        )

    fig.update_layout(
        barmode="stack",
        **_get_layout(
            title="Winners and losers of RI Governor McKee's CTC by income decile",
            xaxis_title="Income decile",
            yaxis_title="Share of population (%)",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
        ),
    )

    return fig


def create_avg_benefit_by_decile_chart() -> go.Figure:
    """Create bar chart showing average benefit by income decile.

    Returns:
        Plotly figure
    """
    deciles = list(range(1, 11))
    benefits = [AVG_BENEFIT_BY_DECILE[d] for d in deciles]

    # Color bars based on positive/negative
    colors = [COLORS["positive"] if b >= 0 else COLORS["negative"] for b in benefits]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[str(d) for d in deciles],
            y=benefits,
            marker_color=colors,
            hovertemplate="Decile %{x}<br>Average: $%{y:.0f}<extra></extra>",
        )
    )

    fig.add_hline(y=0, line_color=COLORS["text"], line_width=1)

    fig.update_layout(
        **_get_layout(
            title="Average benefit of RI Governor McKee's CTC by income decile",
            xaxis_title="Income decile",
            yaxis_title="Average change in household income ($)",
        )
    )

    return fig
