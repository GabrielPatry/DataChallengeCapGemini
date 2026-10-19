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
from pathlib import Path
from typing import ClassVar

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
