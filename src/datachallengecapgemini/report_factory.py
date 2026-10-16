"""Report generation step — fill markdown report templates for solar and wind.

The pipeline ends with two markdown reports, one per asset type. Each report
is produced by filling a template stored in the ``templates/`` folder with:

- **Computed statistics** read from the clusterised incidents CSV (number of
  incidents, sites, total cost, downtime, severity breakdown, top clusters…).
- **Figures** — every ``{{ figure_<plot_name> }}`` placeholder is replaced by
  a markdown image pointing at ``data/plots/<label>/png/<plot_name>.png``
  (relative path, so the report stays portable inside the repository). If the
  PNG is missing but the interactive HTML version exists, a link to the HTML
  page is emitted instead.
- **Prose** — synopsis, methodology, per-cluster descriptions, recommendations
  and conclusion. For now these are placeholder texts defined in this module
  (``FAKE_PROSE``); they are meant to be replaced later by an LLM/agent step.

Placeholders use the ``{{ variable_name }}`` syntax. Filling is done with a
simple regex substitution (no templating dependency); unknown placeholders
raise an error so typos in templates are caught immediately.

Filled reports are written to ``filled_templates/solar/report.md`` and
``filled_templates/wind/report.md``.

Available as the last step of the top-level ``datachallengecapgemini`` entry
point:

- ``uv run datachallengecapgemini`` — preprocessing (optional) + plotting + reporting
"""

import argparse
import os
import re
from datetime import date
from pathlib import Path

import pandas as pd

# Project root: src/datachallengecapgemini/report_factory.py -> 3 levels up
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Placeholder syntax: {{ variable_name }}
PLACEHOLDER_PATTERN = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")

# Prefix of the placeholders that embed a figure: {{ figure_<plot_name> }}
FIGURE_PLACEHOLDER_PREFIX = "figure_"

# Cluster code used for the unclassified / noise incidents
NOISE_CLUSTER_CODE = "C_NOISE"

# Number of clusters detailed in the "cluster_sections" variable
N_DETAILED_CLUSTERS = 5

