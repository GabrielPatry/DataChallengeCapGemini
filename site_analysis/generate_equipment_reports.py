"""Rapport d'incidents par équipement (PV) généré par le LLM Azure OpenAI.

Pour chaque équipement critique :
  1. payload JSON (arrêt vs météo, cluster x météo, ligne de temps des coûts) -> payloads/
  2. figures PNG -> figures/
  3. appel Azure (system + user prompt, sortie JSON structurée) -> reports/<eq>.llm.json
  4. rendu du template markdown -> reports/<eq>.md

Exemples (depuis la racine du repo) :
  python site_analysis/generate_equipment_reports.py --dry-run
  python site_analysis/generate_equipment_reports.py --equipment OUEST1-INV06
  python site_analysis/generate_equipment_reports.py --criterion v2 --language French
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import date
from pathlib import Path

import pandas as pd

from equipment_data import (
    COMPOSANTES, CRITERES, ROOT, build_payload, compute_criticality, load_incidents,
    plot_cluster_weather, plot_cost_timeline, plot_downtime_weather, select_equipment,
)
from prompts import OUTPUT_SCHEMA, SYSTEM_PROMPT, build_user_prompt

OUT = Path(__file__).resolve().parent
TEMPLATE_PATH = OUT / "equipment_report_template.md"


# ---------------- Client Azure ----------------
def get_client():
    try:
        # Réseau d'entreprise avec inspection SSL (cf. notebook)
        import truststore
        truststore.inject_into_ssl()
    except ImportError:
        pass
    from dotenv import load_dotenv
    from openai import AzureOpenAI

    load_dotenv(ROOT / ".env", override=True)
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    )
    return client, os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]


def call_llm(client, deployment: str, user_prompt: str, max_attempts: int = 6,
             system_prompt: str = SYSTEM_PROMPT, schema: dict = OUTPUT_SCHEMA) -> dict:
    """Appel chat avec sortie JSON structurée ; repli sur json_object si json_schema n'est pas supporté."""
    from openai import BadRequestError, RateLimitError

    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
    formats = [
        {"type": "json_schema", "json_schema": {"name": "equipment_report", "strict": True, "schema": schema}},
        {"type": "json_object"},
    ]
    for response_format in formats:
        for attempt in range(1, max_attempts + 1):
            try:
                response = client.with_options(max_retries=0).chat.completions.create(
                    model=deployment,
                    messages=messages if response_format["type"] == "json_schema" else messages + [{
                        "role": "user",
                        "content": "Return the JSON object following this schema:\n" + json.dumps(schema),
                    }],
                    response_format=response_format,
                    temperature=0.2,
                    max_tokens=6000,
                )
                return json.loads(response.choices[0].message.content)
            except RateLimitError as e:
                if attempt == max_attempts:
                    raise
                match = re.search(r"retry after (\d+) seconds", str(e))
                wait = int(match.group(1)) + 1 if match else 30
                print(f"  quota atteint (429), nouvelle tentative dans {wait} s")
                time.sleep(wait)
            except BadRequestError as e:
                if response_format["type"] != "json_schema":
                    raise
                print(f"  json_schema refusé ({e.message[:120]}), repli sur json_object")
                break
    raise RuntimeError("Aucune réponse du LLM")


# ---------------- Rendu markdown ----------------
def _eur(x) -> str:
    return f"{x:,.0f}".replace(",", " ")


def _table(lignes: list[dict], colonnes: dict[str, str]) -> str:
    entete = "| " + " | ".join(colonnes.values()) + " |"
    sep = "| " + " | ".join("---" for _ in colonnes) + " |"
    corps = ["| " + " | ".join("" if l.get(k) is None else str(l.get(k)) for k in colonnes) + " |" for l in lignes]
    return "\n".join([entete, sep, *corps])


