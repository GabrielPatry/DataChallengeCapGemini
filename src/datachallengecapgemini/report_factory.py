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
import hashlib
import json
import os
import re
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import pandas as pd

from datachallengecapgemini.equipment_stats import (
    PRIORITY_RULES,
    RECURRENCE_DAYS,
    SAMPLE_THRESHOLD,
    SEQUENCE_DAYS,
    format_eur,
)

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


# ===========================================================================
# Equipment-level reports — one Azure OpenAI agent per report section
# ===========================================================================
#
# For every equipment of a site (see ``run_equipment_reporting``):
#   1. ``plot_factory.run_equipment_plotting`` has written figures/*.png,
#      json/<figure>.json (the data of each figure) and json/stats.json;
#   2. each ``section_*`` function picks the statistics and figure data of
#      its section, asks its own specialised agent (system prompt = role +
#      shared rules; user prompt = section, questions, data) and renders the
#      section markdown, saved as sections/<name>.md;
#   3. the sections are assembled into report.md with
#      templates/equipment_report.md.
# The agents never calculate: every number comes from json/, and the
# priorities, risk level and confidence levels are decided in Python.

EQUIPMENT_TEMPLATE_NAME = "equipment_report.md"
INCIDENT_REF_PATTERN = re.compile(r"#(\d+)\b")
# Numbers written in text: "49 142", "207,762", "1.33", "2023" (signs ignored)
NUMBER_PATTERN = re.compile(r"\d{1,3}(?:[ ,  ]\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")
DRY_RUN_TEXT = "*[dry run — text not generated]*"
# Confidence of a root-cause hypothesis, from its number of supporting incidents
CONFIDENCE_HIGH_MIN_INCIDENTS = 5
# Public pay-as-you-go GPT-4.1 nano rates (USD per 1M tokens), for the
# estimate printed at the end of a run — see README
USD_PER_M_INPUT_TOKENS = 0.10
USD_PER_M_OUTPUT_TOKENS = 0.40

SHARED_RULES = """You write one section of an equipment-level incident report for asset managers and maintenance planners of utility-scale photovoltaic plants. The equipment is a PV inverter and the DC field upstream of it.

# Rules
1. NO CALCULATIONS. Do not add, subtract, average, compare numerically, compute percentages, ratios, durations or date differences. Every number you write must be copied from the input (rounding allowed). If a figure you would like to quote is not in the input, make the point without a number.
2. `facts` are verified, ready-made sentences: when you quote one of their figures, copy it exactly with the meaning given there (e.g. do not swap "most costly incident" and "most costly failure mode", or the ratio of one indicator for another).
3. Refer to incidents ONLY by their local number as written in the input (e.g. "#3"). Cite an incident for a failure mode only if it is listed among that failure mode's incidents.
4. Before linking a weather condition to a failure mode, check that failure mode's weather counts: if the weather is not listed, the failure mode never occurred under it. Never generalise a weather pattern from one failure mode to another. Weather co-occurrence is a correlation, not a proof.
5. When an entry is flagged "indicative only", say so briefly in the same sentence (e.g. "indicative, 2 incidents"). Never write a separate paragraph about data limitations.
6. Priorities and risk levels are given: never change or re-derive them.
7. No mention of datasets, files, score formulas, algorithms, clustering or AI. Say "failure mode", not "cluster". Failure-mode and weather names are in French: keep them verbatim.
8. Answer only the questions of your section; other specialists write the other sections.

# Output
Return ONLY a JSON object following the provided schema. Text fields may use Markdown emphasis and bullet lists, but no headings and no tables. Be specific and concise."""

SECTION_PROMPT_TEMPLATE = """You are writing the section "{title}" of the incident report of equipment {equipment_id} (site: {site}).

Language of every text field: {language}.

Answer these questions:
{questions}

Statistics and figure data for this section (every value is already computed):
```json
{data}
```"""


# ---------------------------------------------------------------------------
# Azure OpenAI
# ---------------------------------------------------------------------------


def get_azure_client():
    """Azure OpenAI client and chat deployment name, from the ``.env`` file."""
    try:
        # Corporate networks with SSL inspection (see the starter notebook)
        import truststore

        truststore.inject_into_ssl()
    except ImportError:
        pass
    from dotenv import load_dotenv
    from openai import AzureOpenAI

    load_dotenv(PROJECT_ROOT / ".env", override=True)
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    )
    return client, os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]


def call_azure(
    client,
    deployment: str,
    system_prompt: str,
    user_prompt: str,
    schema: dict,
    schema_name: str,
    max_attempts: int = 6,
) -> tuple[dict, dict]:
    """One chat completion with structured JSON output; returns (answer, token usage).

    Uses ``json_schema`` (strict) and falls back to ``json_object`` if the
    deployment refuses it. Waits and retries on rate limits (HTTP 429).
    """
    from openai import BadRequestError, RateLimitError

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    formats = [
        {
            "type": "json_schema",
            "json_schema": {"name": schema_name, "strict": True, "schema": schema},
        },
        {"type": "json_object"},
    ]
    for response_format in formats:
        if response_format["type"] == "json_object":
            messages = [
                *messages,
                {
                    "role": "user",
                    "content": "Return the JSON object following this schema:\n"
                    + json.dumps(schema),
                },
            ]
        for attempt in range(1, max_attempts + 1):
            try:
                response = client.with_options(max_retries=0).chat.completions.create(
                    model=deployment,
                    messages=messages,
                    response_format=response_format,
                    temperature=0.2,
                    max_tokens=4000,
                )
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                }
                return json.loads(response.choices[0].message.content), usage
            except RateLimitError as error:
                if attempt == max_attempts:
                    raise
                match = re.search(r"retry after (\d+) seconds", str(error))
                wait = int(match.group(1)) + 1 if match else 30
                print(f"  rate limit reached (429), retrying in {wait} s")
                time.sleep(wait)
            except BadRequestError as error:
                if response_format["type"] != "json_schema":
                    raise
                print(
                    f"  json_schema refused ({error.message[:120]}), falling back to json_object"
                )
                break
    raise RuntimeError("No answer from Azure OpenAI")