# Placeholder prose, per asset label. These texts are fake for now — they
# demonstrate which variables the templates expect and are meant to be
# replaced by generated content (LLM/agent step) later.
FAKE_PROSE: dict[str, dict[str, str | list[str]]] = {
    "solar": {
        "synopsis": (
            "This report presents the consolidated analysis of the photovoltaic "
            "incident reports collected across the solar fleet. Fire events on "
            "support buildings and rooftops, hot spots in junction boxes and "
            "cabling insulation defects dominate the incident landscape and "
            "concentrate a large share of the estimated financial losses. The "
            "sections below combine global statistics, thematic clustering of "
            "the incident descriptions and per-cluster root-cause hypotheses "
            "to support maintenance prioritisation."
        ),
        "methodology": (
            "Incident reports were consolidated into a single clusterised "
            "dataset covering every solar site. Each incident description was "
            "embedded and grouped into thematic clusters, then cross-referenced "
            "with the structured metadata (site, equipment, severity, downtime, "
            "estimated cost, weather conditions). All figures are generated "
            "from the clusterised dataset; costs are expressed in EUR and "
            "downtime in hours."
        ),
        "cluster_descriptions": [
            (
                "Incidents in this cluster share a common failure signature "
                "observed across several sites. Preliminary reading of the "
                "reports points to recurring contributing factors on the "
                "affected equipment; a dedicated root-cause analysis should "
                "confirm the dominant failure mechanism and quantify the "
                "associated downtime and cost exposure."
            ),
            (
                "The reports grouped here describe similar symptoms under "
                "comparable operating conditions, which suggests a systemic "
                "cause rather than isolated failures. A field inspection "
                "campaign on the most affected equipment is recommended to "
                "validate this hypothesis."
            ),
            (
                "This cluster aggregates incidents with comparable technical "
                "signatures. Cross-referencing the affected sites, the weather "
                "conditions at the time of the incidents and the equipment age "
                "should help isolate the triggering factors and prioritise "
                "corrective actions."
            ),
        ],
        "recommendations": (
            "- Prioritise fire-prevention inspections on support buildings and "
            "rooftop cable trays at the highest-cost sites.\n"
            "- Deploy recurring thermal-imaging campaigns on junction boxes to "
            "detect hot spots before failure.\n"
            "- Reinforce surge protection and grounding checks on equipment "
            "with recurrent overvoltage events.\n"
            "- Schedule preventive replacement of connectors on ageing cabling "
            "sections.\n"
            "- Review the maintenance contract scope for the equipment with "
            "the longest downtime per incident."
        ),
        "conclusion": (
            "The analysis shows that a small number of recurring failure themes "
            "account for most of the cost and downtime of the solar fleet. "
            "Acting on the recommendations above — first on fire-risk areas "
            "and junction-box hot spots — should deliver the largest reduction "
            "in both financial losses and production interruptions."
        ),
    },
    "wind": {
        "synopsis": (
            "This report presents the consolidated analysis of the incident "
            "reports collected across the wind fleet. Excessive-wind safety "
            "shutdowns, mechanical drivetrain failures and blade ruptures "
            "dominate the incident landscape and concentrate a large share of "
            "the estimated financial losses. The sections below combine global "
            "statistics, thematic clustering of the incident descriptions and "
            "per-cluster root-cause hypotheses to support maintenance "
            "prioritisation."
        ),
        "methodology": (
            "Incident reports were consolidated into a single clusterised "
            "dataset covering every wind farm. Each incident description was "
            "embedded and grouped into thematic clusters, then cross-referenced "
            "with the structured metadata (site, turbine, severity, downtime, "
            "estimated cost, weather conditions). All figures are generated "
            "from the clusterised dataset; costs are expressed in EUR and "
            "downtime in hours."
        ),
        "cluster_descriptions": [
            (
                "Incidents in this cluster share a common failure signature "
                "observed across several turbines. Preliminary reading of the "
                "reports points to recurring contributing factors on the "
                "affected equipment; a dedicated root-cause analysis should "
                "confirm the dominant failure mechanism and quantify the "
                "associated downtime and cost exposure."
            ),
            (
                "The reports grouped here describe similar symptoms under "
                "comparable wind and weather conditions, which suggests a "
                "systemic cause rather than isolated failures. A field "
                "inspection campaign on the most affected turbines is "
                "recommended to validate this hypothesis."
            ),
            (
                "This cluster aggregates incidents with comparable technical "
                "signatures. Cross-referencing the affected sites, the wind "
                "conditions at the time of the incidents and the turbine age "
                "should help isolate the triggering factors and prioritise "
                "corrective actions."
            ),
        ],
        "recommendations": (
            "- Strengthen storm shutdown procedures and post-event blade "
            "inspections at the most exposed sites.\n"
            "- Increase the frequency of mechanical drivetrain inspections on "
            "the most affected turbines.\n"
            "- Audit electrical protections and circuit breakers flagged in "
            "recurrent anomaly reports.\n"
            "- Deploy vibration monitoring on turbines with repeated "
            "structural or cosmetic damage.\n"
            "- Review spare-parts stocking for blades and major components at "
            "the highest-exposure sites."
        ),
        "conclusion": (
            "The analysis shows that a small number of recurring failure themes "
            "account for most of the cost and downtime of the wind fleet. "
            "Acting on the recommendations above — first on storm exposure "
            "and drivetrain reliability — should deliver the largest reduction "
            "in both financial losses and production interruptions."
        ),
    },
}


def fill_template(template: str, context: dict[str, str]) -> str:
    """Replace every ``{{ variable_name }}`` placeholder in *template*.

    Raises
    ------
    ValueError
        If a placeholder has no matching key in *context*.
    """
    unknown: list[str] = []

    def _replace(match: re.Match) -> str:
        name = match.group(1)
        if name not in context:
            unknown.append(name)
            return match.group(0)
        return context[name]

    filled = PLACEHOLDER_PATTERN.sub(_replace, template)
    if unknown:
        raise ValueError(
            f"Unknown template placeholder(s): {', '.join(sorted(set(unknown)))}. "
            f"Available variables: {', '.join(sorted(context))}"
        )
    return filled