def methodology(criterion: str) -> str:
    poids = ", ".join(f"{k} (×{v:g})" for k, v in COMPOSANTES.items())
    return (
        "Incidents come from `incidents_clusterised_solar.csv` (text, digital PDF and scanned PDF reports, "
        "clustered into failure modes with BERTopic on Azure OpenAI embeddings). "
        f"The criticality score combines leave-one-out robust z-scores of {poids}, computed against the other "
        "equipment of the same site (and, for the fleet score, against all solar equipment), mapped to 0-100 "
        f"with the normal CDF. Selection criterion used: *{CRITERES[criterion]}*. "
        "The detailed tables, figures and the narrative analysis only cover moderate and severe incidents; "
        "the narrative sections are written by an LLM from the aggregated tables and checked against them."
    )


def render_report(payload: dict, llm: dict, criterion: str, figures: dict[str, Path]) -> str:
    eqp, kf_all, kf = payload["equipment"], payload["key_figures_all_severities"], payload["key_figures_moderate_and_severe"]
    crit, med = eqp["criticality"], kf_all["median_equipment_of_same_site"]
    clusters, meteo = payload["summary_by_cluster"], payload["table_downtime_vs_weather"]

    sections_cluster = "\n\n".join(f"### {c['cluster']}\n\n{c['analysis']}" for c in llm["cluster_sections"])
    causes = "\n".join(
        f"{i}. **{c['hypothesis']}** *(confidence: {c['confidence']})* — {c['evidence']}"
        for i, c in enumerate(llm["root_causes"], 1)
    )
    recos = _table(
        sorted(llm["recommendations"], key=lambda r: r["priority"]),
        {"priority": "Priority", "action": "Action", "type": "Type", "target": "Target", "expected_impact": "Expected impact"},
    )

    valeurs = {
        **{k: llm[k] for k in ("report_title", "synopsis", "risk_justification", "timeline_analysis",
                               "weather_downtime_analysis", "cluster_weather_analysis", "conclusion")},
        "risk_level": llm["risk_level"].upper(),
        "equipment_id": eqp["equipment_id"],
        "site": eqp["site"],
        "asset_label": "Photovoltaic (inverter)",
        "generation_date": date.today().isoformat(),
        "n_incidents_all": kf_all["n_incidents"],
        "site_median_n_incidents": med["n_incidents"],
        "site_median_n_severe": med["n_incidents_severes"],
        "total_cost_all_eur": _eur(kf_all["cost_total_eur"]),
        "site_median_cost_eur": _eur(med["cout_total_eur"]),
        "total_downtime_all_hours": kf_all["downtime_total_h"],
        "site_median_downtime_hours": med["arret_total_h"],
        "n_focus": kf["n_incidents"],
        "n_moderate": kf["n_moderate"],
        "n_severe": kf["n_severe"],
        "period_start": kf_all["period"][0],
        "period_end": kf_all["period"][1],
        "total_cost_focus_eur": _eur(kf["cost_total_eur"]),
        "avg_cost_focus_eur": _eur(kf["cost_mean_eur"]),
        "total_downtime_focus_hours": kf["downtime_total_h"],
        "top_cluster_by_cost": f"{clusters[0]['cluster']} ({_eur(clusters[0]['cost_total_eur'])} EUR)",
        "top_weather_by_downtime": f"{meteo[0]['weather_condition']} ({meteo[0]['downtime_total_h']} h)",
        "score_site": crit["score_within_site_0_100"],
        "rank_in_site": crit["rank_within_site"],
        "n_equipment_site": crit["n_equipment_on_site"],
        "score_fleet": crit["score_vs_whole_fleet_0_100"],
        "methodology": methodology(criterion),
        "figure_cost_timeline": f"![Cost timeline]({figures['timeline']})",
        "figure_downtime_weather": f"![Downtime vs weather]({figures['downtime_weather']})",
        "figure_cluster_weather": f"![Cluster vs weather]({figures['cluster_weather']})",
        "yearly_table": _table(payload["summary_by_year"], {
            "year": "Year", "n_incidents": "Incidents", "n_severe": "Severe", "cost_eur": "Cost (EUR)", "downtime_h": "Downtime (h)"}),
        "downtime_weather_table": _table(meteo, {
            "weather_condition": "Weather", "n_incidents": "Incidents", "n_severe": "Severe",
            "downtime_total_h": "Downtime (h)", "downtime_median_h": "Median (h)",
            "share_of_equipment_downtime_pct": "% of downtime", "lift_vs_site": "Lift vs site"}),
        "cluster_table": _table(clusters, {
            "cluster": "Cluster", "n_incidents": "Incidents", "n_severe": "Severe", "cost_total_eur": "Cost (EUR)",
            "cost_share_pct": "% of cost", "recurrences_within_90_days": "Recurrences < 90 d",
            "share_of_equipment_incidents_pct": "% equipment", "share_of_site_incidents_pct": "% site"}),
        "cluster_sections": sections_cluster,
        "root_causes": causes,
        "recommendations": recos,
        "limitations": "\n".join(f"- {l}" for l in llm["limitations"]),
    }
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    return re.sub(r"\{\{\s*(\w+)\s*\}\}", lambda m: str(valeurs.get(m.group(1), m.group(0))), template)


