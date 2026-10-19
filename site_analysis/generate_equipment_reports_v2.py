"""Rapport par équipement, version 2 du prompt (critère v2, aucun calcul côté LLM).

Sorties suffixées "-v2" pour comparer avec la v1 (generate_equipment_reports.py) :
payloads/<eq>-v2.json, payloads/<eq>-v2.mapping.json (#k -> incident_id), figures/<eq>-v2_*.png,
prompts/<eq>-v2.user.md, prompts/system-v2.md, reports/<eq>-v2.llm.json, reports/<eq>-v2.md

Exemples (depuis la racine du repo) :
  python site_analysis/generate_equipment_reports_v2.py --equipment OUEST1-INV10
  python site_analysis/generate_equipment_reports_v2.py --site OUEST1 --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

from equipment_data import (
    REGLES_PRIORITE, build_payload_v2, compute_criticality, load_incidents,
    plot_cluster_weather, plot_cost_timeline, plot_downtime_weather, select_equipment,
)
from generate_equipment_reports import OUT, _eur, _table, call_llm, get_client
from prompts_v2 import SYSTEM_PROMPT, build_output_schema, build_user_prompt

TEMPLATE_PATH = OUT / "equipment_report_template_v2.md"
SUFFIXE = "-v2"


def methodology(payload: dict, period: tuple[str, str]) -> str:
    eqp = payload["equipment"]
    return "\n\n".join([
        f"**Scope.** This report covers the maintenance incidents recorded on {eqp['equipment_id']} between "
        f"{period[0]} and {period[1]}. Each incident report was read and assigned to a *failure mode* according "
        "to its description. The detailed analysis focuses on moderate and severe incidents; minor incidents "
        "only appear in the key figures. Incidents are numbered #1, #2, … in chronological order for this "
        "equipment (see the annex).",
        "**Why this equipment.** Each piece of equipment receives a criticality score from 0 to 100 that combines "
        "four indicators: number of incidents, number of severe incidents (counted twice), total repair cost and "
        "total downtime. The score is computed twice: against the other equipment of the same site and against "
        "all solar equipment of the fleet. 50 corresponds to a typical piece of equipment, 75 or more to one "
        "clearly above the others. Equipment scoring 75 or more on both comparisons is priority **P1**, on one of "
        f"them priority **P2**. Here: {eqp['why_selected']} → **{eqp['equipment_priority']}**.",
        "**Recommendation priority.** Each recommendation addresses one failure mode and inherits its priority:\n"
        + "\n".join(f"- **{p}** — {regle}" for p, regle in REGLES_PRIORITE.items()),
        "**Analysis.** All figures, tables and charts are computed directly from the incident records. "
        "The commentary was drafted with the help of an AI assistant from these figures only.",
        "*Patterns based on fewer than three incidents are flagged as indicative in the text.*",
    ])


def render_report(payload: dict, llm: dict, figures: dict[str, str], period: tuple[str, str],
                  mapping_dates: dict) -> str:
    eqp, kf = payload["equipment"], payload["key_figures_moderate_and_severe"]
    comp, modes, meteo = (payload["comparison_with_site_median_equipment"], payload["failure_modes"],
                          payload["table_downtime_vs_weather"])
    priorite_mode = {m["cluster"]: m["recommendation_priority"] for m in modes}

    sections_cluster = "\n\n".join(
        f"### {c['cluster']} · {priorite_mode.get(c['cluster'], '')}\n\n{c['analysis']}" for c in llm["cluster_sections"])
    causes = "\n".join(
        f"{i}. **{c['hypothesis']}** *(confidence: {c['confidence']})* — {c['evidence']}"
        for i, c in enumerate(llm["root_causes"], 1))
    recos = [{**r, "priority": priorite_mode.get(r["target_cluster"], "P3")} for r in llm["recommendations"]]
    recos.sort(key=lambda r: r["priority"])

    registre = [
        {"no": t["incident_no"], "date": t["date"], "severity": t["severity"], "cluster": t["cluster"],
         "cost": _eur(t["cost_eur"]), "downtime": t["downtime_h"], "weather": t["weather_condition"]}
        for t in payload["table_cost_timeline"]
    ]

    valeurs = {
        **{k: llm[k] for k in ("report_title", "synopsis", "risk_justification", "timeline_analysis",
                               "weather_downtime_analysis", "cluster_weather_analysis", "conclusion")},
        "equipment_id": eqp["equipment_id"],
        "site": eqp["site"],
        "asset_label": "Photovoltaic (inverter)",
        "generation_date": date.today().isoformat(),
        "equipment_priority": eqp["equipment_priority"],
        "risk_level": eqp["risk_level"].upper(),
        "n_incidents_all": comp["incidents_all_severities"]["this_equipment"],
        "site_median_n_incidents": comp["incidents_all_severities"]["site_median_equipment"],
        "ratio_n_incidents": comp["incidents_all_severities"]["ratio_to_site_median"],
        "n_severe_all": comp["severe_incidents"]["this_equipment"],
        "site_median_n_severe": comp["severe_incidents"]["site_median_equipment"],
        "ratio_n_severe": comp["severe_incidents"]["ratio_to_site_median"],
        "total_cost_all_eur": _eur(comp["cost_all_severities_eur"]["this_equipment"]),
        "site_median_cost_eur": _eur(comp["cost_all_severities_eur"]["site_median_equipment"]),
        "ratio_cost": comp["cost_all_severities_eur"]["ratio_to_site_median"],
        "total_downtime_all_hours": comp["downtime_all_severities_h"]["this_equipment"],
        "site_median_downtime_hours": comp["downtime_all_severities_h"]["site_median_equipment"],
        "ratio_downtime": comp["downtime_all_severities_h"]["ratio_to_site_median"],
        "n_focus": kf["n_incidents"],
        "n_moderate": kf["n_moderate"],
        "n_severe": kf["n_severe"],
        "period_start": period[0],
        "period_end": period[1],
        "total_cost_focus_eur": _eur(kf["cost_total_eur"]),
        "severe_share_of_cost": kf["severe_share_of_cost_pct"],
        "avg_cost_focus_eur": _eur(kf["cost_mean_eur"]),
        "total_downtime_focus_hours": kf["downtime_total_h"],
        "mean_days_between": kf["mean_days_between_incidents"],
        "top_cluster_by_cost": f"{modes[0]['cluster']} ({_eur(modes[0]['cost_total_eur'])} EUR)",
        "top_weather_by_downtime": f"{meteo[0]['weather_condition']} ({meteo[0]['downtime_total_h']} h)",
        "methodology": methodology(payload, period),
        "figure_cost_timeline": f"![Cost timeline]({figures['timeline']})",
        "figure_downtime_weather": f"![Downtime vs weather]({figures['downtime_weather']})",
        "figure_cluster_weather": f"![Failure modes vs weather]({figures['cluster_weather']})",
        "yearly_table": _table(
            [{**a, "cost": _eur(a["cost_eur"]),
              "change": "" if a["cost_change_vs_previous_year_pct"] is None else f"{a['cost_change_vs_previous_year_pct']:+} %"}
             for a in payload["yearly_trend"]["by_year"]],
            {"year": "Year", "n_incidents": "Incidents", "n_severe": "Severe", "cost": "Cost (EUR)",
             "change": "Cost vs previous year", "downtime_h": "Downtime (h)"}),
        "downtime_weather_table": _table(meteo, {
            "weather_condition": "Weather", "n_incidents": "Incidents", "n_severe": "Severe",
            "downtime_total_h": "Downtime (h)", "downtime_median_h": "Median (h)",
            "share_of_equipment_downtime_pct": "% of downtime", "representation": "Compared with site"}),
        "cluster_table": _table(
            [{**m, "cost": _eur(m["cost_total_eur"]), "nos": ", ".join(m["incident_nos"])} for m in modes],
            {"cluster": "Failure mode", "recommendation_priority": "Priority", "n_incidents": "Incidents",
             "n_severe": "Severe", "cost": "Cost (EUR)", "cost_share_pct": "% of cost",
             "recurrences_within_90_days": "Recurrences < 90 d", "nos": "Incidents #"}),
        "cluster_sections": sections_cluster,
        "root_causes": causes,
        "recommendations": _table(recos, {
            "priority": "Priority", "action": "Action", "type": "Type",
            "target_cluster": "Failure mode addressed", "expected_impact": "Expected impact"}),
        "incident_register": _table(registre, {
            "no": "#", "date": "Date", "severity": "Severity", "cluster": "Failure mode",
            "cost": "Cost (EUR)", "downtime": "Downtime (h)", "weather": "Weather"}),
    }
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda m: str(valeurs.get(m.group(1), m.group(0))), template)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--equipment", nargs="*", help="Forcer une liste d'équipements (ignore le critère)")
    parser.add_argument("--site", help="Préfixe d'équipement pour filtrer un site, ex. OUEST1")
    parser.add_argument("--language", default="English")
    parser.add_argument("--dry-run", action="store_true", help="Payloads, figures et prompts, sans appel Azure")
    parser.add_argument("--force", action="store_true", help="Rappeler le LLM même si une génération existe")
    args = parser.parse_args()

    for sous_dossier in ("payloads", "figures", "reports", "prompts"):
        (OUT / sous_dossier).mkdir(exist_ok=True)
    (OUT / "prompts" / f"system{SUFFIXE}.md").write_text(SYSTEM_PROMPT, encoding="utf-8")

    df = load_incidents()
    eq = compute_criticality(df)
    equipements = args.equipment or select_equipment(eq, "v2")
    if args.site:
        equipements = [e for e in equipements if e.startswith(args.site.upper())]
    print(f"{len(equipements)} équipements : {', '.join(equipements)}")

    client = deployment = None
    if not args.dry_run:
        client, deployment = get_client()

    for equipment_id in equipements:
        print(f"- {equipment_id}")
        nom = f"{equipment_id}{SUFFIXE}"
        payload, correspondance = build_payload_v2(df, eq, equipment_id)
        (OUT / "payloads" / f"{nom}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (OUT / "payloads" / f"{nom}.mapping.json").write_text(json.dumps(correspondance, indent=1), encoding="utf-8")

        d_eq = df[df["equipment_id"] == equipment_id]
        period = (f"{d_eq['date'].min():%Y-%m-%d}", f"{d_eq['date'].max():%Y-%m-%d}")
        no_par_id = {c["incident_id"]: c["incident_no"] for c in correspondance}
        couts = d_eq.set_index("incident_id")["estimated_cost_eur"]
        top3 = {int(i): f"{no_par_id[int(i)]} · {_eur(couts[i])} €"
                for i in couts[list(no_par_id)].nlargest(3).index}

        figures = {
            "timeline": OUT / "figures" / f"{nom}_cost_timeline.png",
            "downtime_weather": OUT / "figures" / f"{nom}_downtime_weather.png",
            "cluster_weather": OUT / "figures" / f"{nom}_cluster_weather.png",
        }
        plot_cost_timeline(df, equipment_id, figures["timeline"], etiquettes=top3)
        plot_downtime_weather(df, equipment_id, figures["downtime_weather"])
        plot_cluster_weather(df, equipment_id, figures["cluster_weather"])

        user_prompt = build_user_prompt(payload, args.language)
        (OUT / "prompts" / f"{nom}.user.md").write_text(user_prompt, encoding="utf-8")
        if args.dry_run:
            continue

        llm_path = OUT / "reports" / f"{nom}.llm.json"
        if llm_path.exists() and not args.force:
            llm = json.loads(llm_path.read_text(encoding="utf-8"))
        else:
            schema = build_output_schema([m["cluster"] for m in payload["failure_modes"]])
            llm = call_llm(client, deployment, user_prompt, system_prompt=SYSTEM_PROMPT, schema=schema)
            llm_path.write_text(json.dumps(llm, ensure_ascii=False, indent=2), encoding="utf-8")

        rel = {k: Path("..", "figures", p.name).as_posix() for k, p in figures.items()}
        rapport = render_report(payload, llm, rel, period, no_par_id)
        (OUT / "reports" / f"{nom}.md").write_text(rapport, encoding="utf-8")
        print(f"  -> reports/{nom}.md")


if __name__ == "__main__":
    main()