def _figure_markdown(plot_name: str, plots_dir: Path, report_dir: Path) -> str:
    """Markdown for one figure: a PNG image, or a link to the HTML version."""
    png_path = plots_dir / "png" / f"{plot_name}.png"
    if png_path.exists():
        relative = os.path.relpath(png_path, report_dir).replace(os.sep, "/")
        return f"![{plot_name}]({relative})"
    html_path = plots_dir / "html" / f"{plot_name}.html"
    if html_path.exists():
        relative = os.path.relpath(html_path, report_dir).replace(os.sep, "/")
        return f"[Interactive figure: {plot_name}]({relative})"
    raise FileNotFoundError(
        f"No figure found for plot '{plot_name}' in {plots_dir / 'png'} "
        f"or {plots_dir / 'html'} — run the plotting step first."
    )


def build_report_context(
    df: pd.DataFrame, label: str, plots_dir: Path, report_dir: Path
) -> dict[str, str]:
    """Build every template variable for one report.

    Real statistics come from *df* (the clusterised incidents dataframe);
    prose blocks are the placeholder texts from ``FAKE_PROSE``; figures are
    resolved from *plots_dir* (``png`` and ``html`` subfolders) as
    ``figure_<plot_name>`` variables pointing relatively to *report_dir*.
    """
    prose = FAKE_PROSE[label]
    cluster_descriptions = prose["cluster_descriptions"]
    assert isinstance(cluster_descriptions, list)

    n_incidents = len(df)
    severity_counts = df["severity"].value_counts()
    total_cost = df["estimated_cost_eur"].sum()
    total_downtime = df["downtime_hours"].sum()
    dates = pd.to_datetime(df["date"])
    top_site = df.groupby("site")["estimated_cost_eur"].sum().idxmax()
    top_equipment = df.groupby("equipment_id")["estimated_cost_eur"].sum().idxmax()

    # Clusters, largest first; the noise cluster is reported separately
    cluster_counts = (
        df.groupby(["cluster_code", "cluster_name"])
        .size()
        .to_frame("incident_count")
        .reset_index()
        .sort_values("incident_count", ascending=False)
    )
    thematic_counts = cluster_counts[
        cluster_counts["cluster_code"] != NOISE_CLUSTER_CODE
    ]

    rows = ["| Cluster | Incidents | Share |", "| --- | ---: | ---: |"]
    for _, cluster in cluster_counts.iterrows():
        code = cluster["cluster_code"]
        name = cluster["cluster_name"]
        count = cluster["incident_count"]
        cell = (
            f"{name} (unclassified)"
            if code == NOISE_CLUSTER_CODE
            else f"{code} — {name}"
        )
        rows.append(f"| {cell} | {count} | {100 * count / n_incidents:.1f}% |")
    top_clusters_table = "\n".join(rows)

    sections = []
    for i, (_, cluster) in enumerate(
        thematic_counts.head(N_DETAILED_CLUSTERS).iterrows()
    ):
        code = cluster["cluster_code"]
        name = cluster["cluster_name"]
        count = cluster["incident_count"]
        cluster_df = df[df["cluster_code"] == code]
        cluster_top_site = (
            cluster_df.groupby("site")["estimated_cost_eur"].sum().idxmax()
        )
        dominant_severity = cluster_df["severity"].value_counts().idxmax()
        sections.append(
            f"### {code} — {name}\n\n"
            f"- **Incidents:** {count} ({100 * count / n_incidents:.1f}% of all incidents)\n"
            f"- **Most affected site:** {cluster_top_site}\n"
            f"- **Dominant severity:** {dominant_severity}\n\n"
            f"{cluster_descriptions[i % len(cluster_descriptions)]}"
        )
    cluster_sections = "\n\n".join(sections)

    context: dict[str, str] = {
        "report_title": f"{label.capitalize()} Asset Incident Analysis Report",
        "asset_label": label.capitalize(),
        "asset_label_lower": label,
        "generation_date": date.today().isoformat(),
        "n_incidents": str(n_incidents),
        "n_sites": str(df["site"].nunique()),
        "n_equipment": str(df["equipment_id"].nunique()),
        "period_start": dates.min().date().isoformat(),
        "period_end": dates.max().date().isoformat(),
        "total_cost_eur": f"{total_cost:,.2f}",
        "total_downtime_hours": f"{total_downtime:,.1f}",
        "avg_cost_per_incident": f"{total_cost / n_incidents:,.2f}",
        "n_minor": str(int(severity_counts.get("mineure", 0))),
        "n_moderate": str(int(severity_counts.get("modérée", 0))),
        "n_severe": str(int(severity_counts.get("sévère", 0))),
        "top_site_by_cost": str(top_site),
        "top_equipment_by_cost": str(top_equipment),
        "n_clusters": str(len(thematic_counts)),
        "top_clusters_table": top_clusters_table,
        "synopsis": str(prose["synopsis"]),
        "methodology": str(prose["methodology"]),
        "cluster_sections": cluster_sections,
        "recommendations": str(prose["recommendations"]),
        "conclusion": str(prose["conclusion"]),
    }

    # One figure_<plot_name> variable per available plot (PNG preferred,
    # interactive HTML as fallback)
    png_dir = plots_dir / "png"
    html_dir = plots_dir / "html"
    if not png_dir.is_dir() and not html_dir.is_dir():
        raise FileNotFoundError(
            f"No plots found in {plots_dir} — run the plotting step first "
            "(uv run datachallengecapgemini)."
        )
    plot_names = sorted(
        {path.stem for path in png_dir.glob("plot_*.png")}
        | {path.stem for path in html_dir.glob("plot_*.html")}
    )
    for plot_name in plot_names:
        context[f"{FIGURE_PLACEHOLDER_PREFIX}{plot_name}"] = _figure_markdown(
            plot_name, plots_dir, report_dir
        )

    return context