# ---------------- Pipeline ----------------
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--criterion", choices=list(CRITERES), default="notebook")
    parser.add_argument("--equipment", nargs="*", help="Forcer une liste d'équipements (ignore le critère)")
    parser.add_argument("--site", help="Préfixe d'équipement pour filtrer un site, ex. OUEST1")
    parser.add_argument("--limit", type=int, help="Nombre maximal d'équipements à traiter")
    parser.add_argument("--language", default="English")
    parser.add_argument("--with-text", action="store_true", help="Ajouter un extrait du rapport technicien par incident")
    parser.add_argument("--dry-run", action="store_true", help="Payloads, figures et prompts, sans appel Azure")
    parser.add_argument("--force", action="store_true", help="Rappeler le LLM même si une génération existe")
    args = parser.parse_args()

    for sous_dossier in ("payloads", "figures", "reports", "prompts"):
        (OUT / sous_dossier).mkdir(exist_ok=True)

    df = load_incidents()
    eq = compute_criticality(df)
    eq.round(2).to_csv(OUT / "equipment_criticality.csv", index=False)

    equipements = args.equipment or select_equipment(eq, args.criterion)
    if args.site:
        equipements = [e for e in equipements if e.startswith(args.site.upper())]
    if args.limit:
        equipements = equipements[: args.limit]
    print(f"{len(equipements)} équipements ({args.criterion}) : {', '.join(equipements)}")

    client = deployment = None
    if not args.dry_run:
        client, deployment = get_client()

    for equipment_id in equipements:
        print(f"- {equipment_id}")
        payload = build_payload(df, eq, equipment_id, args.criterion, with_text=args.with_text)
        (OUT / "payloads" / f"{equipment_id}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

        figures = {
            "timeline": OUT / "figures" / f"{equipment_id}_cost_timeline.png",
            "downtime_weather": OUT / "figures" / f"{equipment_id}_downtime_weather.png",
            "cluster_weather": OUT / "figures" / f"{equipment_id}_cluster_weather.png",
        }
        plot_cost_timeline(df, equipment_id, figures["timeline"])
        plot_downtime_weather(df, equipment_id, figures["downtime_weather"])
        plot_cluster_weather(df, equipment_id, figures["cluster_weather"])

        user_prompt = build_user_prompt(payload, args.language)
        (OUT / "prompts" / f"{equipment_id}.user.md").write_text(user_prompt, encoding="utf-8")
        if args.dry_run:
            continue

        # Les générations sont sauvegardées pour ne pas reconsommer de quota
        llm_path = OUT / "reports" / f"{equipment_id}.llm.json"
        if llm_path.exists() and not args.force:
            llm = json.loads(llm_path.read_text(encoding="utf-8"))
        else:
            llm = call_llm(client, deployment, user_prompt)
            llm_path.write_text(json.dumps(llm, ensure_ascii=False, indent=2), encoding="utf-8")

        rel = {k: Path("..", "figures", p.name).as_posix() for k, p in figures.items()}
        rapport = render_report(payload, llm, args.criterion, rel)
        (OUT / "reports" / f"{equipment_id}.md").write_text(rapport, encoding="utf-8")
        print(f"  -> reports/{equipment_id}.md")

    (OUT / "prompts" / "system.md").write_text(SYSTEM_PROMPT, encoding="utf-8")


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    main()
