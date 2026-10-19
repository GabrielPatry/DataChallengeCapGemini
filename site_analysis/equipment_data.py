"""Préparation des données par équipement : score de criticité, payload JSON pour le LLM, figures.

Source : `incidents_clusterised_solar.csv` (incidents PV + cluster BERTopic nommé).
Seuls les incidents modérés et sévères alimentent les tableaux envoyés au LLM.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "incidents_clusterised_solar.csv"

SEVERITES_FOCUS = ["modérée", "sévère"]
ORDRE_METEO = [
    "ciel dégagé", "conditions nominales", "temps calme", "vent modéré", "pluie modérée",
    "forte chaleur", "canicule", "vent fort / tempête", "orage avec grêle",
    "orage avec activité électrique",
]

# ---------------- Criticité (repris du notebook, cellule "construire_eq") ----------------
COMPOSANTES = {"n_incidents": 1.0, "n_incidents_severes": 2.0, "cout_total": 1.0, "arret_total": 1.0}
SCORE_CRITIQUE = 75
Z_MAX = 3.0

CRITERES = {
    # Critère du notebook : score site >= 75, ou (>= 1 sévère et score site >= 50)
    "notebook": "score intra-site >= 75, ou au moins un incident sévère et score intra-site >= 50",
    # Variante proposée : on garde le score intra-site, on ajoute une comparaison à toute la flotte
    # (un onduleur "normal" sur un site très coûteux peut coûter plus que le pire d'un autre site).
    "v2": "score intra-site >= 75 ou score flotte >= 75 (P1 si les deux, P2 sinon)",
}

# ---------------- Familles de clusters (couleur) ; le marqueur distingue les clusters d'une famille ----------------
FAMILLES = {
    "Incendie": ["Incendie support bâtiment PV", "Incendie toiture et panneaux PV",
                 "Incendie bâtiment support PV", "Premiers secours incendie PV"],
    "Jonction / connectique": ["Point chaud boîtier de jonction", "Défaillance chaîne et boîtier de jonction",
                               "Remplacement préventif connecteurs"],
    "Câblage": ["Anomalies d'isolement câblage", "Dégradation et court-circuit câblage"],
    "Surtension": ["Surtensions et protections transitoires"],
    "Modules": ["Dommages superficiels modules PV"],
    "Surchauffe": ["Surchauffe panneaux PV", "Limitation puissance suite surchauffe"],
    "Encrassement": ["Salissure et nettoyage modules PV", "Encrassement et planification nettoyage"],
    "Onduleur": ["Baisse de rendement onduleur"],
}
# Palette catégorielle de référence (ordre fixe, validé CVD sur paires adjacentes)
COULEURS_FAMILLE = dict(zip(FAMILLES, [
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948",
]))
MARQUEURS = ["o", "s", "^", "D"]
STYLE_CLUSTER = {
    cluster: (COULEURS_FAMILLE[famille], MARQUEURS[i])
    for famille, clusters in FAMILLES.items()
    for i, cluster in enumerate(clusters)
}
STYLE_DEFAUT = ("#8a8984", "X")

TEXTE_SECONDAIRE = "#52514e"
GRILLE = "#e4e3df"


def load_incidents(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values(["site", "equipment_id", "date"]).reset_index(drop=True)


def calculer_z_loo(x: pd.Series) -> pd.Series:
    """Z-score robuste (médiane / MAD) de chaque valeur par rapport aux AUTRES valeurs."""
    valeurs = x.to_numpy(float)
    resultats = np.zeros(len(valeurs))
    for i in range(len(valeurs)):
        autres = np.delete(valeurs, i)
        if len(autres) == 0:
            continue
        mediane = np.median(autres)
        echelle = 1.4826 * np.median(np.abs(autres - mediane))
        if echelle == 0:
            echelle = np.std(autres)
        if echelle == 0:
            resultats[i] = 0.0 if valeurs[i] == mediane else np.sign(valeurs[i] - mediane) * Z_MAX
        else:
            resultats[i] = (valeurs[i] - mediane) / echelle
    return pd.Series(np.clip(resultats, -Z_MAX, Z_MAX), index=x.index)


def _score(z_par_composante: pd.DataFrame) -> pd.Series:
    poids = pd.Series(COMPOSANTES)
    z = (z_par_composante[list(COMPOSANTES)] * poids.values).sum(axis=1) / poids.sum()
    return 100 * norm.cdf(z)


def compute_criticality(df: pd.DataFrame) -> pd.DataFrame:
    eq = df.groupby(["site", "equipment_id"]).agg(
        n_incidents=("incident_id", "count"),
        n_incidents_severes=("severity", lambda s: (s == "sévère").sum()),
        cout_total=("estimated_cost_eur", "sum"),
        arret_total=("downtime_hours", "sum"),
    ).reset_index()

    z_site = pd.DataFrame({c: eq.groupby("site")[c].transform(calculer_z_loo) for c in COMPOSANTES})
    z_flotte = pd.DataFrame({c: calculer_z_loo(eq[c]) for c in COMPOSANTES})
    for c in COMPOSANTES:
        eq[f"z_{c}"] = z_site[c]
    eq["score_site"] = _score(z_site)
    eq["score_flotte"] = _score(z_flotte)
    eq["rang_site"] = eq.groupby("site")["score_site"].rank(ascending=False, method="min").astype(int)
    eq["n_equipements_site"] = eq.groupby("site")["equipment_id"].transform("count")

    a_un_severe = eq["n_incidents_severes"] >= 1
    eq["critique_notebook"] = (eq["score_site"] >= SCORE_CRITIQUE) | (a_un_severe & (eq["score_site"] >= 50))

    haut_site = eq["score_site"] >= SCORE_CRITIQUE
    haut_flotte = eq["score_flotte"] >= SCORE_CRITIQUE
    eq["critique_v2"] = haut_site | haut_flotte
    eq["priorite_v2"] = np.select([haut_site & haut_flotte, eq["critique_v2"]], ["P1", "P2"], default="-")

    return eq.sort_values(["site", "score_site"], ascending=[True, False]).reset_index(drop=True)


def select_equipment(eq: pd.DataFrame, criterion: str = "notebook") -> list[str]:
    if criterion not in CRITERES:
        raise ValueError(f"Critère inconnu : {criterion} (choix : {list(CRITERES)})")
    return eq.loc[eq[f"critique_{criterion}"], "equipment_id"].tolist()


# ---------------- Payload JSON envoyé au LLM ----------------
def _r(x, nd=1):
    if pd.isna(x):
        return None
    return int(round(float(x))) if nd == 0 else round(float(x), nd)


def _repartition_pct(s: pd.Series) -> dict:
    return {k: _r(100 * v) for k, v in s.value_counts(normalize=True).items()}


def build_payload(df: pd.DataFrame, eq: pd.DataFrame, equipment_id: str, criterion: str,
                  with_text: bool = False) -> dict:
    d_all = df[df["equipment_id"] == equipment_id].sort_values("date")
    site = d_all["site"].iloc[0]
    d = d_all[d_all["severity"].isin(SEVERITES_FOCUS)].copy()
    site_focus = df[(df["site"] == site) & df["severity"].isin(SEVERITES_FOCUS)]
    row = eq.set_index("equipment_id").loc[equipment_id]
    eq_site = eq[eq["site"] == site]

    # Repères de comparaison : le même équipement vs l'équipement médian du site
    equipement_median = {
        "n_incidents": _r(eq_site["n_incidents"].median()),
        "n_incidents_severes": _r(eq_site["n_incidents_severes"].median()),
        "cout_total_eur": _r(eq_site["cout_total"].median(), 0),
        "arret_total_h": _r(eq_site["arret_total"].median()),
    }

    # 1) Heures d'arrêt vs météo (+ surreprésentation vs le reste du site)
    part_site = site_focus["weather_condition"].value_counts(normalize=True)
    arret_meteo = []
    for meteo, g in d.groupby("weather_condition"):
        part_eq = len(g) / len(d)
        arret_meteo.append({
            "weather_condition": meteo,
            "n_incidents": int(len(g)),
            "n_severe": int((g["severity"] == "sévère").sum()),
            "downtime_total_h": _r(g["downtime_hours"].sum()),
            "downtime_mean_h": _r(g["downtime_hours"].mean()),
            "downtime_median_h": _r(g["downtime_hours"].median()),
            "downtime_max_h": _r(g["downtime_hours"].max()),
            "share_of_equipment_downtime_pct": _r(100 * g["downtime_hours"].sum() / d["downtime_hours"].sum()),
            "share_of_equipment_incidents_pct": _r(100 * part_eq),
            "share_of_site_incidents_pct": _r(100 * part_site.get(meteo, 0)),
            "lift_vs_site": _r(part_eq / part_site[meteo], 2) if part_site.get(meteo, 0) > 0 else None,
        })
    arret_meteo.sort(key=lambda r: r["downtime_total_h"], reverse=True)

    # 2) Nombre d'incidents : cluster x météo (cellules nulles omises)
    ct = pd.crosstab(d["cluster_name"], d["weather_condition"])
    cluster_meteo = {
        cluster: {m: int(n) for m, n in ligne.items() if n > 0}
        for cluster, ligne in ct.iterrows()
    }

    # 3) Ligne de temps des coûts (un point = un incident, avec son cluster)
    d["jours_depuis_precedent"] = d["date"].diff().dt.days
    d["jours_depuis_meme_cluster"] = d.groupby("cluster_name")["date"].diff().dt.days
    timeline = []
    for _, r in d.iterrows():
        item = {
            "incident_id": int(r["incident_id"]),
            "date": r["date"].strftime("%Y-%m-%d"),
            "severity": r["severity"],
            "cluster": r["cluster_name"],
            "cost_eur": _r(r["estimated_cost_eur"], 0),
            "downtime_h": _r(r["downtime_hours"]),
            "weather_condition": r["weather_condition"],
            "days_since_previous_incident": None if pd.isna(r["jours_depuis_precedent"]) else int(r["jours_depuis_precedent"]),
            "days_since_previous_same_cluster": None if pd.isna(r["jours_depuis_meme_cluster"]) else int(r["jours_depuis_meme_cluster"]),
        }
        if with_text:
            item["report_excerpt"] = " ".join(str(r["text"]).split())[:450]
        timeline.append(item)

    # Synthèses dérivées de la ligne de temps (tendance annuelle, récurrence par cluster)
    par_annee = [
        {"year": int(a), "n_incidents": int(len(g)), "n_severe": int((g["severity"] == "sévère").sum()),
         "cost_eur": _r(g["estimated_cost_eur"].sum(), 0), "downtime_h": _r(g["downtime_hours"].sum())}
        for a, g in d.groupby(d["date"].dt.year)
    ]
    part_cluster_site = site_focus["cluster_name"].value_counts(normalize=True)
    par_cluster = []
    for cluster, g in d.groupby("cluster_name"):
        ecarts = g["date"].diff().dt.days.dropna()
        par_cluster.append({
            "cluster": cluster,
            "n_incidents": int(len(g)),
            "n_severe": int((g["severity"] == "sévère").sum()),
            "cost_total_eur": _r(g["estimated_cost_eur"].sum(), 0),
            "cost_share_pct": _r(100 * g["estimated_cost_eur"].sum() / d["estimated_cost_eur"].sum()),
            "downtime_total_h": _r(g["downtime_hours"].sum()),
            "first_date": g["date"].min().strftime("%Y-%m-%d"),
            "last_date": g["date"].max().strftime("%Y-%m-%d"),
            "median_days_between_recurrences": _r(ecarts.median(), 0) if len(ecarts) else None,
            "recurrences_within_90_days": int((ecarts <= 90).sum()),
            "share_of_equipment_incidents_pct": _r(100 * len(g) / len(d)),
            "share_of_site_incidents_pct": _r(100 * part_cluster_site.get(cluster, 0)),
            # Redondant avec le tableau cluster x météo, mais évite les erreurs de lecture du LLM
            "weather_counts": cluster_meteo[cluster],
            "incident_ids": [int(i) for i in g["incident_id"]],
        })
    par_cluster.sort(key=lambda r: r["cost_total_eur"], reverse=True)

    return {
        "equipment": {
            "equipment_id": equipment_id,
            "site": site,
            "asset_type": "solar (PV inverter and its upstream DC field)",
            "selection_criterion": CRITERES[criterion],
            "criticality": {
                "score_within_site_0_100": _r(row["score_site"]),
                "rank_within_site": int(row["rang_site"]),
                "n_equipment_on_site": int(row["n_equipements_site"]),
                "score_vs_whole_fleet_0_100": _r(row["score_flotte"]),
                "priority_v2": row["priorite_v2"],
                "robust_z_within_site": {c: _r(row[f"z_{c}"], 2) for c in COMPOSANTES},
                "score_reading": "50 = typical equipment of the site, >= 75 = clear outlier",
            },
        },
        "key_figures_all_severities": {
            "n_incidents": int(len(d_all)),
            "by_severity": {k: int(v) for k, v in d_all["severity"].value_counts().items()},
            "cost_total_eur": _r(d_all["estimated_cost_eur"].sum(), 0),
            "downtime_total_h": _r(d_all["downtime_hours"].sum()),
            "period": [d_all["date"].min().strftime("%Y-%m-%d"), d_all["date"].max().strftime("%Y-%m-%d")],
            "median_equipment_of_same_site": equipement_median,
        },
        "key_figures_moderate_and_severe": {
            "n_incidents": int(len(d)),
            "n_moderate": int((d["severity"] == "modérée").sum()),
            "n_severe": int((d["severity"] == "sévère").sum()),
            "cost_total_eur": _r(d["estimated_cost_eur"].sum(), 0),
            "cost_mean_eur": _r(d["estimated_cost_eur"].mean(), 0),
            "downtime_total_h": _r(d["downtime_hours"].sum()),
            "downtime_mean_h": _r(d["downtime_hours"].mean()),
        },
        "table_downtime_vs_weather": arret_meteo,
        "table_incident_count_cluster_vs_weather": cluster_meteo,
        "table_cost_timeline": timeline,
        "summary_by_year": par_annee,
        "summary_by_cluster": par_cluster,
    }


# ---------------- Payload v2 : numérotation locale, tout est pré-calculé (le LLM ne calcule rien) ----------------
SEUIL_ECHANTILLON = 3      # en dessous : tendance "indicative"
JOURS_SEQUENCE = 30        # incidents successifs à moins de 30 jours = séquence rapprochée
SAISONS = {12: "winter", 1: "winter", 2: "winter", 3: "spring", 4: "spring", 5: "spring",
           6: "summer", 7: "summer", 8: "summer", 9: "autumn", 10: "autumn", 11: "autumn"}

REGLES_PRIORITE = {
    "P1": "within 1 month: the failure mode caused at least one severe incident on this equipment "
          "and either represents >= 20% of its cost or recurred within 90 days",
    "P2": "within 6 months: the failure mode caused at least one severe incident or represents >= 10% of the cost",
    "P3": "next yearly maintenance plan: all other failure modes",
}


def priorite_cluster(n_severe: int, part_cout_pct: float, recurrences_90j: int) -> tuple[str, str]:
    if n_severe >= 1 and (part_cout_pct >= 20 or recurrences_90j >= 1):
        raisons = [f"{n_severe} severe incident(s)"]
        if part_cout_pct >= 20:
            raisons.append(f"{part_cout_pct}% of the equipment cost")
        if recurrences_90j >= 1:
            raisons.append(f"{recurrences_90j} recurrence(s) within 90 days")
        return "P1", " + ".join(raisons)
    if n_severe >= 1:
        return "P2", f"{n_severe} severe incident(s), {part_cout_pct}% of the cost, no recurrence within 90 days"
    if part_cout_pct >= 10:
        return "P2", f"no severe incident but {part_cout_pct}% of the equipment cost"
    return "P3", f"no severe incident and {part_cout_pct}% of the cost"


def niveau_risque(row: pd.Series) -> str:
    if row["priorite_v2"] == "P1":
        return "critical"
    if row["priorite_v2"] == "P2":
        return "high"
    return "medium" if max(row["score_site"], row["score_flotte"]) >= 50 else "low"


def _representation(ratio) -> str:
    if ratio is None:
        return "not observed on the site"
    if ratio >= 1.3:
        return "over-represented vs site"
    if ratio <= 0.7:
        return "under-represented vs site"
    return "in line with site"


def _echantillon(n: int) -> str:
    return "indicative only (fewer than 3 incidents)" if n < SEUIL_ECHANTILLON else "ok"


def build_payload_v2(df: pd.DataFrame, eq: pd.DataFrame, equipment_id: str) -> tuple[dict, list[dict]]:
    """Payload v2 + table de correspondance numéro local (#k) -> incident_id (non envoyée au LLM)."""
    base = build_payload(df, eq, equipment_id, "v2")
    num = {t["incident_id"]: k for k, t in enumerate(base["table_cost_timeline"], 1)}
    d = _focus(df, equipment_id).copy()
    d["no"] = d["incident_id"].map(num)
    d = d.sort_values("no")
    row = eq.set_index("equipment_id").loc[equipment_id]
    kf_all, med = base["key_figures_all_severities"], base["key_figures_all_severities"]["median_equipment_of_same_site"]
    cout_total = d["estimated_cost_eur"].sum()

    def compare(valeur, mediane):
        return {"this_equipment": valeur, "site_median_equipment": mediane,
                "ratio_to_site_median": _r(valeur / mediane, 2) if mediane else None}

    s, f = row["score_site"], row["score_flotte"]
    equipement = {
        "equipment_id": equipment_id,
        "site": base["equipment"]["site"],
        "equipment_priority": row["priorite_v2"],
        "risk_level": niveau_risque(row),
        "criticality_score_within_site": _r(s),
        "criticality_score_vs_fleet": _r(f),
        "rank_within_site": int(row["rang_site"]),
        "n_equipment_on_site": int(row["n_equipements_site"]),
        "why_selected": f"score within site {_r(s)} ({'>=' if s >= 75 else '<'} 75), "
                        f"score vs fleet {_r(f)} ({'>=' if f >= 75 else '<'} 75)",
    }

    comparaison = {
        "incidents_all_severities": compare(kf_all["n_incidents"], med["n_incidents"]),
        "severe_incidents": compare(kf_all["by_severity"].get("sévère", 0), med["n_incidents_severes"]),
        "cost_all_severities_eur": compare(kf_all["cost_total_eur"], med["cout_total_eur"]),
        "downtime_all_severities_h": compare(kf_all["downtime_total_h"], med["arret_total_h"]),
    }

    severe = d["severity"] == "sévère"
    chiffres = {
        "n_incidents": int(len(d)),
        "n_moderate": int((~severe).sum()),
        "n_severe": int(severe.sum()),
        "severe_share_of_incidents_pct": _r(100 * severe.mean()),
        "cost_total_eur": _r(cout_total, 0),
        "cost_mean_eur": _r(d["estimated_cost_eur"].mean(), 0),
        "cost_median_eur": _r(d["estimated_cost_eur"].median(), 0),
        "severe_share_of_cost_pct": _r(100 * d.loc[severe, "estimated_cost_eur"].sum() / cout_total),
        "downtime_total_h": _r(d["downtime_hours"].sum()),
        "downtime_mean_h": _r(d["downtime_hours"].mean()),
        "mean_days_between_incidents": _r(d["date"].diff().dt.days.mean(), 0),
        "first_incident": f"#1 on {d['date'].iloc[0]:%Y-%m-%d}",
        "last_incident": f"#{len(d)} on {d['date'].iloc[-1]:%Y-%m-%d}",
    }

    # Tendance annuelle, variations déjà calculées
    annees = base["summary_by_year"]
    for prec, cour in zip([None] + annees[:-1], annees):
        cour["cost_change_vs_previous_year_pct"] = (
            _r(100 * (cour["cost_eur"] / prec["cost_eur"] - 1)) if prec else None)
        cour["incident_count_change_vs_previous_year"] = cour["n_incidents"] - prec["n_incidents"] if prec else None
    variation = 100 * (annees[-1]["cost_eur"] / annees[0]["cost_eur"] - 1) if len(annees) > 1 else 0
    tendance = {
        "first_year": annees[0]["year"], "last_year": annees[-1]["year"],
        "cost_change_first_to_last_year_pct": _r(variation),
        "label": "increasing" if variation > 20 else "decreasing" if variation < -20 else "stable",
    }

    saisons = []
    for saison in ["winter", "spring", "summer", "autumn"]:
        g = d[d["date"].dt.month.map(SAISONS) == saison]
        saisons.append({"season": saison, "n_incidents": int(len(g)), "n_severe": int((g["severity"] == "sévère").sum()),
                        "cost_eur": _r(g["estimated_cost_eur"].sum(), 0), "downtime_h": _r(g["downtime_hours"].sum())})

    top = d.nlargest(3, "estimated_cost_eur")
    plus_couteux = {
        "incidents": [
            {"incident_no": f"#{r['no']}", "date": f"{r['date']:%Y-%m-%d}", "severity": r["severity"],
             "cluster": r["cluster_name"], "weather_condition": r["weather_condition"],
             "cost_eur": _r(r["estimated_cost_eur"], 0), "downtime_h": _r(r["downtime_hours"]),
             "share_of_total_cost_pct": _r(100 * r["estimated_cost_eur"] / cout_total)}
            for _, r in top.iterrows()
        ],
        "top3_combined_cost_eur": _r(top["estimated_cost_eur"].sum(), 0),
        "top3_combined_share_of_total_cost_pct": _r(100 * top["estimated_cost_eur"].sum() / cout_total),
    }

    # Séquences d'incidents rapprochés (écart <= JOURS_SEQUENCE entre deux incidents successifs)
    sequences, courante = [], [d.iloc[0]]
    for (_, prec), (_, r) in zip(d.iloc[:-1].iterrows(), d.iloc[1:].iterrows()):
        if (r["date"] - prec["date"]).days <= JOURS_SEQUENCE:
            courante.append(r)
        else:
            sequences.append(courante)
            courante = [r]
    sequences.append(courante)
    sequences = [
        {"incident_nos": [f"#{r['no']}" for r in seq],
         "from": f"{seq[0]['date']:%Y-%m-%d}", "to": f"{seq[-1]['date']:%Y-%m-%d}",
         "span_days": int((seq[-1]["date"] - seq[0]["date"]).days),
         "n_severe": int(sum(r["severity"] == "sévère" for r in seq)),
         "combined_cost_eur": _r(sum(r["estimated_cost_eur"] for r in seq), 0),
         "clusters": sorted({r["cluster_name"] for r in seq})}
        for seq in sequences if len(seq) >= 2
    ]

    meteo = []
    for m in base["table_downtime_vs_weather"]:
        meteo.append({**m, "representation": _representation(m["lift_vs_site"]),
                      "sample": _echantillon(m["n_incidents"])})

    clusters = []
    for c in base["summary_by_cluster"]:
        g = d[d["cluster_name"] == c["cluster"]]
        ratio = (c["share_of_equipment_incidents_pct"] / c["share_of_site_incidents_pct"]
                 if c["share_of_site_incidents_pct"] else None)
        maxi = max(c["weather_counts"].values())
        dominantes = [m for m, n in c["weather_counts"].items() if n == maxi]
        priorite, raison = priorite_cluster(c["n_severe"], c["cost_share_pct"], c["recurrences_within_90_days"])
        clusters.append({
            "cluster": c["cluster"],
            "recommendation_priority": priorite,
            "priority_reason": raison,
            "n_incidents": c["n_incidents"],
            "n_moderate": c["n_incidents"] - c["n_severe"],
            "n_severe": c["n_severe"],
            "sample": _echantillon(c["n_incidents"]),
            "incident_nos": [f"#{n}" for n in g["no"]],
            "cost_total_eur": c["cost_total_eur"],
            "cost_mean_eur": _r(g["estimated_cost_eur"].mean(), 0),
            "cost_share_pct": c["cost_share_pct"],
            "downtime_total_h": c["downtime_total_h"],
            "first_date": c["first_date"],
            "last_date": c["last_date"],
            "median_days_between_recurrences": c["median_days_between_recurrences"],
            "recurrences_within_90_days": c["recurrences_within_90_days"],
            "share_of_equipment_incidents_pct": c["share_of_equipment_incidents_pct"],
            "share_of_site_incidents_pct": c["share_of_site_incidents_pct"],
            "ratio_equipment_vs_site_share": _r(ratio, 2) if ratio is not None else None,
            "representation": _representation(ratio),
            "weather_counts": c["weather_counts"],
            "dominant_weather": dominantes,
            "dominant_weather_share_pct": _r(100 * maxi / c["n_incidents"]),
        })

    timeline = [
        {"incident_no": f"#{num[t['incident_id']]}",
         **{k: v for k, v in t.items() if k not in ("incident_id", "report_excerpt")}}
        for t in base["table_cost_timeline"]
    ]

    payload = {
        "equipment": equipement,
        "comparison_with_site_median_equipment": comparaison,
        "key_figures_moderate_and_severe": chiffres,
        "yearly_trend": {"by_year": annees, "overall": tendance},
        "seasonality": saisons,
        "most_costly_incidents": plus_couteux,
        f"close_sequences_within_{JOURS_SEQUENCE}_days": sequences,
        "table_downtime_vs_weather": meteo,
        "table_incident_count_cluster_vs_weather": base["table_incident_count_cluster_vs_weather"],
        "failure_modes": clusters,
        "table_cost_timeline": timeline,
    }
    correspondance = [{"incident_no": f"#{k}", "incident_id": int(i)} for i, k in num.items()]
    return payload, correspondance


# ---------------- Figures (PNG insérées dans le rapport markdown) ----------------
def _style_axe(ax):
    ax.grid(color=GRILLE, lw=0.8)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=TEXTE_SECONDAIRE, labelsize=9)