def render_report(template: str, context: dict[str, str], plots_dir: Path) -> str:
    """Fill *template* with *context*, with a specific error for bad figures."""
    for match in PLACEHOLDER_PATTERN.finditer(template):
        name = match.group(1)
        if name.startswith(FIGURE_PLACEHOLDER_PREFIX) and name not in context:
            plot_name = name[len(FIGURE_PLACEHOLDER_PREFIX) :]
            raise ValueError(
                f"Template references unknown figure '{{{{ {name} }}}}' — no plot "
                f"'{plot_name}' found in {plots_dir / 'png'} or "
                f"{plots_dir / 'html'}."
            )
    return fill_template(template, context)


def run_reporting(
    solar_csv_path: Path,
    wind_csv_path: Path,
    plots_output_dir: Path,
    templates_dir: Path,
    reports_output_dir: Path,
) -> None:
    """Fill the solar and wind markdown templates and save the reports.

    Reads ``<templates_dir>/<label>_report.md`` for each label, fills it with
    statistics from the clusterised CSV and figures from
    ``<plots_output_dir>/<label>/{png,html}``, and writes the result to
    ``<reports_output_dir>/<label>/report.md``.
    """
    for label, csv_path in (("solar", solar_csv_path), ("wind", wind_csv_path)):
        template_path = templates_dir / f"{label}_report.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Report template not found: {template_path}")

        df = pd.read_csv(csv_path)
        plots_dir = plots_output_dir / label
        report_dir = reports_output_dir / label
        report_dir.mkdir(parents=True, exist_ok=True)

        template = template_path.read_text(encoding="utf-8")
        context = build_report_context(df, label, plots_dir, report_dir)
        report = render_report(template, context, plots_dir)

        report_path = report_dir / "report.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"Saved {report_path}")

    print(f"Done. Filled reports are in {reports_output_dir}")


def add_report_arguments(parser: argparse.ArgumentParser) -> None:
    """Add report-generation-specific arguments to *parser*."""
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=PROJECT_ROOT / "templates",
        help="Directory containing the markdown report templates (<label>_report.md).",
    )
    parser.add_argument(
        "--reports-output-dir",
        type=Path,
        default=PROJECT_ROOT / "filled_templates",
        help="Directory where filled reports are saved (<label>/report.md subfolders are created inside).",
    )
