"""Plotting step — build plotly figures from the solar and wind incidents CSVs.

``SolarPlotFactory`` and ``WindPlotFactory`` each wrap one clusterised
incidents dataframe and expose one ``plot_*`` method per figure. Every method
returns a ``plotly.graph_objects.Figure`` and a dictionary describing the
figure, built from the dataframe held in the ``df`` attribute.

The pipeline iterates over every ``plot_*`` method (see
``PlotFactory.plot_method_names``) and saves each figure as a PNG in the
``png`` subfolder (requires the ``kaleido`` package) and an interactive HTML
page in the ``html`` subfolder. Each method's description is saved as JSON in
the ``json`` subfolder.

Available as a CLI step through the top-level ``datachallengecapgemini``
entry point:

- ``uv run datachallengecapgemini`` — preprocessing (optional) + plotting
"""

import argparse
import inspect
import json
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

from datachallengecapgemini.equipment_stats import (
    SEVERE,
    UNCLASSIFIED,
    build_equipment_stats,
    classified,
    failure_mode_weather_matrix,
    format_eur,
    number_incidents,
    ordered_weather,
    site_focus,
    weather_table,
)

# Project root: src/datachallengecapgemini/plot_factory.py -> 3 levels up
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Prefix marking the graph-building methods of PlotFactory. The pipeline
# iterates over every method with this prefix, so adding a new ``plot_*``
# method is enough to add a new figure to the pipeline output.
PLOT_METHOD_PREFIX = "plot_"

# Severity levels in increasing order of seriousness (used for axis ordering)
SEVERITY_ORDER: list[str] = ["mineure", "modérée", "sévère"]