def _focus(df: pd.DataFrame, equipment_id: str) -> pd.DataFrame:
    d = df[(df["equipment_id"] == equipment_id) & df["severity"].isin(SEVERITES_FOCUS)]
    return d.sort_values("date")


def plot_cost_timeline(df: pd.DataFrame, equipment_id: str, path: Path,
                       etiquettes: dict[int, str] | None = None) -> None:
    """Coût de chaque incident modéré/sévère dans le temps : couleur = famille, marqueur = cluster.

    `etiquettes` : {incident_id: texte} à annoter ; par défaut, seul le pic de coût est annoté.
    """
    d = _focus(df, equipment_id)
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.plot(d["date"], d["estimated_cost_eur"], color=GRILLE, lw=1.2, zorder=1)
    for cluster, g in d.groupby("cluster_name"):
        couleur, marqueur = STYLE_CLUSTER.get(cluster, STYLE_DEFAUT)
        severe = g["severity"] == "sévère"
        # Sévère = marqueur plein, modéré = marqueur creux (la gravité ne repose pas sur la couleur)
        ax.scatter(g.loc[severe, "date"], g.loc[severe, "estimated_cost_eur"], s=70, marker=marqueur,
                   color=couleur, edgecolor="white", linewidth=1.5, zorder=3)
        ax.scatter(g.loc[~severe, "date"], g.loc[~severe, "estimated_cost_eur"], s=60, marker=marqueur,
                   facecolor="white", edgecolor=couleur, linewidth=2, zorder=3)

    if etiquettes is None:
        pic = d.loc[d["estimated_cost_eur"].idxmax()]
        etiquettes = {pic["incident_id"]: f"{pic['estimated_cost_eur']:,.0f} €"}
    for incident_id, texte in etiquettes.items():
        r = d[d["incident_id"] == incident_id].iloc[0]
        ax.annotate(texte, (r["date"], r["estimated_cost_eur"]),
                    xytext=(8, 6), textcoords="offset points", fontsize=9, color=TEXTE_SECONDAIRE)

    _style_axe(ax)
    ax.set_ylabel("Coût estimé (€)", color=TEXTE_SECONDAIRE)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.set_xlim(df["date"].min() - pd.Timedelta(days=20), df["date"].max() + pd.Timedelta(days=20))
    ax.set_title(f"{equipment_id} — coût des incidents modérés et sévères par cluster",
                 loc="left", fontsize=12)

    handles = []
    for cluster in sorted(d["cluster_name"].unique()):
        couleur, marqueur = STYLE_CLUSTER.get(cluster, STYLE_DEFAUT)
        handles.append(Line2D([], [], ls="", marker=marqueur, color=couleur, markersize=8, label=cluster))
    handles += [
        Line2D([], [], ls="", marker="o", color=TEXTE_SECONDAIRE, markersize=8, label="plein = sévère"),
        Line2D([], [], ls="", marker="o", markerfacecolor="white", markeredgecolor=TEXTE_SECONDAIRE,
               markeredgewidth=2, markersize=8, label="creux = modérée"),
    ]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.01, 1), frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_downtime_weather(df: pd.DataFrame, equipment_id: str, path: Path) -> None:
    """Heures d'arrêt par condition météo : un point par incident, trait = médiane."""
    d = _focus(df, equipment_id)
    meteos = [m for m in ORDRE_METEO if m in set(d["weather_condition"])]
    meteos += sorted(set(d["weather_condition"]) - set(meteos))
    fig, ax = plt.subplots(figsize=(9, 0.5 * len(meteos) + 1.4))
    rng = np.random.default_rng(0)
    for i, m in enumerate(meteos):
        g = d[d["weather_condition"] == m]
        y = i + rng.uniform(-0.15, 0.15, len(g))
        ax.scatter(g["downtime_hours"], y, s=40, color="#2a78d6", edgecolor="white", linewidth=1, zorder=3)
        ax.vlines(g["downtime_hours"].median(), i - 0.3, i + 0.3, color="#0b0b0b", lw=2, zorder=4)
        ax.text(1.01, i, f"n={len(g)} · {g['downtime_hours'].sum():.0f} h",
                transform=ax.get_yaxis_transform(), va="center", fontsize=8, color=TEXTE_SECONDAIRE)
    _style_axe(ax)
    ax.set_yticks(range(len(meteos)))
    ax.set_yticklabels(meteos)
    ax.invert_yaxis()
    ax.set_xlabel("Heures d'arrêt par incident (trait noir = médiane)", color=TEXTE_SECONDAIRE)
    ax.set_title(f"{equipment_id} — heures d'arrêt vs météo (modérés + sévères)", loc="left", fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_cluster_weather(df: pd.DataFrame, equipment_id: str, path: Path) -> None:
    """Nombre d'incidents par cluster et par météo (heatmap séquentielle bleue)."""
    d = _focus(df, equipment_id)
    ct = pd.crosstab(d["cluster_name"], d["weather_condition"])
    ct = ct[[m for m in ORDRE_METEO if m in ct.columns] + [m for m in ct.columns if m not in ORDRE_METEO]]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list(
        "bleu", ["#fcfcfb", "#cde2fb", "#86b6ef", "#2a78d6", "#184f95"])
    fig, ax = plt.subplots(figsize=(0.95 * ct.shape[1] + 4, 0.5 * ct.shape[0] + 1.8))
    ax.imshow(ct.values, cmap=cmap, vmin=0, vmax=max(ct.values.max(), 1), aspect="auto")
    for i in range(ct.shape[0]):
        for j in range(ct.shape[1]):
            n = ct.values[i, j]
            if n:
                fonce = n > 0.55 * ct.values.max()
                ax.text(j, i, n, ha="center", va="center", fontsize=9,
                        color="white" if fonce else "#0b0b0b")
    ax.set_xticks(range(ct.shape[1]))
    ax.set_xticklabels(ct.columns, rotation=30, ha="right", fontsize=9, color=TEXTE_SECONDAIRE)
    ax.set_yticks(range(ct.shape[0]))
    ax.set_yticklabels(ct.index, fontsize=9, color=TEXTE_SECONDAIRE)
    ax.set_xticks(np.arange(-0.5, ct.shape[1]), minor=True)
    ax.set_yticks(np.arange(-0.5, ct.shape[0]), minor=True)
    ax.grid(which="minor", color="white", lw=2)
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(f"{equipment_id} — nombre d'incidents : cluster × météo", loc="left", fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