# ---------------------------------------------------------------------------
# Output schemas and markdown helpers
# ---------------------------------------------------------------------------


def _text(description: str) -> dict:
    return {"type": "string", "description": description}


def _choice(values: list[str], description: str) -> dict:
    return {"type": "string", "enum": values, "description": description}


def _list(items: dict, description: str) -> dict:
    return {"type": "array", "items": items, "description": description}


def _object(properties: dict) -> dict:
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def _placeholder(schema: dict):
    """Answer with the shape of *schema*, used in dry runs (no Azure call)."""
    if schema["type"] == "object":
        return {key: _placeholder(value) for key, value in schema["properties"].items()}
    if schema["type"] == "array":
        return []
    return schema["enum"][0] if "enum" in schema else DRY_RUN_TEXT


def _md_table(rows: list[dict], columns: dict[str, str]) -> str:
    """Markdown table of *rows*, with *columns* mapping row keys to headers."""
    lines = [
        "| " + " | ".join(columns.values()) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = ("" if row.get(key) is None else str(row[key]) for key in columns)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def _numbers_in_text(text: str) -> list[str]:
    """Numbers written in *text*, incident numbers (#k) and priorities (P1) excluded."""
    text = re.sub(r"#\d+|\b[Pp]\d\b", " ", text)
    return [re.sub(r"[ ,  ]", "", n) for n in NUMBER_PATTERN.findall(text)]


def _numbers_in_data(data) -> set[float]:
    """Every number of a JSON-like value, including numbers written inside its strings."""
    if isinstance(data, dict):
        return set().union(
            *(_numbers_in_data(v) for v in (*data.keys(), *data.values()))
        )
    if isinstance(data, list):
        return set().union(*(_numbers_in_data(v) for v in data)) if data else set()
    if isinstance(data, bool) or data is None:
        return set()
    if isinstance(data, int | float):
        return {abs(float(data))}
    return {float(n) for n in _numbers_in_text(str(data))}


def _strings(answer) -> list[str]:
    if isinstance(answer, dict):
        return [s for v in answer.values() for s in _strings(v)]
    if isinstance(answer, list):
        return [s for v in answer for s in _strings(v)]
    return [answer] if isinstance(answer, str) else []


def _invented_numbers(answer: dict, data: dict) -> list[str]:
    """Numbers of *answer* that are not a rounding of any number of *data*."""
    known = _numbers_in_data(data)
    invented = []
    for text in _strings(answer):
        for number in _numbers_in_text(text):
            decimals = len(number.split(".")[1]) if "." in number else 0
            tolerance = 0.5 * 10**-decimals + 1e-9
            if not any(abs(float(number) - value) <= tolerance for value in known):
                invented.append(number)
    return sorted(set(invented), key=float)


def _wrong_refs(text: str, allowed: list[str]) -> list[str]:
    """Incident numbers cited in *text* that are not in *allowed*."""
    cited = {f"#{n}" for n in INCIDENT_REF_PATTERN.findall(text)}
    return sorted(cited - set(allowed), key=lambda ref: int(ref[1:]))


def _figure(name: str, alt: str) -> str:
    """Image link relative to sections/ (rewritten for report.md on assembly)."""
    return f"![{alt}](../figures/{name}.png)"


# ---------------------------------------------------------------------------
# Section context — what every section agent shares
# ---------------------------------------------------------------------------


@dataclass
class SectionContext:
    """Inputs of one equipment report and the answers collected so far.

    ``ask`` runs one section agent. Answers are cached in
    ``sections/<section>.llm.json`` together with a hash of the prompt: an
    agent is called again only if its prompt changed or if the section is in
    ``forced``.
    """

    equipment_id: str
    stats: dict
    figures: dict[str, dict]
    sections_dir: Path
    language: str = "English"
    client: object | None = None
    deployment: str | None = None
    dry_run: bool = False
    forced: set[str] = field(default_factory=set)
    answers: dict[str, dict] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    usage: dict[str, int] = field(
        default_factory=lambda: {"prompt_tokens": 0, "completion_tokens": 0}
    )

    @property
    def site(self) -> str:
        return self.stats["equipment"]["site"]

    @property
    def facts(self) -> dict[str, list[str]]:
        return self.stats["facts"]

    @property
    def failure_modes(self) -> list[dict]:
        return self.stats["failure_modes"]

    @property
    def refs(self) -> list[str]:
        return [incident["ref"] for incident in self.stats["register"]]

    def ask(
        self,
        section: str,
        title: str,
        role: str,
        questions: list[str],
        data: dict,
        schema: dict,
        check: Callable[[dict], list[str]] | None = None,
    ) -> dict:
        """Run the agent of *section* and return its JSON answer.

        The answer is checked for numbers absent from *data* and with
        *check* (section-specific problems, e.g. a P1 failure mode without
        action). If there is a problem, the agent gets one correction round;
        problems left afterwards are recorded in ``warnings``.
        """

        def problems_of(answer: dict) -> list[str]:
            problems = list(check(answer)) if check and not self.dry_run else []
            unknown = _wrong_refs(" ".join(_strings(answer)), self.refs)
            if unknown:
                problems.append(
                    f"incident numbers that do not exist on this equipment: {', '.join(unknown)}"
                )
            invented = _invented_numbers(answer, data)
            if invented:
                problems.append(
                    f"numbers not found in the input: {', '.join(invented)} — copy every "
                    "number exactly from the input, or make the point without a number"
                )
            return problems

        system_prompt = f"You are {role}\n\n{SHARED_RULES}"
        user_prompt = SECTION_PROMPT_TEMPLATE.format(
            title=title,
            equipment_id=self.equipment_id,
            site=self.site,
            language=self.language,
            questions="\n".join(f"{i}. {q}" for i, q in enumerate(questions, 1)),
            data=json.dumps(data, ensure_ascii=False, indent=1),
        )
        (self.sections_dir / f"{section}.prompt.md").write_text(
            f"# System\n\n{system_prompt}\n\n# User\n\n{user_prompt}\n",
            encoding="utf-8",
        )
        prompt_hash = hashlib.sha256(
            (system_prompt + user_prompt + json.dumps(schema)).encode("utf-8")
        ).hexdigest()

        cache_path = self.sections_dir / f"{section}.llm.json"
        cached = (
            json.loads(cache_path.read_text(encoding="utf-8"))
            if cache_path.exists()
            else None
        )
        if (
            cached
            and cached["prompt_sha256"] == prompt_hash
            and section not in self.forced
        ):
            answer = cached["answer"]
        elif self.dry_run:
            answer = _placeholder(schema)
        else:
            print(f"  {section}: asking Azure OpenAI")
            answer, usage = call_azure(
                self.client,
                self.deployment,
                system_prompt,
                user_prompt,
                schema,
                section,
            )
            problems = problems_of(answer)
            if problems:
                # One correction round, telling the agent what was wrong
                print(f"  {section}: {'; '.join(problems)} — asking again")
                correction = (
                    f"{user_prompt}\n\nA previous answer to this request had these problems, "
                    "fix them:\n" + "\n".join(f"- {p}" for p in problems)
                )
                answer, retry_usage = call_azure(
                    self.client,
                    self.deployment,
                    system_prompt,
                    correction,
                    schema,
                    section,
                )
                usage = {key: usage[key] + retry_usage[key] for key in usage}
            for key in self.usage:
                self.usage[key] += usage[key]
            cache_path.write_text(
                json.dumps(
                    {"prompt_sha256": prompt_hash, "usage": usage, "answer": answer},
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        self.warnings.extend(f"{section}: {problem}" for problem in problems_of(answer))
        self.answers[section] = answer
        return answer


# ---------------------------------------------------------------------------
# One function per report section
# ---------------------------------------------------------------------------


def section_key_figures(ctx: SectionContext) -> str:
    """1. Key figures — tables computed in Python + a benchmarking agent's reading."""
    equipment = ctx.stats["equipment"]
    comparison = ctx.stats["comparison_with_site_median"]
    key = ctx.stats["key_figures"]
    answer = ctx.ask(
        "key_figures",
        "1. Key figures",
        role="an asset-performance analyst who benchmarks PV inverters against the other inverters of their site.",
        questions=[
            (
                "On which indicators does this equipment stand out from the median equipment of its "
                "site, and on which is it in line? Quote the ratios as written in `facts`."
            ),
            (
                "Why was this equipment selected (`why_selected`) and what does its priority mean for "
                "the reader?"
            ),
            "How concentrated is the cost on severe incidents?",
        ],
        data={
            "equipment": equipment,
            "comparison_with_site_median_equipment": comparison,
            "key_figures_moderate_and_severe": key,
            "facts": ctx.facts["benchmark"] + ctx.facts["cost"][:1],
        },
        schema=_object({"reading": _text("2-4 sentences answering the questions.")}),
    )

    def row(label: str, block: dict, unit: str = "", money: bool = False) -> dict:
        fmt = format_eur if money else str
        return {
            "label": label,
            "this": f"{fmt(block['this_equipment'])}{unit}",
            "median": f"{fmt(block['site_median_equipment'])}{unit}",
            "ratio": f"×{block['ratio_to_site_median']}",
        }

    benchmark = _md_table(
        [
            row("Incidents (all severities)", comparison["incidents_all_severities"]),
            row("Severe incidents", comparison["severe_incidents"]),
            row(
                "Total estimated cost (all severities)",
                comparison["cost_all_severities_eur"],
                " EUR",
                True,
            ),
            row(
                "Total downtime (all severities)",
                comparison["downtime_all_severities_h"],
                " h",
            ),
        ],
        {
            "label": "Indicator",
            "this": "This equipment",
            "median": "Median equipment of the site",
            "ratio": "Ratio",
        },
    )
    top_mode = ctx.failure_modes[0]
    top_weather = ctx.figures["downtime_weather"]["rows"][0]
    period = ctx.stats["period"]
    scope = _md_table(
        [
            {
                "label": "Incidents analysed",
                "value": f"{key['n_incidents']} ({key['n_moderate']} moderate · {key['n_severe']} severe)",
            },
            {
                "label": "Period covered",
                "value": f"{period['first_record']} → {period['last_record']}",
            },
            {
                "label": "Total estimated cost",
                "value": f"{format_eur(key['cost_total_eur'])} EUR "
                f"({key['severe_share_of_cost_pct']} % from severe incidents)",
            },
            {
                "label": "Average cost per incident",
                "value": f"{format_eur(key['cost_mean_eur'])} EUR",
            },
            {"label": "Total downtime", "value": f"{key['downtime_total_h']} h"},
            {
                "label": "Average interval between incidents",
                "value": f"{key['mean_days_between_incidents']} days",
            },
            {
                "label": "Most costly failure mode",
                "value": f"{top_mode['failure_mode']} ({format_eur(top_mode['cost_total_eur'])} EUR)",
            },
            {
                "label": "Weather with most downtime",
                "value": f"{top_weather['weather_condition']} ({top_weather['downtime_total_h']} h)",
            },
        ],
        {
            "label": "Moderate and severe incidents (scope of this report)",
            "value": "Value",
        },
    )
    return "\n\n".join(["## 1. Key figures", benchmark, scope, answer["reading"]])


def section_methodology(ctx: SectionContext) -> str:
    """2. How this report was built — fixed text, no agent.

    The rules described here (selection, priorities, confidence) must match
    the code exactly, so this section is not rewritten by a model.
    """
    equipment = ctx.stats["equipment"]
    period = ctx.stats["period"]
    priority = equipment["equipment_priority"]
    outcome = (
        f"**{priority}**"
        if priority in ("P1", "P2")
        else "not flagged as critical (included on request)"
    )
    paragraphs = [
        "## 2. How this report was built",
        (
            f"**Scope.** This report covers the maintenance incidents recorded on "
            f"{equipment['equipment_id']} between {period['first_record']} and {period['last_record']}. "
            "Each incident report was read and assigned to a *failure mode* according to its "
            "description. The detailed analysis focuses on moderate and severe incidents; minor "
            "incidents only appear in the comparison with the site. Incidents are numbered #1, #2, … "
            "in chronological order for this equipment (see the annex)."
        ),
        (
            "**Why this equipment.** Each piece of equipment receives a criticality score from 0 to "
            "100 that combines four indicators: number of incidents, number of severe incidents "
            "(counted twice), total repair cost and total downtime. The score is computed twice: "
            "against the other equipment of the same site and against all solar equipment of the "
            "fleet. 50 corresponds to a typical piece of equipment, 75 or more to one clearly above "
            "the others. Equipment scoring 75 or more on both comparisons is priority **P1**, on one "
            f"of them priority **P2**. Here: {equipment['why_selected']} → {outcome}."
        ),
        "**Recommendation priority.** Each recommendation addresses one failure mode and inherits "
        "its priority:\n"
        + "\n".join(f"- **{p}** — {rule}" for p, rule in PRIORITY_RULES.items()),
        (
            "**Root-cause confidence.** The confidence of a root-cause hypothesis reflects the number "
            f"of incidents supporting it: high from {CONFIDENCE_HIGH_MIN_INCIDENTS} incidents, medium "
            f"from {SAMPLE_THRESHOLD}, low below."
        ),
        (
            "**Analysis.** All figures, tables and charts are computed directly from the incident "
            f"records (a *close sequence* is a series of incidents less than {SEQUENCE_DAYS} days "
            f"apart; a *recurrence* is the same failure mode coming back within {RECURRENCE_DAYS} "
            "days). The commentary of each section was drafted with the help of an AI assistant "
            "specialised in that topic, from the figures of the section only."
        ),
        f"*Patterns based on fewer than {SAMPLE_THRESHOLD} incidents are flagged as indicative in the text.*",
    ]
    return "\n\n".join(paragraphs)


def section_cost_timeline(ctx: SectionContext) -> str:
    """3. Cost timeline — trend, dominant incidents, sequences and seasonality."""
    stats = ctx.stats
    answer = ctx.ask(
        "cost_timeline",
        "3. Cost timeline",
        role="a reliability engineer who analyses the cost history and recurrence of incidents on PV inverters.",
        questions=[
            (
                "How did the number of incidents and their cost evolve year by year? Comment on every "
                "year, including the change in the last year, using the year-on-year changes given."
            ),
            "Which incidents dominate the cost (`most_costly_incidents`) and what are their failure modes?",
            (
                "Are there close sequences of incidents or quick recurrences of the same failure mode? "
                "Name the incidents and failure modes involved."
            ),
            "Is there a seasonal pattern? Flag seasons with few incidents as indicative.",
        ],
        data={
            "cost_timeline_figure": ctx.figures["cost_timeline"],
            "yearly_trend": stats["yearly_trend"],
            "seasonality": stats["seasonality"],
            "most_costly_incidents": stats["most_costly_incidents"],
            f"close_sequences_within_{SEQUENCE_DAYS}_days": stats[
                f"close_sequences_within_{SEQUENCE_DAYS}_days"
            ],
            "facts": ctx.facts["trend"] + ctx.facts["cost"][1:],
        },
        schema=_object(
            {
                "trend": _text("Answer to question 1 (2-4 sentences)."),
                "dominant_incidents": _text("Answer to question 2 (1-3 sentences)."),
                "sequences_and_recurrences": _text(
                    "Answer to question 3 (1-3 sentences)."
                ),
                "seasonality": _text("Answer to question 4 (1-2 sentences)."),
            }
        ),
    )

    years = [
        {
            **year,
            "cost": format_eur(year["cost_eur"]),
            "change": ""
            if year["cost_change_vs_previous_year_pct"] is None
            else f"{year['cost_change_vs_previous_year_pct']:+} %",
        }
        for year in stats["yearly_trend"]["by_year"]
    ]
    yearly_table = _md_table(
        years,
        {
            "year": "Year",
            "n_incidents": "Incidents",
            "n_severe": "Severe",
            "cost": "Cost (EUR)",
            "change": "Cost vs previous year",
            "downtime_h": "Downtime (h)",
        },
    )
    return "\n\n".join(
        [
            "## 3. Cost timeline",
            _figure("cost_timeline", "Cost timeline"),
            (
                "*Estimated cost of each moderate (hollow) and severe (filled) incident. Colour = family of "
                "failure modes, marker shape = failure mode; the three most costly incidents are labelled.*"
            ),
            yearly_table,
            f"**Trend.** {answer['trend']}",
            f"**Dominant incidents.** {answer['dominant_incidents']}",
            f"**Sequences and recurrences.** {answer['sequences_and_recurrences']}",
            f"**Seasonality.** {answer['seasonality']}",
        ]
    )


def section_weather(ctx: SectionContext) -> str:
    """4. Weather exposure — downtime vs weather and failure modes vs weather."""
    downtime = ctx.figures["downtime_weather"]
    answer = ctx.ask(
        "weather",
        "4. Weather exposure",
        role="an engineer specialised in the weather and environmental exposure of PV plants.",
        questions=[
            (
                "Under which weather conditions does this equipment lose the most hours? Are these "
                "conditions over- or under-represented compared with the rest of the site "
                "(`representation`)?"
            ),
            (
                "Which failure modes occur under which weather conditions? Read each row of the "
                "matrix: link a weather condition to a failure mode only if it appears in that row. "
                "What does it imply for operations (e.g. inspections after a given weather event)?"
            ),
        ],
        data={
            "downtime_vs_weather_figure": downtime,
            "failure_modes_vs_weather_figure": ctx.figures["cluster_weather"],
            "facts": ctx.facts["weather"],
        },
        schema=_object(
            {
                "downtime_vs_weather": _text("Answer to question 1 (2-4 sentences)."),
                "failure_modes_vs_weather": _text(
                    "Answer to question 2 (2-4 sentences)."
                ),
            }
        ),
    )

    table = _md_table(
        downtime["rows"],
        {
            "weather_condition": "Weather",
            "n_incidents": "Incidents",
            "n_severe": "Severe",
            "downtime_total_h": "Downtime (h)",
            "downtime_median_h": "Median (h)",
            "share_of_equipment_downtime_pct": "% of downtime",
            "representation": "Compared with site",
        },
    )
    return "\n\n".join(
        [
            "## 4. Weather exposure",
            "### 4.1 Downtime vs weather condition",
            _figure("downtime_weather", "Downtime vs weather"),
            "*Downtime of each incident per weather condition; the black tick is the median.*",
            table,
            answer["downtime_vs_weather"],
            "### 4.2 Failure modes vs weather condition",
            _figure("cluster_weather", "Failure modes vs weather"),
            "*Number of incidents per failure mode and weather condition.*",
            answer["failure_modes_vs_weather"],
        ]
    )


def section_failure_modes(ctx: SectionContext) -> str:
    """5. Failure modes — summary table + one paragraph per failure mode."""
    modes = ctx.failure_modes
    names = [mode["failure_mode"] for mode in modes]
    refs_by_mode = {
        mode["failure_mode"]: [i["ref"] for i in mode["incidents"]] for mode in modes
    }

    def check(answer: dict) -> list[str]:
        problems = []
        missing = [
            n
            for n in names
            if n not in {e["failure_mode"] for e in answer["failure_modes"]}
        ]
        if missing:
            problems.append(f"no entry for failure mode(s): {'; '.join(missing)}")
        for entry in answer["failure_modes"]:
            text = entry["mechanism"] + " " + entry["evidence_and_impact"]
            wrong = _wrong_refs(text, refs_by_mode[entry["failure_mode"]])
            if wrong:
                problems.append(
                    f"{', '.join(wrong)} cited for {entry['failure_mode']}, which they do not belong to"
                )
        return problems

    answer = ctx.ask(
        "failure_modes",
        "5. Failure modes",
        role="a PV failure-analysis expert (inverters, DC cabling, junction boxes, modules, fire risk).",
        questions=[
            "For each failure mode, in this order: "
            + "; ".join(f'"{n}"' for n in names)
            + ", give "
            "(a) its probable physical mechanism on a PV inverter and its DC field, and "
            "(b) the evidence on this equipment — incidents (only from that failure mode's "
            "`incidents`), dates, severity, cost, recurrences — and its impact.",
        ],
        data={"failure_modes": modes, "facts": ctx.facts["priorities"]},
        schema=_object(
            {
                "failure_modes": _list(
                    _object(
                        {
                            "failure_mode": _choice(
                                names, "Failure mode name, verbatim."
                            ),
                            "mechanism": _text(
                                "Probable physical mechanism (1-2 sentences)."
                            ),
                            "evidence_and_impact": _text(
                                "Evidence on this equipment and impact (1-3 sentences)."
                            ),
                        }
                    ),
                    "Exactly one entry per failure mode.",
                ),
            }
        ),
        check=check,
    )
    by_name = {entry["failure_mode"]: entry for entry in answer["failure_modes"]}

    table = _md_table(
        [
            {
                **mode,
                "cost": format_eur(mode["cost_total_eur"]),
                "refs": ", ".join(i["ref"] for i in mode["incidents"]),
            }
            for mode in modes
        ],
        {
            "failure_mode": "Failure mode",
            "recommendation_priority": "Priority",
            "n_incidents": "Incidents",
            "n_severe": "Severe",
            "cost": "Cost (EUR)",
            "cost_share_pct": "% of cost",
            f"recurrences_within_{RECURRENCE_DAYS}_days": f"Recurrences < {RECURRENCE_DAYS} d",
            "refs": "Incidents #",
        },
    )
    parts = ["## 5. Failure modes", table]
    for mode in modes:
        name = mode["failure_mode"]
        parts.append(f"### {name} · {mode['recommendation_priority']}")
        entry = by_name.get(name)
        if entry is None:
            parts.append("*No commentary generated.*")
            continue
        parts.append(f"{entry['mechanism']} {entry['evidence_and_impact']}")
    return "\n\n".join(parts)


def section_root_causes(ctx: SectionContext) -> str:
    """6. Root-cause hypotheses — confidence computed from the supporting incidents."""
    modes = ctx.failure_modes
    names = [mode["failure_mode"] for mode in modes]
    refs_by_mode = {
        mode["failure_mode"]: [i["ref"] for i in mode["incidents"]] for mode in modes
    }

    def allowed_refs(hypothesis: dict) -> set[str]:
        return {
            ref for name in hypothesis["failure_modes"] for ref in refs_by_mode[name]
        }

    def check(answer: dict) -> list[str]:
        problems = []
        for i, hypothesis in enumerate(answer["hypotheses"], 1):
            text = " ".join(
                [*hypothesis["supporting_incidents"], hypothesis["reasoning"]]
            )
            wrong = _wrong_refs(text, sorted(allowed_refs(hypothesis)))
            if wrong:
                problems.append(
                    f"hypothesis {i} cites {', '.join(wrong)}, which do not belong to its failure modes"
                )
        return problems

    answer = ctx.ask(
        "root_causes",
        "6. Root-cause hypotheses",
        role="a root-cause analysis (RCA) engineer for PV plants.",
        questions=[
            (
                "Propose 3 to 5 root-cause hypotheses explaining the incidents of this equipment. A "
                "hypothesis may cover one failure mode or a common cause behind several (e.g. heat "
                "stress, poor connections, lightning exposure)."
            ),
            (
                "For each hypothesis, list the failure modes it explains and the incidents supporting "
                "it — only incidents belonging to those failure modes."
            ),
            "Explain the reasoning in 1-3 sentences (mechanism, weather or timing patterns).",
        ],
        data={
            "failure_modes": [
                {
                    key: mode[key]
                    for key in (
                        "failure_mode",
                        "n_incidents",
                        "n_severe",
                        "sample",
                        "weather_counts",
                        "dominant_weather",
                        "median_days_between_recurrences",
                        f"recurrences_within_{RECURRENCE_DAYS}_days",
                        "incidents",
                    )
                }
                for mode in modes
            ],
            f"close_sequences_within_{SEQUENCE_DAYS}_days": ctx.stats[
                f"close_sequences_within_{SEQUENCE_DAYS}_days"
            ],
            "seasonality": ctx.stats["seasonality"],
            "facts": ctx.facts["weather"],
        },
        schema=_object(
            {
                "hypotheses": _list(
                    _object(
                        {
                            "hypothesis": _text(
                                "The root-cause hypothesis, in one sentence."
                            ),
                            "failure_modes": _list(
                                _choice(names, "Failure mode name."),
                                "Failure modes explained.",
                            ),
                            "supporting_incidents": _list(
                                _choice(ctx.refs, "Incident number."),
                                "Incidents supporting the hypothesis.",
                            ),
                            "reasoning": _text("Reasoning (1-3 sentences)."),
                        }
                    ),
                    "3 to 5 hypotheses.",
                ),
            }
        ),
        check=check,
    )

    items = []
    for i, hypothesis in enumerate(answer["hypotheses"], 1):
        # Incidents outside the hypothesis' failure modes never count as support
        support = sorted(
            set(hypothesis["supporting_incidents"]) & allowed_refs(hypothesis),
            key=lambda ref: int(ref[1:]),
        )
        if len(support) >= CONFIDENCE_HIGH_MIN_INCIDENTS:
            confidence = "high"
        elif len(support) >= SAMPLE_THRESHOLD:
            confidence = "medium"
        else:
            confidence = "low"
        items.append(
            f"{i}. **{hypothesis['hypothesis']}** — *confidence: {confidence} "
            f"({len(support)} supporting incident{'s' if len(support) != 1 else ''}"
            f"{': ' + ', '.join(support) if support else ''})*  \n"
            f"   Failure modes: {', '.join(hypothesis['failure_modes'])}.  \n"
            f"   {hypothesis['reasoning']}"
        )
    return "\n\n".join(
        ["## 6. Root-cause hypotheses", "\n".join(items) or DRY_RUN_TEXT]
    )


def section_recommendations(ctx: SectionContext) -> str:
    """7. Recommendations — each action inherits the priority of its failure mode."""
    modes = ctx.failure_modes
    names = [mode["failure_mode"] for mode in modes]
    priority_of = {
        mode["failure_mode"]: mode["recommendation_priority"] for mode in modes
    }
    p1 = [name for name in names if priority_of[name] == "P1"]
    coverage = (
        "Address every failure mode of priority P1 ("
        + "; ".join(f'"{n}"' for n in p1)
        + ") with at least one action."
        if p1
        else "Start with the failure modes of priority P2."
    )
    hypotheses = ctx.answers.get("root_causes", {}).get("hypotheses", [])

    def check(answer: dict) -> list[str]:
        missing = sorted(
            set(p1) - {a["target_failure_mode"] for a in answer["actions"]}
        )
        return (
            [f"no action for the P1 failure mode(s): {'; '.join(missing)}"]
            if missing
            else []
        )

    answer = ctx.ask(
        "recommendations",
        "7. Recommendations",
        role="an O&M maintenance planner for utility-scale PV plants.",
        questions=[
            (
                "Propose 4 to 7 concrete actions for the maintenance team, each addressing one failure "
                "mode of this equipment (thermography, IV-curve tracing, insulation resistance tests, "
                "connector torque checks, surge protection inspection, cleaning schedule, fire-risk "
                "inspection, spare parts…)."
            ),
            coverage,
            (
                "Use the root-cause hypotheses to choose the actions. For each action, state the "
                "expected impact qualitatively, citing only figures from the input."
            ),
        ],
        data={
            "failure_modes": [
                {
                    key: mode[key]
                    for key in (
                        "failure_mode",
                        "recommendation_priority",
                        "priority_reason",
                        "n_incidents",
                        "n_severe",
                        "cost_share_pct",
                        f"recurrences_within_{RECURRENCE_DAYS}_days",
                        "dominant_weather",
                    )
                }
                for mode in modes
            ],
            "root_cause_hypotheses": [
                {"hypothesis": h["hypothesis"], "failure_modes": h["failure_modes"]}
                for h in hypotheses
            ],
        },
        schema=_object(
            {
                "actions": _list(
                    _object(
                        {
                            "action": _text(
                                "Concrete maintenance or technical action."
                            ),
                            "type": _choice(
                                [
                                    "preventive",
                                    "corrective",
                                    "monitoring",
                                    "design change",
                                    "spare parts",
                                ],
                                "Action type.",
                            ),
                            "target_failure_mode": _choice(
                                names, "Failure mode addressed (sets the priority)."
                            ),
                            "expected_impact": _text("Expected effect (1 sentence)."),
                        }
                    ),
                    "4 to 7 actions.",
                ),
            }
        ),
        check=check,
    )
    actions = sorted(
        (
            {**a, "priority": priority_of[a["target_failure_mode"]]}
            for a in answer["actions"]
        ),
        key=lambda a: a["priority"],
    )
    ctx.answers["prioritised_actions"] = {"actions": actions}

    table = _md_table(
        actions,
        {
            "priority": "Priority",
            "action": "Action",
            "type": "Type",
            "target_failure_mode": "Failure mode addressed",
            "expected_impact": "Expected impact",
        },
    )
    return "\n\n".join(["## 7. Recommendations", table if actions else DRY_RUN_TEXT])


def _first_actions(ctx: SectionContext) -> list[dict]:
    """Actions to do first: the P1 ones, else the three highest-priority ones."""
    actions = ctx.answers.get("prioritised_actions", {}).get("actions", [])
    first = [a for a in actions if a["priority"] == "P1"] or actions[:3]
    return [
        {
            "priority": a["priority"],
            "action": a["action"],
            "failure_mode": a["target_failure_mode"],
        }
        for a in first
    ]


def section_conclusion(ctx: SectionContext) -> str:
    """8. Conclusion — written after the recommendations, which it refers to."""
    equipment = ctx.stats["equipment"]
    answer = ctx.ask(
        "conclusion",
        "8. Conclusion",
        role="the reliability manager who signs off equipment reports.",
        questions=[
            (
                "In 2-3 sentences: the main issue of this equipment, what to do first (the actions "
                "given) and the expected benefit."
            ),
        ],
        data={
            "equipment": {
                k: equipment[k]
                for k in ("equipment_id", "equipment_priority", "risk_level")
            },
            "facts": ctx.facts["cost"] + ctx.facts["benchmark"][:2],
            "failure_mode_priorities": ctx.facts["priorities"],
            "first_actions": _first_actions(ctx),
        },
        schema=_object({"conclusion": _text("2-3 sentence conclusion.")}),
    )
    return "\n\n".join(["## 8. Conclusion", answer["conclusion"]])


def section_summary(ctx: SectionContext) -> str:
    """Report header — title and executive summary, written once every other section is known."""
    equipment = ctx.stats["equipment"]
    answer = ctx.ask(
        "summary",
        "Title and executive summary",
        role="an executive-summary writer for asset managers of PV plants.",
        questions=[
            "Give the report a short title naming the equipment ID and its main failure modes.",
            (
                "Write a 3-4 sentence executive summary: what fails, how much it costs, how the "
                "equipment compares with its site and what to do first."
            ),
        ],
        data={
            "equipment": equipment,
            "facts": ctx.facts["benchmark"][:2]
            + ctx.facts["cost"]
            + ctx.facts["trend"][-1:],
            "failure_mode_priorities": ctx.facts["priorities"],
            "first_actions": _first_actions(ctx),
        },
        schema=_object(
            {
                "title": _text("Short report title naming the equipment."),
                "synopsis": _text("3-4 sentence executive summary."),
            }
        ),
    )
    title = (
        answer["title"]
        if answer["title"] != DRY_RUN_TEXT
        else f"Incident report — {ctx.equipment_id}"
    )
    priority = equipment["equipment_priority"]
    why = equipment["why_selected"]
    return "\n\n".join(
        [
            f"# {title}",
            (
                f"**Equipment:** {ctx.equipment_id} · **Site:** {ctx.site} · **Asset type:** PV inverter · "
                f"**Generated on:** {date.today().isoformat()}"
            ),
            f"> {answer['synopsis']}",
            (
                f"**Equipment priority: {priority} · Risk level: {equipment['risk_level'].upper()}** — "
                f"{why[0].upper()}{why[1:]}."
            ),
        ]
    )


def section_incident_register(ctx: SectionContext) -> str:
    """Annex — incident register, no agent."""
    rows = [{**r, "cost": format_eur(r["cost_eur"])} for r in ctx.stats["register"]]
    table = _md_table(
        rows,
        {
            "ref": "#",
            "date": "Date",
            "severity": "Severity",
            "failure_mode": "Failure mode",
            "cost": "Cost (EUR)",
            "downtime_h": "Downtime (h)",
            "weather_condition": "Weather",
        },
    )
    return f"### Annex — Incident register\n\n{table}"


# Generation order: the conclusion and the summary come after the sections
# they summarise. The order in the report is set by the template.
EQUIPMENT_SECTIONS: dict[str, Callable[[SectionContext], str]] = {
    "key_figures": section_key_figures,
    "methodology": section_methodology,
    "cost_timeline": section_cost_timeline,
    "weather": section_weather,
    "failure_modes": section_failure_modes,
    "root_causes": section_root_causes,
    "recommendations": section_recommendations,
    "conclusion": section_conclusion,
    "summary": section_summary,
    "incident_register": section_incident_register,
}


def run_equipment_reporting(
    equipment_ids: list[str],
    site_dir: Path,
    templates_dir: Path,
    language: str = "English",
    dry_run: bool = False,
    force: list[str] | None = None,
    pdf: bool = False,
) -> None:
    """Write the section markdowns and the assembled report of every equipment.

    Reads ``<site_dir>/<equipment_id>/json/`` (written by
    ``plot_factory.run_equipment_plotting``) and writes
    ``sections/<section>.md`` (plus the prompt and the cached answer of each
    agent) and ``report.md`` next to it.

    *force*: ``None`` reuses cached answers whose prompt did not change, an
    empty list regenerates every section, a list of names only those. With
    *dry_run*, no Azure call is made: the prompts are written and the text
    fields of the sections are placeholders.
    """
    template = (templates_dir / EQUIPMENT_TEMPLATE_NAME).read_text(encoding="utf-8")
    if force is None:
        forced: set[str] = set()
    else:
        unknown = sorted(set(force) - set(EQUIPMENT_SECTIONS))
        if unknown:
            raise ValueError(
                f"Unknown section(s) {', '.join(unknown)}; choose from {', '.join(EQUIPMENT_SECTIONS)}"
            )
        forced = set(force) or set(EQUIPMENT_SECTIONS)

    client, deployment = (None, None) if dry_run else get_azure_client()
    total = {"prompt_tokens": 0, "completion_tokens": 0}
    for equipment_id in equipment_ids:
        equipment_dir = site_dir / equipment_id
        json_dir = equipment_dir / "json"
        stats_path = json_dir / "stats.json"
        if not stats_path.exists():
            raise FileNotFoundError(
                f"{stats_path} not found — run the equipment plotting step first."
            )
        print(f"- {equipment_id}")
        figures = {
            path.stem: json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(json_dir.glob("*.json"))
            if path.stem != "stats"
        }
        sections_dir = equipment_dir / "sections"
        sections_dir.mkdir(parents=True, exist_ok=True)
        ctx = SectionContext(
            equipment_id=equipment_id,
            stats=json.loads(stats_path.read_text(encoding="utf-8")),
            figures=figures,
            sections_dir=sections_dir,
            language=language,
            client=client,
            deployment=deployment,
            dry_run=dry_run,
            forced=forced,
        )

        context: dict[str, str] = {}
        for name, build_section in EQUIPMENT_SECTIONS.items():
            markdown = build_section(ctx)
            (sections_dir / f"{name}.md").write_text(markdown + "\n", encoding="utf-8")
            context[f"section_{name}"] = markdown.replace("](../figures/", "](figures/")

        report_path = equipment_dir / "report.md"
        report_path.write_text(fill_template(template, context), encoding="utf-8")
        print(f"  Saved {report_path}")
        (sections_dir / "checks.txt").write_text(
            "\n".join(ctx.warnings) + "\n", encoding="utf-8"
        )
        for warning in ctx.warnings:
            print(f"  check: {warning}")
        for key in total:
            total[key] += ctx.usage[key]

        if pdf:
            from datachallengecapgemini.pdf_export import convert_markdown_to_pdf

            print(f"  Saved {convert_markdown_to_pdf(report_path)}")

    cost = (
        total["prompt_tokens"] * USD_PER_M_INPUT_TOKENS
        + total["completion_tokens"] * USD_PER_M_OUTPUT_TOKENS
    ) / 1e6
    print(
        f"Done. {total['prompt_tokens']} input + {total['completion_tokens']} output tokens "
        f"(estimated {cost:.4f} USD at GPT-4.1 nano rates). Reports are in {site_dir}"
    )


def add_equipment_report_arguments(parser: argparse.ArgumentParser) -> None:
    """Add equipment-report-specific arguments to *parser*."""
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=PROJECT_ROOT / "templates",
        help=f"Directory containing the {EQUIPMENT_TEMPLATE_NAME} template.",
    )
    parser.add_argument(
        "--language",
        default="English",
        help="Language of the generated text (headings and tables stay in English).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write figures, JSON, prompts and a report skeleton without calling Azure OpenAI.",
    )
    parser.add_argument(
        "--force",
        nargs="*",
        metavar="SECTION",
        choices=list(EQUIPMENT_SECTIONS),
        help="Call the agents again even if their prompt did not change: every section, "
        "or only the sections listed.",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Also convert each report to PDF with pandoc (see README).",
    )
