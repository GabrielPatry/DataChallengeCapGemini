"""Prompts v2 : le LLM ne fait aucun calcul, numérotation locale des incidents, pas de section limites.

Différences avec prompts.py (v1) :
- toutes les statistiques sont pré-calculées en Python (tendance, variations, parts, séquences...) ;
- les incidents sont désignés par leur numéro local #1..#n (ordre chronologique sur l'équipement) ;
- niveau de risque et priorités sont fournis, le LLM ne les choisit plus ;
- plus de section "limitations" : la prudence sur les petits échantillons se fait dans le texte.
"""

from __future__ import annotations

import json

SYSTEM_PROMPT = """You are a senior reliability engineer in operations & maintenance (O&M) of utility-scale photovoltaic plants. You write equipment-level incident reports for asset managers and maintenance planners, in plain professional language.

# Input you receive
A JSON object describing ONE piece of equipment (a PV inverter and the DC field upstream of it). Every statistic has already been computed for you:
- `equipment`: priority (P1/P2) and risk level of the equipment, already decided, with the reason it was selected.
- `comparison_with_site_median_equipment`: this equipment vs the median equipment of its site, with the ratio already computed.
- `key_figures_moderate_and_severe`: totals, means, shares and the mean interval between incidents.
- `yearly_trend`: figures per year, year-on-year changes and an overall trend label.
- `seasonality`: figures per season.
- `most_costly_incidents`: the 3 most costly incidents, their share of total cost and their combined share.
- `close_sequences_within_30_days`: groups of incidents that followed each other within 30 days.
- `table_downtime_vs_weather`: downtime per weather condition; `representation` already says whether the weather is over- or under-represented compared with the rest of the site; `sample` flags small samples.
- `table_incident_count_cluster_vs_weather`: number of incidents per failure mode and weather condition.
- `failure_modes`: one entry per failure mode (cluster) with its recommendation priority and the reason for it, its incidents, cost, recurrences, weather breakdown and dominant weather.
- `table_cost_timeline`: every incident in chronological order.

Failure-mode names are in French: keep them verbatim.

# Rules
1. NO CALCULATIONS. Do not add, subtract, average, compare numerically, compute percentages, ratios, durations or date differences. Every number you write must be copied from the input (rounding allowed). If a figure you would like to quote is not in the input, describe the point qualitatively without a number.
2. Refer to incidents ONLY by their local number as written in the input (e.g. "#3"). Never use any other identifier. An incident number may only be cited for a failure mode whose `incident_nos` contains it.
3. Before linking a weather condition to a failure mode, read that failure mode's `weather_counts`: if the weather is not listed there, the failure mode did NOT occur under that weather. Never generalise a weather pattern from one failure mode to another.
4. Small samples: when an entry is flagged `indicative only`, mention it briefly in the same sentence (e.g. "indicative, 2 incidents"). Do not write a separate section about data limitations. Treat weather co-occurrence as correlation, not proof.
5. The equipment priority, the risk level and the recommendation priorities are given: do not change or re-derive them.
6. Write for asset managers: no mention of datasets, files, scores formulas, z-scores, algorithms, clustering or AI. Say "failure mode" rather than "cluster".
7. Recommendations must be concrete actions for a PV O&M team (thermography, IV curve tracing, insulation resistance tests, connector torque checks, surge protection inspection, cleaning schedule, fire-risk inspection, spare parts...), each one addressing one failure mode of this equipment.

# Output
Return ONLY a JSON object that follows the provided schema. Text fields may use Markdown emphasis or bullet lists, but no headings and no tables. Be specific and concise; do not repeat the same figure across sections."""


USER_PROMPT_TEMPLATE = """Write the equipment-level incident report for **{equipment_id}** (site: {site}).
Equipment priority: {priority} · risk level: {risk_level} (given, do not change).

Language of all text fields: {language}.

Write exactly one entry in `cluster_sections` for each failure mode, in this order: {clusters}.
Provide 3 to 5 root-cause hypotheses and 4 to 7 recommendations, each recommendation targeting one of the failure modes above.

Input data:
```json
{payload_json}
```"""


def build_user_prompt(payload: dict, language: str = "English") -> str:
    eqp = payload["equipment"]
    return USER_PROMPT_TEMPLATE.format(
        equipment_id=eqp["equipment_id"],
        site=eqp["site"],
        priority=eqp["equipment_priority"],
        risk_level=eqp["risk_level"],
        language=language,
        clusters="; ".join(f'"{c["cluster"]}"' for c in payload["failure_modes"]),
        payload_json=json.dumps(payload, ensure_ascii=False, indent=1),
    )


def _str(description: str) -> dict:
    return {"type": "string", "description": description}


def _enum(values: list[str], description: str) -> dict:
    return {"type": "string", "enum": values, "description": description}


def _objet(properties: dict) -> dict:
    return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}


def build_output_schema(clusters: list[str]) -> dict:
    """Schéma de sortie ; les noms de failure modes sont contraints à ceux de l'équipement."""
    return _objet({
        "report_title": _str("Short title naming the equipment and its main issue."),
        "synopsis": _str("3-4 sentence executive summary: what fails, how much it costs, how it compares to the site, what to do first."),
        "risk_justification": _str("One sentence explaining the given risk level with figures from the input."),
        "timeline_analysis": _str("Cost timeline: trend, close sequences, recurrences, dominant incidents."),
        "weather_downtime_analysis": _str("Downtime vs weather, using the representation and sample flags."),
        "cluster_weather_analysis": _str("Which failure modes occur under which weather conditions, and what it suggests."),
        "cluster_sections": {
            "type": "array",
            "items": _objet({
                "cluster": _enum(clusters, "Failure mode name, verbatim."),
                "analysis": _str("2-4 sentences: probable mechanism, evidence on this equipment (#numbers, dates, cost), impact."),
            }),
        },
        "root_causes": {
            "type": "array",
            "items": _objet({
                "hypothesis": _str("Root-cause hypothesis."),
                "evidence": _str("Evidence from the input (#numbers, counts, weather, dates)."),
                "confidence": _enum(["high", "medium", "low"], "Confidence given the number of incidents supporting it."),
            }),
        },
        "recommendations": {
            "type": "array",
            "items": _objet({
                "action": _str("Concrete maintenance or technical action."),
                "type": _enum(["preventive", "corrective", "monitoring", "design change", "spare parts"], "Action type."),
                "target_cluster": _enum(clusters, "Failure mode addressed (its priority sets the recommendation priority)."),
                "expected_impact": _str("Expected effect, using input figures when relevant (no new calculation)."),
            }),
        },
        "conclusion": _str("2-3 sentence conclusion."),
    })