class PlotFactory:
    """Builds plotly figures from an incidents dataframe.

    The dataframe is the main attribute (``df``). Use ``PlotFactory.from_csv``
    to load and validate it from a CSV, or pass a dataframe directly to the
    constructor.
    """

    # Columns the plots rely on. ``text``, ``document_format`` and
    # ``document_path`` are intentionally excluded.
    REQUIRED_COLUMNS: ClassVar[list[str]] = [
        "site",
        "asset_type",
        "equipment_id",
        "date",
        "severity",
        "downtime_hours",
        "estimated_cost_eur",
        "weather_condition",
        "technician_id",
    ]

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    @classmethod
    def from_csv(cls, csv_path: Path) -> "PlotFactory":
        """Load the merged incidents CSV from *csv_path* and validate it.

        Raises
        ------
        ValueError
            If a required column is missing, or if a required column contains
            NaN values.
        """
        df = pd.read_csv(csv_path)

        missing = [col for col in cls.REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(
                f"{csv_path} is missing required columns: {', '.join(missing)}. "
                f"Expected columns: {', '.join(cls.REQUIRED_COLUMNS)}"
            )

        nan_columns = [col for col in cls.REQUIRED_COLUMNS if df[col].isna().any()]
        if nan_columns:
            raise ValueError(
                f"{csv_path} has NaN values in required columns: "
                f"{', '.join(nan_columns)}"
            )

        return cls(df)

    @classmethod
    def plot_method_names(cls) -> list[str]:
        """Names of all graph-building methods (``plot_*``), sorted alphabetically."""
        return sorted(
            name
            for name, member in inspect.getmembers(cls, predicate=inspect.isfunction)
            if name.startswith(PLOT_METHOD_PREFIX)
        )

    # ------------------------------------------------------------------
    # Graph-building methods — each returns a plotly Figure and its description
    # ------------------------------------------------------------------

    def plot_daily_cost_for_equipment(
        self, equipment_id: str | None = None
    ) -> tuple[go.Figure, dict[str, object]]:
        """Daily estimated cost over time for a single equipment.

        Inspired by ``notebooks/view_csv_data.py``: costs are summed per day
        and missing days are filled with 0 over the full date range. When
        *equipment_id* is ``None``, the equipment with the highest total
        estimated cost is used.
        """
        if equipment_id is None:
            equipment_id = (
                self.df.groupby("equipment_id")["estimated_cost_eur"].sum().idxmax()
            )
        elif equipment_id not in set(self.df["equipment_id"]):
            raise ValueError(f"Unknown equipment_id: {equipment_id}")

        df_equipment = self.df[self.df["equipment_id"] == equipment_id].copy()
        df_equipment["date"] = pd.to_datetime(df_equipment["date"])

        df_daily_cost = (
            df_equipment.groupby("date")["estimated_cost_eur"].sum().reset_index()
        )
        full_date_range = pd.date_range(
            start=df_daily_cost["date"].min(),
            end=df_daily_cost["date"].max(),
            freq="D",
        )
        df_daily_cost = (
            df_daily_cost.set_index("date")
            .reindex(full_date_range, fill_value=0)
            .reset_index()
            .rename(columns={"index": "date"})
        )

        fig = px.line(
            df_daily_cost,
            x="date",
            y="estimated_cost_eur",
            title=f"Daily Estimated Cost Over Time - Equipment ID: {equipment_id}",
            labels={
                "date": "Date",
                "estimated_cost_eur": "Estimated Cost (EUR)",
            },
        )
        fig.update_traces(mode="lines+markers")
        description = {
            "title": f"Coût estimé quotidien - Équipement : {equipment_id}",
            "chart_type": "courbe avec marqueurs quotidiens",
            "main_features": (
                "Coût estimé quotidien pour un équipement ; les jours sans "
                "incident sont représentés par une valeur nulle."
            ),
            "equipment_id": str(equipment_id),
            "date_range": [
                df_daily_cost["date"].min().date().isoformat(),
                df_daily_cost["date"].max().date().isoformat(),
            ],
            "total_estimated_cost_eur": float(df_equipment["estimated_cost_eur"].sum()),
            "days_shown": len(df_daily_cost),
        }
        return fig, description

    def plot_cost_distribution_per_equipment_by_site(
        self,
    ) -> tuple[go.Figure, dict[str, object]]:
        """Box plot of the total estimated cost per equipment, grouped by site.

        Inspired by ``notebooks/view_csv_data.py``.
        """
        cost_by_site_equipment = (
            self.df.groupby(["site", "equipment_id"])["estimated_cost_eur"]
            .sum()
            .reset_index()
        )
        fig = px.box(
            cost_by_site_equipment,
            x="site",
            y="estimated_cost_eur",
            title="Distribution of Total Cost per Equipment by Site",
            labels={
                "site": "Site",
                "estimated_cost_eur": "Total Estimated Cost per Equipment (EUR)",
            },
            points="all",
            color="site",
        )
        fig.update_layout(showlegend=False)
        fig.update_yaxes(showgrid=True, zeroline=False)
        description = {
            "title": "Distribution du coût total par équipement et par site",
            "chart_type": "boîte à moustaches avec les points de chaque équipement",
            "main_features": (
                "Compare la distribution du coût total estimé par équipement "
                "entre les sites ; chaque point représente un équipement."
            ),
            "sites": sorted(cost_by_site_equipment["site"].astype(str).unique()),
            "equipment_count": len(cost_by_site_equipment),
            "cost_metric": "coût total estimé par équipement (EUR)",
        }
        return fig, description

    def plot_daily_cost_top_equipment_at_top_site(
        self, top_n: int = 3
    ) -> tuple[go.Figure, dict[str, object]]:
        """Daily estimated cost over time for the top-N equipment at the highest-cost site.

        Inspired by ``notebooks/view_csv_data.py``: the site with the highest
        total estimated cost is selected, then its top-N equipment by total
        cost. Markers only (no connecting lines) to avoid interpolating
        between days without incidents.
        """
        cost_by_site = self.df.groupby("site")["estimated_cost_eur"].sum()
        selected_site = cost_by_site.idxmax()

        df_site = self.df[self.df["site"] == selected_site].copy()
        df_site["date"] = pd.to_datetime(df_site["date"])

        cost_by_equipment_site = (
            df_site.groupby("equipment_id")["estimated_cost_eur"]
            .sum()
            .reset_index()
            .sort_values("estimated_cost_eur", ascending=False)
        )
        top_equipment = cost_by_equipment_site.head(top_n)["equipment_id"].tolist()

        full_date_range = pd.date_range(
            start=df_site["date"].min(), end=df_site["date"].max(), freq="D"
        )
        frames = []
        for equip_id in top_equipment:
            df_equip_daily = (
                df_site[df_site["equipment_id"] == equip_id]
                .groupby("date")["estimated_cost_eur"]
                .sum()
                .reset_index()
                .set_index("date")
                .reindex(full_date_range, fill_value=0)
                .reset_index()
                .rename(columns={"index": "date"})
            )
            df_equip_daily["equipment_id"] = str(equip_id)
            frames.append(df_equip_daily)
        df_plot = pd.concat(frames, ignore_index=True)

        fig = px.line(
            df_plot,
            x="date",
            y="estimated_cost_eur",
            color="equipment_id",
            title=f"Estimated Cost Over Time - Top {top_n} Equipment at Site: {selected_site}",
            labels={
                "date": "Date",
                "estimated_cost_eur": "Estimated Cost (EUR)",
                "equipment_id": "Equipment ID",
            },
        )
        fig.update_traces(mode="markers", marker={"size": 8})
        description = {
            "title": (
                f"Évolution du coût estimé - {top_n} équipements principaux "
                f"du site : {selected_site}"
            ),
            "chart_type": "nuage de points quotidien avec une série par équipement",
            "main_features": (
                "Coûts quotidiens des équipements les plus coûteux du site dont "
                "le coût estimé total est le plus élevé. Les marqueurs ne sont "
                "pas reliés par des lignes."
            ),
            "selected_site": str(selected_site),
            "site_total_estimated_cost_eur": float(cost_by_site.loc[selected_site]),
            "top_equipment": [
                {
                    "equipment_id": str(row["equipment_id"]),
                    "total_estimated_cost_eur": float(row["estimated_cost_eur"]),
                }
                for _, row in cost_by_equipment_site.head(top_n).iterrows()
            ],
        }
        return fig, description

    def plot_incident_count_by_severity(
        self,
    ) -> tuple[go.Figure, dict[str, object]]:
        """Number of incidents per severity level, split by asset type."""
        counts = (
            self.df.groupby(["severity", "asset_type"])
            .size()
            .to_frame("incident_count")
            .reset_index()
        )
        fig = px.bar(
            counts,
            x="severity",
            y="incident_count",
            color="asset_type",
            barmode="group",
            title="Number of Incidents by Severity and Asset Type",
            labels={
                "severity": "Severity",
                "incident_count": "Number of Incidents",
                "asset_type": "Asset Type",
            },
            category_orders={"severity": SEVERITY_ORDER},
        )
        description = {
            "title": "Nombre d'incidents par niveau de sévérité et type d'actif",
            "chart_type": "diagramme à barres groupées",
            "main_features": (
                "Compare le nombre d'incidents par niveau de sévérité, avec des "
                "barres distinctes pour chaque type d'actif."
            ),
            "incident_counts": [
                {
                    "severity": str(row["severity"]),
                    "asset_type": str(row["asset_type"]),
                    "incident_count": int(row["incident_count"]),
                }
                for _, row in counts.iterrows()
            ],
        }
        return fig, description

    def plot_total_cost_by_weather_condition(
        self,
    ) -> tuple[go.Figure, dict[str, object]]:
        """Total estimated cost per weather condition, split by asset type."""
        totals = (
            self.df.groupby(["weather_condition", "asset_type"])["estimated_cost_eur"]
            .sum()
            .reset_index()
        )
        fig = px.bar(
            totals,
            x="weather_condition",
            y="estimated_cost_eur",
            color="asset_type",
            barmode="group",
            title="Total Estimated Cost by Weather Condition and Asset Type",
            labels={
                "weather_condition": "Weather Condition",
                "estimated_cost_eur": "Total Estimated Cost (EUR)",
                "asset_type": "Asset Type",
            },
        )
        fig.update_xaxes(tickangle=-45)
        description = {
            "title": "Coût estimé total par condition météorologique et type d'actif",
            "chart_type": "diagramme à barres groupées",
            "main_features": (
                "Compare le coût estimé total selon les conditions "
                "météorologiques, avec des barres distinctes pour chaque type "
                "d'actif."
            ),
            "cost_totals_eur": [
                {
                    "weather_condition": str(row["weather_condition"]),
                    "asset_type": str(row["asset_type"]),
                    "total_estimated_cost_eur": float(row["estimated_cost_eur"]),
                }
                for _, row in totals.iterrows()
            ],
        }
        return fig, description

    def plot_downtime_vs_cost(self) -> tuple[go.Figure, dict[str, object]]:
        """Scatter plot of downtime duration vs estimated cost, per asset type."""
        fig = px.scatter(
            self.df,
            x="downtime_hours",
            y="estimated_cost_eur",
            color="severity",
            facet_col="asset_type",
            opacity=0.6,
            title="Estimated Cost vs Downtime Duration",
            labels={
                "downtime_hours": "Downtime (hours)",
                "estimated_cost_eur": "Estimated Cost (EUR)",
                "severity": "Severity",
                "asset_type": "Asset Type",
            },
            category_orders={"severity": SEVERITY_ORDER},
        )
        description = {
            "title": "Coût estimé en fonction du temps d'arrêt",
            "chart_type": "nuage de points avec facettes",
            "main_features": (
                "Chaque point représente un incident ; le temps d'arrêt est en "
                "abscisse, le coût estimé en ordonnée, la couleur indique la "
                "sévérité et les panneaux distinguent les types d'actifs."
            ),
            "incident_count": len(self.df),
            "incident_counts_by_asset_type": {
                str(key): int(value)
                for key, value in self.df["asset_type"].value_counts().items()
            },
            "incident_counts_by_severity": {
                str(key): int(value)
                for key, value in self.df["severity"].value_counts().items()
            },
        }
        return fig, description

    def plot_monthly_incident_count(
        self,
    ) -> tuple[go.Figure, dict[str, object]]:
        """Number of incidents per month over time, split by asset type."""
        df_plot = self.df.copy()
        df_plot["date"] = pd.to_datetime(df_plot["date"])
        df_plot["month"] = df_plot["date"].dt.to_period("M").dt.to_timestamp()
        counts = (
            df_plot.groupby(["month", "asset_type"])
            .size()
            .to_frame("incident_count")
            .reset_index()
        )
        fig = px.line(
            counts,
            x="month",
            y="incident_count",
            color="asset_type",
            title="Number of Incidents per Month by Asset Type",
            labels={
                "month": "Month",
                "incident_count": "Number of Incidents",
                "asset_type": "Asset Type",
            },
        )
        fig.update_traces(mode="lines+markers")
        description = {
            "title": "Nombre d'incidents par mois et par type d'actif",
            "chart_type": "courbe mensuelle avec marqueurs",
            "main_features": (
                "Présente l'évolution mensuelle du nombre d'incidents, avec une "
                "série distincte pour chaque type d'actif."
            ),
            "monthly_incident_counts": [
                {
                    "month": row["month"].date().isoformat(),
                    "asset_type": str(row["asset_type"]),
                    "incident_count": int(row["incident_count"]),
                }
                for _, row in counts.iterrows()
            ],
        }
        return fig, description

    def plot_total_cost_by_site(self) -> tuple[go.Figure, dict[str, object]]:
        """Total estimated cost per site, split by asset type."""
        totals = (
            self.df.groupby(["site", "asset_type"])["estimated_cost_eur"]
            .sum()
            .reset_index()
        )
        fig = px.bar(
            totals,
            x="site",
            y="estimated_cost_eur",
            color="asset_type",
            barmode="group",
            title="Total Estimated Cost by Site and Asset Type",
            labels={
                "site": "Site",
                "estimated_cost_eur": "Total Estimated Cost (EUR)",
                "asset_type": "Asset Type",
            },
        )
        description = {
            "title": "Coût estimé total par site et type d'actif",
            "chart_type": "diagramme à barres groupées",
            "main_features": (
                "Compare le coût estimé total des incidents entre les sites, "
                "avec des barres distinctes pour chaque type d'actif."
            ),
            "cost_totals_eur": [
                {
                    "site": str(row["site"]),
                    "asset_type": str(row["asset_type"]),
                    "total_estimated_cost_eur": float(row["estimated_cost_eur"]),
                }
                for _, row in totals.iterrows()
            ],
        }
        return fig, description


class SolarPlotFactory(PlotFactory):
    """Build plots from the clusterised solar incidents dataframe."""


class WindPlotFactory(PlotFactory):
    """Build plots from the clusterised wind incidents dataframe."""


# ---------------------------------------------------------------------------
# Pipeline step — build every plot and save it as PNG + HTML + JSON
# ---------------------------------------------------------------------------


def run_plotting(
    solar_csv_path: Path, wind_csv_path: Path, plots_output_dir: Path
) -> None:
    """Build solar and wind plots under separate directories in *plots_output_dir*.

    Each figure and its description are saved as ``<name>.png`` in the
    ``png`` subfolder, ``<name>.html`` in the ``html`` subfolder, and
    ``<name>.json`` in the ``json`` subfolder, where ``<name>`` is a
    ``plot_*`` method name.
    """
    for label, factory_type, csv_path in (
        ("solar", SolarPlotFactory, solar_csv_path),
        ("wind", WindPlotFactory, wind_csv_path),
    ):
        factory = factory_type.from_csv(csv_path)
        output_dir = plots_output_dir / label
        png_dir = output_dir / "png"
        html_dir = output_dir / "html"
        json_dir = output_dir / "json"
        png_dir.mkdir(parents=True, exist_ok=True)
        html_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)

        for name in factory_type.plot_method_names():
            fig, description = getattr(factory, name)()
            png_path = png_dir / f"{name}.png"
            html_path = html_dir / f"{name}.html"
            json_path = json_dir / f"{name}.json"
            fig.write_image(png_path)
            fig.write_html(html_path)
            json_path.write_text(
                json.dumps(description, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(f"Saved {png_path}")
            print(f"Saved {html_path}")
            print(f"Saved {json_path}")

        print(
            f"Done. {len(factory_type.plot_method_names())} {label} plots are in {output_dir}"
        )


def add_plotting_arguments(parser: argparse.ArgumentParser) -> None:
    """Add plotting-specific arguments to *parser*."""
    parser.add_argument(
        "--solar-csv",
        type=Path,
        default=PROJECT_ROOT / "data" / "incidents_clusterised_solar.csv",
        help="Path to the clusterised solar incidents CSV.",
    )
    parser.add_argument(
        "--wind-csv",
        type=Path,
        default=PROJECT_ROOT / "data" / "incidents_clusterised_wind.csv",
        help="Path to the clusterised wind incidents CSV.",
    )
    parser.add_argument(
        "--plots-output-dir",
        type=Path,
        default=PROJECT_ROOT / "data" / "plots",
        help="Directory where plots are saved (png/, html/ and json/ subfolders are created inside).",
    )


# ===========================================================================
# Equipment-level figures — one PNG + one JSON (the plotted data) per figure
# ===========================================================================
#
# The equipment reports are built per equipment of a site. Their figures are
# static matplotlib PNGs (no kaleido/Chrome needed) and each one comes with
# the JSON of the data it shows, which ``report_factory`` injects into the
# prompt of the section that comments the figure.

# Failure-mode families: colour = family, marker shape = failure mode inside
# the family. Cluster names are regenerated by the LLM at each clustering run,
# so a failure mode is assigned to its family by keywords (lowercase, accents
# removed). Families are tried in this order: the first match wins (e.g.
# "Salissure et nettoyage modules PV" is soiling, not modules).
FAILURE_MODE_FAMILIES: dict[str, list[str]] = {
    "Fire": ["incendie", "feu", "fumee"],
    "Soiling": ["salissure", "nettoyage", "encrassement", "poussiere"],
    "Overheating": ["surchauffe", "temperature"],
    "Junction box / connectors": ["jonction", "connecteur", "chaine"],
    "Cabling": ["cablage", "cable", "isolement", "court-circuit"],
    "Overvoltage": ["surtension", "foudre", "parafoudre"],
    "Inverter": ["onduleur"],
    "Modules": ["module", "panneau"],
}
# Reference categorical palette, fixed colour per family (CVD-validated on
# adjacent pairs); failure modes matching no family are grey
FAMILY_COLORS: dict[str, str] = {
    "Fire": "#2a78d6",
    "Junction box / connectors": "#eb6834",
    "Cabling": "#1baf7a",
    "Overvoltage": "#eda100",
    "Modules": "#e87ba4",
    "Overheating": "#008300",
    "Soiling": "#6250d6",
    "Inverter": "#e34948",
    "Other": "#8a8984",
}
FAMILY_MARKERS: list[str] = ["o", "s", "^", "D", "v", "P"]
# Unclassified incidents (noise cluster): grey cross
DEFAULT_STYLE = ("#8a8984", "X")
TEXT_SECONDARY = "#52514e"
GRID_COLOR = "#e4e3df"
SEQUENTIAL_BLUES = ["#fcfcfb", "#cde2fb", "#86b6ef", "#2a78d6", "#184f95"]


def _plain(text: str) -> str:
    """Lowercase *text* without accents, for keyword matching."""
    decomposed = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def failure_mode_family(mode: str) -> str:
    """Family of a failure mode name (``"Other"`` when no keyword matches)."""
    name = _plain(mode)
    for family, keywords in FAILURE_MODE_FAMILIES.items():
        if any(keyword in name for keyword in keywords):
            return family
    return "Other"


def failure_mode_styles(modes: Iterable[str]) -> dict[str, tuple[str, str]]:
    """``{failure_mode: (colour, marker)}`` for every failure mode of *modes*.

    Within a family, markers follow the alphabetical order of the failure
    modes, so pass every failure mode of the dataset (not only those of one
    equipment) to keep the same style across all equipment.
    """
    styles = {UNCLASSIFIED: DEFAULT_STYLE}
    by_family: dict[str, list[str]] = {}
    for mode in sorted(set(modes) - {UNCLASSIFIED}):
        by_family.setdefault(failure_mode_family(mode), []).append(mode)
    for family, members in by_family.items():
        for i, mode in enumerate(members):
            styles[mode] = (
                FAMILY_COLORS[family],
                FAMILY_MARKERS[i % len(FAMILY_MARKERS)],
            )
    return styles


@dataclass
class EquipmentPlot:
    """A figure and the data it shows (sent to the LLM along with the figure)."""

    figure: Figure
    data: dict


def _style_axes(ax) -> None:
    ax.grid(color=GRID_COLOR, lw=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID_COLOR)
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=9)


class EquipmentPlotFactory:
    """Builds the figures of one equipment report from the solar incidents dataframe.

    The whole dataframe is kept (``df``) because some figures compare the
    equipment with the rest of its site. Each ``plot_*`` method returns an
    ``EquipmentPlot``; adding a method is enough to add a figure (and its
    JSON) to the pipeline output.
    """

    REQUIRED_COLUMNS: ClassVar[list[str]] = [
        *PlotFactory.REQUIRED_COLUMNS,
        "incident_id",
        "cluster_name",
    ]

    def __init__(self, df: pd.DataFrame, equipment_id: str) -> None:
        missing = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(missing)}")
        self.df = df
        self.equipment_id = equipment_id
        self.styles = failure_mode_styles(df["cluster_name"].unique())
        self.incidents = number_incidents(df, equipment_id)
        if self.incidents.empty:
            raise ValueError(
                f"{equipment_id} has no moderate or severe incident to plot"
            )
        self.site = self.incidents["site"].iloc[0]

    @classmethod
    def plot_method_names(cls) -> list[str]:
        """Names of all graph-building methods (``plot_*``), sorted alphabetically."""
        return sorted(
            name
            for name, member in inspect.getmembers(cls, predicate=inspect.isfunction)
            if name.startswith(PLOT_METHOD_PREFIX)
        )

    def plot_cost_timeline(self) -> EquipmentPlot:
        """Cost of each moderate/severe incident over time, by failure mode.

        Colour = failure-mode family, marker shape = failure mode, filled =
        severe, hollow = moderate. The three most costly incidents are labelled.
        """
        d = self.incidents
        fig = Figure(figsize=(11, 4.6))
        ax = fig.subplots()
        ax.plot(d["date"], d["estimated_cost_eur"], color=GRID_COLOR, lw=1.2, zorder=1)
        for mode, g in d.groupby("cluster_name"):
            color, marker = self.styles[str(mode)]
            severe = g["severity"] == SEVERE
            ax.scatter(
                g.loc[severe, "date"],
                g.loc[severe, "estimated_cost_eur"],
                s=70,
                marker=marker,
                color=color,
                edgecolor="white",
                linewidth=1.5,
                zorder=3,
            )
            ax.scatter(
                g.loc[~severe, "date"],
                g.loc[~severe, "estimated_cost_eur"],
                s=60,
                marker=marker,
                facecolor="white",
                edgecolor=color,
                linewidth=2,
                zorder=3,
            )

        top = d.nlargest(3, "estimated_cost_eur")
        for _, r in top.iterrows():
            ax.annotate(
                f"{r['ref']} · {format_eur(r['estimated_cost_eur'])} €",
                (r["date"], r["estimated_cost_eur"]),
                xytext=(8, 6),
                textcoords="offset points",
                fontsize=9,
                color=TEXT_SECONDARY,
            )

        _style_axes(ax)
        ax.set_ylabel("Estimated cost (€)", color=TEXT_SECONDARY)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: format_eur(v)))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        pad = pd.Timedelta(days=20)
        ax.set_xlim(self.df["date"].min() - pad, self.df["date"].max() + pad)
        ax.set_title(
            f"{self.equipment_id} — cost of moderate and severe incidents by failure mode",
            loc="left",
            fontsize=12,
        )

        handles = []
        for mode in sorted(d["cluster_name"].unique()):
            color, marker = self.styles[str(mode)]
            handles.append(
                Line2D(
                    [], [], ls="", marker=marker, color=color, markersize=8, label=mode
                )
            )
        handles += [
            Line2D(
                [],
                [],
                ls="",
                marker="o",
                color=TEXT_SECONDARY,
                markersize=8,
                label="filled = severe",
            ),
            Line2D(
                [],
                [],
                ls="",
                marker="o",
                markerfacecolor="white",
                markeredgecolor=TEXT_SECONDARY,
                markeredgewidth=2,
                markersize=8,
                label="hollow = moderate",
            ),
        ]
        ax.legend(
            handles=handles,
            loc="upper left",
            bbox_to_anchor=(1.01, 1),
            frameon=False,
            fontsize=8,
        )
        fig.tight_layout()

        points = [
            {
                "ref": r["ref"],
                "date": f"{r['date']:%Y-%m-%d}",
                "severity": r["severity"],
                "failure_mode": r["cluster_name"],
                "cost_eur": round(float(r["estimated_cost_eur"])),
                "downtime_h": round(float(r["downtime_hours"]), 1),
                "weather_condition": r["weather_condition"],
                "days_since_previous_incident": None
                if pd.isna(r["days_since_previous"])
                else int(r["days_since_previous"]),
                "days_since_previous_same_failure_mode": None
                if pd.isna(r["days_since_previous_same_mode"])
                else int(r["days_since_previous_same_mode"]),
            }
            for _, r in d.iterrows()
        ]
        data = {
            "figure": "Cost timeline of moderate and severe incidents",
            "how_to_read": "One point per incident, in chronological order; the three most "
            "costly incidents are labelled on the figure.",
            "labelled_incidents": top["ref"].tolist(),
            "points": points,
        }
        return EquipmentPlot(fig, data)

    def plot_downtime_weather(self) -> EquipmentPlot:
        """Downtime of each incident per weather condition (dot strip + median tick)."""
        d = self.incidents
        conditions = ordered_weather(d["weather_condition"])
        fig = Figure(figsize=(9, 0.5 * len(conditions) + 1.4))
        ax = fig.subplots()
        rng = np.random.default_rng(0)
        for i, weather in enumerate(conditions):
            g = d[d["weather_condition"] == weather]
            y = i + rng.uniform(-0.15, 0.15, len(g))
            ax.scatter(
                g["downtime_hours"],
                y,
                s=40,
                color="#2a78d6",
                edgecolor="white",
                linewidth=1,
                zorder=3,
            )
            ax.vlines(
                g["downtime_hours"].median(),
                i - 0.3,
                i + 0.3,
                color="#0b0b0b",
                lw=2,
                zorder=4,
            )
            ax.text(
                1.01,
                i,
                f"n={len(g)} · {g['downtime_hours'].sum():.0f} h",
                transform=ax.get_yaxis_transform(),
                va="center",
                fontsize=8,
                color=TEXT_SECONDARY,
            )
        _style_axes(ax)
        ax.set_yticks(range(len(conditions)))
        ax.set_yticklabels(conditions)
        ax.invert_yaxis()
        ax.set_xlabel(
            "Downtime per incident in hours (black tick = median)", color=TEXT_SECONDARY
        )
        ax.set_title(
            f"{self.equipment_id} — downtime vs weather (moderate + severe)",
            loc="left",
            fontsize=12,
        )
        fig.tight_layout()

        data = {
            "figure": "Downtime vs weather condition",
            "how_to_read": "Rows sorted by total downtime. 'representation' compares the share of the "
            "equipment's incidents under this weather with the share on the whole site.",
            "rows": weather_table(d, site_focus(self.df, self.site)),
        }
        return EquipmentPlot(fig, data)

    def plot_cluster_weather(self) -> EquipmentPlot:
        """Number of incidents per failure mode and weather condition (sequential heatmap).

        Unclassified incidents are left out: they belong to no failure mode.
        """
        d = classified(self.incidents)
        ct = pd.crosstab(d["cluster_name"], d["weather_condition"])
        ct = ct[ordered_weather(ct.columns)]
        cmap = LinearSegmentedColormap.from_list("blues", SEQUENTIAL_BLUES)
        fig = Figure(figsize=(0.95 * ct.shape[1] + 4, 0.5 * ct.shape[0] + 1.8))
        ax = fig.subplots()
        vmax = max(int(ct.values.max()), 1)
        ax.imshow(ct.values, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
        for i in range(ct.shape[0]):
            for j in range(ct.shape[1]):
                n = ct.values[i, j]
                if n:
                    ax.text(
                        j,
                        i,
                        n,
                        ha="center",
                        va="center",
                        fontsize=9,
                        color="white" if n > 0.55 * vmax else "#0b0b0b",
                    )
        ax.set_xticks(range(ct.shape[1]))
        ax.set_xticklabels(
            ct.columns, rotation=30, ha="right", fontsize=9, color=TEXT_SECONDARY
        )
        ax.set_yticks(range(ct.shape[0]))
        ax.set_yticklabels(ct.index, fontsize=9, color=TEXT_SECONDARY)
        ax.set_xticks(np.arange(-0.5, ct.shape[1]), minor=True)
        ax.set_yticks(np.arange(-0.5, ct.shape[0]), minor=True)
        ax.grid(which="minor", color="white", lw=2)
        ax.tick_params(which="both", length=0)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_title(
            f"{self.equipment_id} — number of incidents: failure mode × weather",
            loc="left",
            fontsize=12,
        )
        fig.tight_layout()

        data = {
            "figure": "Failure modes vs weather condition",
            "how_to_read": "Number of incidents per failure mode (rows) and weather condition. A weather "
            "condition absent from a failure mode's row never occurred with that failure mode.",
            "matrix": failure_mode_weather_matrix(d),
        }
        return EquipmentPlot(fig, data)


def run_equipment_plotting(
    df: pd.DataFrame,
    criticality: pd.DataFrame,
    equipment_ids: list[str],
    site_dir: Path,
) -> None:
    """Write the figures and JSON files of every equipment report of one site.

    For each equipment, in ``<site_dir>/<equipment_id>/``:

    - ``figures/<name>.png`` — one PNG per ``EquipmentPlotFactory.plot_*`` method;
    - ``json/<name>.json`` — the data shown by that figure;
    - ``json/stats.json`` — every statistic of the report
      (``equipment_stats.build_equipment_stats``).
    """
    for equipment_id in equipment_ids:
        figures_dir = site_dir / equipment_id / "figures"
        json_dir = site_dir / equipment_id / "json"
        figures_dir.mkdir(parents=True, exist_ok=True)
        json_dir.mkdir(parents=True, exist_ok=True)

        factory = EquipmentPlotFactory(df, equipment_id)
        for method in EquipmentPlotFactory.plot_method_names():
            plot = getattr(factory, method)()
            name = method.removeprefix(PLOT_METHOD_PREFIX)
            plot.figure.savefig(
                figures_dir / f"{name}.png", dpi=150, bbox_inches="tight"
            )
            (json_dir / f"{name}.json").write_text(
                json.dumps(plot.data, ensure_ascii=False, indent=2), encoding="utf-8"
            )

        stats = build_equipment_stats(df, criticality, equipment_id)
        (json_dir / "stats.json").write_text(
            json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Saved figures and JSON of {equipment_id} in {site_dir / equipment_id}")


def add_equipment_plotting_arguments(parser: argparse.ArgumentParser) -> None:
    """Add equipment-plotting-specific arguments to *parser*."""
    # Team convention is data/; the branch also versions a copy at the root
    candidates = [
        PROJECT_ROOT / "data" / "incidents_clusterised_solar.csv",
        PROJECT_ROOT / "incidents_clusterised_solar.csv",
    ]
    parser.add_argument(
        "--solar-csv",
        type=Path,
        default=next((path for path in candidates if path.exists()), candidates[0]),
        help="Path to the clusterised solar incidents CSV (data/ first, then the project root).",
    )
    parser.add_argument(
        "--equipment-output-dir",
        type=Path,
        default=PROJECT_ROOT / "equipment_reports",
        help="Directory where <site>/<equipment>/{figures,json,sections,report.md} are written.",
    )
