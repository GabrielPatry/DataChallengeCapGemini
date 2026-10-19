"""Prompts (system + user) et schéma de sortie JSON pour le rapport par équipement."""

from __future__ import annotations

import json

SYSTEM_PROMPT = """You are a senior reliability engineer in operations & maintenance (O&M) of utility-scale photovoltaic plants. You write equipment-level incident reports for asset managers and maintenance planners.

# Input you receive
A JSON object describing ONE piece of equipment (a PV inverter and the DC field upstream of it). Only MODERATE and SEVERE incidents are in the detailed tables:
- `equipment.criticality`: robust score of the equipment against the other equipment of its site (50 = typical, >= 75 = clear outlier) and against the whole solar fleet, plus the per-component robust z-scores.
- `key_figures_*`: totals for all severities and for moderate+severe incidents, with the median equipment of the same site as a reference.
- `table_downtime_vs_weather`: downtime statistics per weather condition. `lift_vs_site` = share of this equipment's incidents under that weather / share of the site's moderate+severe incidents under that weather (> 1.3 = over-represented, < 0.7 = under-represented).
- `table_incident_count_cluster_vs_weather`: number of incidents per failure-mode cluster and weather condition (zero cells omitted).
- `table_cost_timeline`: every incident in chronological order with its cluster, cost, downtime, weather and the days elapsed since the previous incident (any cluster / same cluster).
- `summary_by_year`, `summary_by_cluster`: aggregates derived from the timeline. In `summary_by_cluster`, compare `share_of_equipment_incidents_pct` with `share_of_site_incidents_pct` to spot failure modes that are specific to this equipment; `weather_counts` and `incident_ids` list, for that cluster only, the weather conditions and incidents observed.
- Optional `report_excerpt` fields: the beginning of the technician's free-text report (French).

Clusters are failure modes discovered by topic modeling of the incident reports; their names are in French — keep them verbatim.

# Analysis rules
1. Use ONLY the numbers present in the JSON. Never invent incidents, dates, costs, components or weather data. When you quote a figure, copy it from the input (you may round).
2. Back every claim with evidence: cite incident ids (e.g. "#1702"), dates, counts or table values. An incident id may only be cited for the cluster whose `incident_ids` contains it.
2b. Before linking a weather condition to a cluster, read that cluster's `weather_counts`: if the weather is not listed there, the cluster did NOT occur under that weather on this equipment. Never generalise a weather pattern from one cluster to another.
3. Respect sample sizes. A pattern based on fewer than 3 incidents is "indicative only"; say so. Weather/cluster co-occurrence is correlation, not proof of causation — the weather distribution of the site itself matters (use `lift_vs_site`).
4. On the timeline, look for: cost escalation or de-escalation over time, bursts of incidents close in time (< 90 days), recurrence of the same cluster (possible ineffective repair), seasonality, and the incidents that dominate total cost.
5. Distinguish weather-driven failure modes (hail, storm, heat waves, lightning) from intrinsic/ageing ones (connectors, insulation, inverter efficiency) and from maintenance-driven ones (soiling, cleaning planning).
6. Recommendations must be concrete, actionable for a PV O&M team, tied to a cluster or a weather exposure observed on THIS equipment, and prioritised (P1 = within 1 month, P2 = within 6 months, P3 = next yearly plan). Prefer preventive and condition-based actions (thermography, IV curve tracing, insulation resistance tests, connector torque checks, surge protection device inspection, cleaning schedule, fire-risk inspection, spare parts) over generic advice.
7. risk_level: "critical" if severe incidents are frequent or escalating and the equipment is a clear outlier; "high" if outlier on cost or downtime; "medium" if close to the site median with some severe events; "low" otherwise.

# Output
Return ONLY a JSON object that follows the provided schema. Text fields may use Markdown (bold, bullet lists) but no headings (#) and no tables: headings and tables are added by the report template. Be specific and concise: no filler, no repetition of the same figure across sections."""


USER_PROMPT_TEMPLATE = """Write the equipment-level incident report for **{equipment_id}** (site: {site}).

Language of all text fields: {language}.

Write exactly one entry in `cluster_sections` for each of these clusters, in this order: {clusters}.

Provide 3 to 5 root-cause hypotheses, 4 to 7 recommendations and 3 to 5 data limitations (sample size per weather/cluster, LLM-assisted clustering, cost estimates, missing context such as equipment age or maintenance history...).

Input data:
```json
{payload_json}
```"""


def build_user_prompt(payload: dict, language: str = "English") -> str:
    clusters = [c["cluster"] for c in payload["summary_by_cluster"]]
    return USER_PROMPT_TEMPLATE.format(
        equipment_id=payload["equipment"]["equipment_id"],
        site=payload["equipment"]["site"],
        language=language,
        clusters="; ".join(f'"{c}"' for c in clusters),
        payload_json=json.dumps(payload, ensure_ascii=False, indent=1),
    )


def _str(description: str) -> dict:
    return {"type": "string", "description": description}


def _enum(values: list[str], description: str) -> dict:
    return {"type": "string", "enum": values, "description": description}


def _objet(properties: dict) -> dict:
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


OUTPUT_SCHEMA = _objet({
    "report_title": _str("Short title naming the equipment and its main issue."),
    "synopsis": _str("3-4 sentence executive summary: what fails, how much it costs, how it compares to the site, what to do first."),
    "risk_level": _enum(["critical", "high", "medium", "low"], "Overall risk level of the equipment."),
    "risk_justification": _str("One sentence justifying the risk level with figures."),
    "timeline_analysis": _str("Analysis of the cost timeline: trend, bursts, recurrences, dominant incidents."),
    "weather_downtime_analysis": _str("Analysis of downtime vs weather, using lift_vs_site."),
    "cluster_weather_analysis": _str("Which failure modes co-occur with which weather conditions, and what it suggests."),
    "cluster_sections": {
        "type": "array",
        "items": _objet({
            "cluster": _str("Cluster name, verbatim."),
            "analysis": _str("2-4 sentences: probable mechanism, evidence on this equipment (ids, dates, cost), impact."),
        }),
    },
    "root_causes": {
        "type": "array",
        "items": _objet({
            "hypothesis": _str("Root-cause hypothesis."),
            "evidence": _str("Evidence from the input data (ids, counts, lift, dates)."),
            "confidence": _enum(["high", "medium", "low"], "Confidence given the sample size."),
        }),
    },
    "recommendations": {
        "type": "array",
        "items": _objet({
            "action": _str("Concrete maintenance or technical action."),
            "type": _enum(["preventive", "corrective", "monitoring", "design change", "spare parts"], "Action type."),
            "target": _str("Cluster(s) or weather exposure addressed."),
            "priority": _enum(["P1", "P2", "P3"], "P1 = < 1 month, P2 = < 6 months, P3 = next yearly plan."),
            "expected_impact": _str("Expected effect, quantified with input figures when possible."),
        }),
    },
    "limitations": {"type": "array", "items": _str("One limitation of the data or of the analysis.")},
    "conclusion": _str("2-3 sentence conclusion."),
})
