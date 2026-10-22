"""Equipment-level statistics for the per-equipment incident reports (solar only).

Every number that ends up in an equipment report is computed here, in plain
pandas, so that the LLM agents of ``report_factory`` never calculate anything:
they receive these statistics and turn them into prose.

- ``compute_criticality`` scores every equipment against the other equipment
  of its site and against the whole fleet, and flags the critical ones
  (priority P1 or P2).
- ``number_incidents`` gives the moderate and severe incidents of one
  equipment a local number (``#1``, ``#2``… in chronological order), used in
  the report instead of the global ``incident_id``.
- ``weather_table`` and ``failure_mode_weather_matrix`` are shared with
  ``plot_factory``, so a figure and the statistics sent to the agents always
  come from the same computation.
- ``build_equipment_stats`` returns every statistic block used by the report
  sections, plus ready-made sentences (``facts``) for the figures the model
  tends to misread (most costly incident vs most costly failure mode, ratios,
  year-on-year changes).

Incidents of the clustering's noise cluster (``C_NOISE``) are relabelled
``UNCLASSIFIED``: they count in every total, timeline and register, but not in
the failure-mode analysis (failure modes, priorities, weather matrix).
"""

import math
from pathlib import Path

import numpy as np
import pandas as pd

# Only moderate and severe incidents are analysed in detail; minor ones only
# appear in the comparison with the site
FOCUS_SEVERITIES: list[str] = ["modérée", "sévère"]
SEVERE = "sévère"

# Display order of the weather conditions, from benign to extreme
WEATHER_ORDER: list[str] = [
    "ciel dégagé",
    "conditions nominales",
    "temps calme",
    "vent modéré",
    "pluie modérée",
    "forte chaleur",
    "canicule",
    "vent fort / tempête",
    "orage avec grêle",
    "orage avec activité électrique",
]

# Criticality score: weighted mean of leave-one-out robust z-scores, mapped to
# 0-100 with the normal CDF (50 = typical equipment, >= 75 = clear outlier)
CRITICALITY_WEIGHTS: dict[str, float] = {
    "n_incidents": 1.0,
    "n_severe": 2.0,
    "total_cost": 1.0,
    "total_downtime": 1.0,
}
CRITICAL_SCORE = 75
Z_MAX = 3.0

# Below this number of incidents, a pattern is reported as indicative only
SAMPLE_THRESHOLD = 3
# Successive incidents closer than this are grouped into a "close sequence"
SEQUENCE_DAYS = 30
# A failure mode coming back within this delay counts as a recurrence
RECURRENCE_DAYS = 90
# Lift thresholds (share on the equipment / share on the site)
OVER_REPRESENTED = 1.3
UNDER_REPRESENTED = 0.7

SEASONS: dict[int, str] = {
    12: "winter",
    1: "winter",
    2: "winter",
    3: "spring",
    4: "spring",
    5: "spring",
    6: "summer",
    7: "summer",
    8: "summer",
    9: "autumn",
    10: "autumn",
    11: "autumn",
}

# Noise cluster of the clustering step (incidents without a clear failure
# mode) and the label they get in the equipment reports
NOISE_CLUSTER_CODE = "C_NOISE"
UNCLASSIFIED = "Unclassified (no failure mode)"

# Priority of a recommendation = priority of the failure mode it addresses
PRIORITY_RULES: dict[str, str] = {
    "P1": (
        "within 1 month: the failure mode caused at least one severe incident on "
        f"this equipment and either represents >= 20% of its cost or recurred "
        f"within {RECURRENCE_DAYS} days"
    ),
    "P2": (
        "within 6 months: the failure mode caused at least one severe incident "
        "or represents >= 10% of the cost"
    ),
    "P3": "next yearly maintenance plan: all other failure modes",
}


def load_solar_incidents(csv_path: Path) -> pd.DataFrame:
    """Load the clusterised solar incidents CSV, with parsed dates.

    Noise-cluster incidents and incidents without a cluster are relabelled
    ``UNCLASSIFIED``.
    """
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    noise = df["cluster_name"].isna()
    if "cluster_code" in df.columns:
        noise |= df["cluster_code"] == NOISE_CLUSTER_CODE
    df.loc[noise, "cluster_name"] = UNCLASSIFIED
    return df.sort_values(["site", "equipment_id", "date"]).reset_index(drop=True)


def site_code(equipment_id: str) -> str:
    """Site code used as equipment prefix, e.g. ``OUEST1`` for ``OUEST1-INV10``."""
    return equipment_id.split("-")[0]


def format_eur(value: float) -> str:
    """``49142.3`` -> ``"49 142"`` (thin-space thousands, no decimals)."""
    return f"{value:,.0f}".replace(",", " ")


def _round(value, ndigits: int = 1):
    """JSON-friendly rounding: ``None`` for NaN, ``int`` when *ndigits* is 0."""
    if value is None or pd.isna(value):
        return None
    if ndigits == 0:
        return round(float(value))
    return round(float(value), ndigits)


# ---------------------------------------------------------------------------
# Criticality and selection of the equipment to report on
# ---------------------------------------------------------------------------


def _robust_loo_z(values: pd.Series) -> pd.Series:
    """Robust z-score (median / MAD) of each value against the OTHER values."""
    x = values.to_numpy(float)
    z = np.zeros(len(x))
    for i in range(len(x)):
        others = np.delete(x, i)
        if len(others) == 0:
            continue
        median = np.median(others)
        scale = 1.4826 * np.median(np.abs(others - median)) or np.std(others)
        if scale == 0:
            z[i] = 0.0 if x[i] == median else np.sign(x[i] - median) * Z_MAX
        else:
            z[i] = (x[i] - median) / scale
    return pd.Series(np.clip(z, -Z_MAX, Z_MAX), index=values.index)


def _score(z: pd.DataFrame) -> pd.Series:
    weights = pd.Series(CRITICALITY_WEIGHTS)
    combined = (z[weights.index] * weights).sum(axis=1) / weights.sum()
    return combined.map(lambda v: 50 * (1 + math.erf(v / math.sqrt(2))))


def compute_criticality(df: pd.DataFrame) -> pd.DataFrame:
    """One row per equipment with its criticality scores and priority.

    ``score_site`` compares the equipment with the other equipment of its
    site, ``score_fleet`` with every equipment of the dataframe. An equipment
    is critical when one of the two scores reaches ``CRITICAL_SCORE``:
    priority P1 if both do, P2 if only one does.
    """
    eq = (
        df.groupby(["site", "equipment_id"])
        .agg(
            n_incidents=("incident_id", "count"),
            n_severe=("severity", lambda s: int((s == SEVERE).sum())),
            total_cost=("estimated_cost_eur", "sum"),
            total_downtime=("downtime_hours", "sum"),
        )
        .reset_index()
    )
    z_site = pd.DataFrame(
        {c: eq.groupby("site")[c].transform(_robust_loo_z) for c in CRITICALITY_WEIGHTS}
    )
    z_fleet = pd.DataFrame({c: _robust_loo_z(eq[c]) for c in CRITICALITY_WEIGHTS})
    eq["score_site"] = _score(z_site)
    eq["score_fleet"] = _score(z_fleet)
    eq["rank_site"] = (
        eq.groupby("site")["score_site"].rank(ascending=False, method="min").astype(int)
    )
    eq["n_equipment_site"] = eq.groupby("site")["equipment_id"].transform("count")

    high_site = eq["score_site"] >= CRITICAL_SCORE
    high_fleet = eq["score_fleet"] >= CRITICAL_SCORE
    eq["is_critical"] = high_site | high_fleet
    eq["equipment_priority"] = np.select(
        [high_site & high_fleet, eq["is_critical"]], ["P1", "P2"], default="-"
    )
    eq["risk_level"] = np.select(
        [
            eq["equipment_priority"] == "P1",
            eq["equipment_priority"] == "P2",
            eq[["score_site", "score_fleet"]].max(axis=1) >= 50,
        ],
        ["critical", "high", "medium"],
        default="low",
    )
    return eq.sort_values(["site", "score_site"], ascending=[True, False]).reset_index(
        drop=True
    )


def select_equipment(
    criticality: pd.DataFrame,
    site: str,
    equipment: list[str] | None = None,
    all_equipment: bool = False,
) -> list[str]:
    """Equipment to report on for *site* (site code such as ``OUEST1`` or full site name).

    By default only the critical equipment (P1/P2) of the site; every
    equipment of the site with *all_equipment*; or exactly *equipment*.
    """
    codes = criticality["equipment_id"].map(site_code).str.upper()
    on_site = criticality[(codes == site.upper()) | (criticality["site"] == site)]
    if on_site.empty:
        known = ", ".join(sorted(codes.unique()))
        raise ValueError(f"Unknown site '{site}'. Known site codes: {known}")
    if equipment:
        unknown = sorted(set(equipment) - set(on_site["equipment_id"]))
        if unknown:
            raise ValueError(
                f"Equipment not found on site {site}: {', '.join(unknown)}"
            )
        return list(equipment)
    if all_equipment:
        return on_site["equipment_id"].tolist()
    return on_site.loc[on_site["is_critical"], "equipment_id"].tolist()


# ---------------------------------------------------------------------------
# Building blocks shared with plot_factory
# ---------------------------------------------------------------------------


def number_incidents(df: pd.DataFrame, equipment_id: str) -> pd.DataFrame:
    """Moderate and severe incidents of one equipment, numbered ``#1..#n`` by date.

    Adds ``no`` (int), ``ref`` (``"#k"``), ``days_since_previous`` and
    ``days_since_previous_same_mode``.
    """
    d = df[(df["equipment_id"] == equipment_id) & df["severity"].isin(FOCUS_SEVERITIES)]
    d = d.sort_values(["date", "incident_id"]).reset_index(drop=True)
    d["no"] = np.arange(1, len(d) + 1)
    d["ref"] = "#" + d["no"].astype(str)
    d["days_since_previous"] = d["date"].diff().dt.days
    d["days_since_previous_same_mode"] = (
        d.groupby("cluster_name")["date"].diff().dt.days
    )
    # Unclassified incidents do not share a failure mode with each other
    d.loc[d["cluster_name"] == UNCLASSIFIED, "days_since_previous_same_mode"] = np.nan
    return d


def classified(d: pd.DataFrame) -> pd.DataFrame:
    """Incidents of *d* that belong to a failure mode (``UNCLASSIFIED`` removed)."""
    return d[d["cluster_name"] != UNCLASSIFIED]


def has_failure_modes(df: pd.DataFrame, equipment_id: str) -> bool:
    """Whether the equipment has a moderate or severe incident with a failure mode."""
    return not classified(number_incidents(df, equipment_id)).empty


def site_focus(df: pd.DataFrame, site: str) -> pd.DataFrame:
    return df[(df["site"] == site) & df["severity"].isin(FOCUS_SEVERITIES)]


def representation(lift: float | None) -> str:
    """Plain-language reading of a lift (share on the equipment / share on the site)."""
    if lift is None:
        return "not observed on the rest of the site"
    if lift >= OVER_REPRESENTED:
        return "over-represented vs site"
    if lift <= UNDER_REPRESENTED:
        return "under-represented vs site"
    return "in line with site"


def sample_flag(n: int) -> str:
    return (
        f"indicative only (fewer than {SAMPLE_THRESHOLD} incidents)"
        if n < SAMPLE_THRESHOLD
        else "ok"
    )


def weather_table(d: pd.DataFrame, focus_site: pd.DataFrame) -> list[dict]:
    """Downtime per weather condition for numbered incidents *d*, most downtime first."""
    site_share = focus_site["weather_condition"].value_counts(normalize=True)
    total_downtime = d["downtime_hours"].sum()
    rows = []
    for weather, g in d.groupby("weather_condition"):
        share = len(g) / len(d)
        lift = share / site_share[weather] if site_share.get(weather, 0) > 0 else None
        rows.append(
            {
                "weather_condition": weather,
                "n_incidents": len(g),
                "n_severe": int((g["severity"] == SEVERE).sum()),
                "incidents": g["ref"].tolist(),
                "downtime_total_h": _round(g["downtime_hours"].sum()),
                "downtime_median_h": _round(g["downtime_hours"].median()),
                "downtime_max_h": _round(g["downtime_hours"].max()),
                "share_of_equipment_downtime_pct": _round(
                    100 * g["downtime_hours"].sum() / total_downtime
                ),
                "share_of_equipment_incidents_pct": _round(100 * share),
                "share_of_site_incidents_pct": _round(100 * site_share.get(weather, 0)),
                "representation": representation(lift),
                "sample": sample_flag(len(g)),
            }
        )
    return sorted(rows, key=lambda r: r["downtime_total_h"], reverse=True)


def ordered_weather(conditions) -> list[str]:
    present = set(conditions)
    return [w for w in WEATHER_ORDER if w in present] + sorted(
        present - set(WEATHER_ORDER)
    )


def failure_mode_weather_matrix(d: pd.DataFrame) -> dict[str, dict[str, int]]:
    """``{failure_mode: {weather: n_incidents}}``, empty cells and unclassified incidents omitted."""
    d = classified(d)
    ct = pd.crosstab(d["cluster_name"], d["weather_condition"])
    ct = ct[ordered_weather(ct.columns)]
    return {
        mode: {weather: int(n) for weather, n in row.items() if n > 0}
        for mode, row in ct.iterrows()
    }


# ---------------------------------------------------------------------------
# Statistics of one equipment, by report block
# ---------------------------------------------------------------------------


def failure_mode_priority(
    n_severe: int, cost_share_pct: float, recurrences: int
) -> tuple[str, str]:
    """Priority of a failure mode (see ``PRIORITY_RULES``) and the reason for it."""
    if n_severe >= 1 and (cost_share_pct >= 20 or recurrences >= 1):
        reasons = [f"{n_severe} severe incident(s)"]
        if cost_share_pct >= 20:
            reasons.append(f"{cost_share_pct}% of the equipment cost")
        if recurrences >= 1:
            reasons.append(f"{recurrences} recurrence(s) within {RECURRENCE_DAYS} days")
        return "P1", " + ".join(reasons)
    if n_severe >= 1:
        return "P2", (
            f"{n_severe} severe incident(s), {cost_share_pct}% of the cost, "
            f"no recurrence within {RECURRENCE_DAYS} days"
        )
    if cost_share_pct >= 10:
        return "P2", f"no severe incident but {cost_share_pct}% of the equipment cost"
    return "P3", f"no severe incident and {cost_share_pct}% of the cost"


def _compare(value, median) -> dict:
    return {
        "this_equipment": value,
        "site_median_equipment": median,
        "ratio_to_site_median": _round(value / median, 2) if median else None,
    }


def _yearly_trend(d: pd.DataFrame, years: range) -> dict:
    by_year = []
    for year in years:
        g = d[d["date"].dt.year == year]
        by_year.append(
            {
                "year": year,
                "n_incidents": len(g),
                "n_severe": int((g["severity"] == SEVERE).sum()),
                "cost_eur": _round(g["estimated_cost_eur"].sum(), 0),
                "downtime_h": _round(g["downtime_hours"].sum()),
            }
        )
    for previous, current in zip([None, *by_year[:-1]], by_year):
        current["cost_change_vs_previous_year_pct"] = (
            _round(100 * (current["cost_eur"] / previous["cost_eur"] - 1))
            if previous and previous["cost_eur"]
            else None
        )
        current["incident_count_change_vs_previous_year"] = (
            current["n_incidents"] - previous["n_incidents"] if previous else None
        )
    first, last = by_year[0], by_year[-1]
    change = (
        100 * (last["cost_eur"] / first["cost_eur"] - 1) if first["cost_eur"] else None
    )
    if change is None:
        label = "no incident in the first year"
    else:
        label = (
            "increasing" if change > 20 else "decreasing" if change < -20 else "stable"
        )
    overall = {
        "first_year": first["year"],
        "last_year": last["year"],
        "cost_change_first_to_last_year_pct": _round(change),
        "label": label,
    }
    return {"by_year": by_year, "overall": overall}


def _close_sequences(d: pd.DataFrame) -> list[dict]:
    groups, current = [], [d.iloc[0]]
    for i in range(1, len(d)):
        row = d.iloc[i]
        if (row["date"] - current[-1]["date"]).days <= SEQUENCE_DAYS:
            current.append(row)
        else:
            groups.append(current)
            current = [row]
    groups.append(current)
    return [
        {
            "incidents": [r["ref"] for r in group],
            "from": f"{group[0]['date']:%Y-%m-%d}",
            "to": f"{group[-1]['date']:%Y-%m-%d}",
            "span_days": int((group[-1]["date"] - group[0]["date"]).days),
            "n_severe": int(sum(r["severity"] == SEVERE for r in group)),
            "combined_cost_eur": _round(sum(r["estimated_cost_eur"] for r in group), 0),
            "failure_modes": sorted({r["cluster_name"] for r in group}),
        }
        for group in groups
        if len(group) >= 2
    ]


def _failure_modes(d: pd.DataFrame, focus_site: pd.DataFrame) -> list[dict]:
    total_cost = d["estimated_cost_eur"].sum()
    site_share = focus_site["cluster_name"].value_counts(normalize=True)
    weather = failure_mode_weather_matrix(d)
    modes = []
    # Shares stay relative to every incident of the equipment (d), but only
    # classified incidents form failure modes
    for mode, g in classified(d).groupby("cluster_name"):
        gaps = g["date"].diff().dt.days.dropna()
        n_severe = int((g["severity"] == SEVERE).sum())
        cost_share = _round(100 * g["estimated_cost_eur"].sum() / total_cost)
        recurrences = int((gaps <= RECURRENCE_DAYS).sum())
        priority, reason = failure_mode_priority(n_severe, cost_share, recurrences)
        share = len(g) / len(d)
        lift = share / site_share[mode] if site_share.get(mode, 0) > 0 else None
        top = max(weather[str(mode)].values())
        modes.append(
            {
                "failure_mode": mode,
                "recommendation_priority": priority,
                "priority_reason": reason,
                "n_incidents": len(g),
                "n_moderate": len(g) - n_severe,
                "n_severe": n_severe,
                "sample": sample_flag(len(g)),
                "cost_total_eur": _round(g["estimated_cost_eur"].sum(), 0),
                "cost_mean_eur": _round(g["estimated_cost_eur"].mean(), 0),
                "cost_share_pct": cost_share,
                "downtime_total_h": _round(g["downtime_hours"].sum()),
                "first_date": f"{g['date'].min():%Y-%m-%d}",
                "last_date": f"{g['date'].max():%Y-%m-%d}",
                "median_days_between_recurrences": _round(gaps.median(), 0)
                if len(gaps)
                else None,
                f"recurrences_within_{RECURRENCE_DAYS}_days": recurrences,
                "share_of_equipment_incidents_pct": _round(100 * share),
                "share_of_site_incidents_pct": _round(100 * site_share.get(mode, 0)),
                "representation": representation(lift),
                "weather_counts": weather[str(mode)],
                "dominant_weather": [
                    w for w, n in weather[str(mode)].items() if n == top
                ],
                "dominant_weather_share_pct": _round(100 * top / len(g)),
                "incidents": [
                    {
                        "ref": r["ref"],
                        "date": f"{r['date']:%Y-%m-%d}",
                        "severity": r["severity"],
                        "cost_eur": _round(r["estimated_cost_eur"], 0),
                        "downtime_h": _round(r["downtime_hours"]),
                        "weather_condition": r["weather_condition"],
                    }
                    for _, r in g.iterrows()
                ],
            }
        )
    return sorted(modes, key=lambda m: m["cost_total_eur"], reverse=True)


def build_equipment_stats(
    df: pd.DataFrame, criticality: pd.DataFrame, equipment_id: str
) -> dict:
    """Every statistic block of the report of *equipment_id* (JSON-serialisable).

    Raises
    ------
    ValueError
        If the equipment has no moderate or severe incident.
    """
    d_all = df[df["equipment_id"] == equipment_id]
    d = number_incidents(df, equipment_id)
    if d.empty:
        raise ValueError(
            f"{equipment_id} has no moderate or severe incident to analyse"
        )
    site = d_all["site"].iloc[0]
    focus_site = site_focus(df, site)
    row = criticality.set_index("equipment_id").loc[equipment_id]
    on_site = criticality[criticality["site"] == site]
    severe = d["severity"] == SEVERE
    total_cost = d["estimated_cost_eur"].sum()

    def versus(score: float) -> str:
        side = "at or above" if score >= CRITICAL_SCORE else "below"
        return f"{_round(score)} ({side} the threshold of {CRITICAL_SCORE})"

    priority = str(row["equipment_priority"])
    why = (
        f"criticality score {versus(row['score_site'])} against the other equipment of "
        f"the site and {versus(row['score_fleet'])} against the whole solar fleet"
    )
    equipment = {
        "equipment_id": equipment_id,
        "site": site,
        "asset_type": "PV inverter and the DC field upstream of it",
        "equipment_priority": priority if priority != "-" else "not critical",
        "risk_level": str(row["risk_level"]),
        "criticality_score_within_site": _round(row["score_site"]),
        "criticality_score_vs_fleet": _round(row["score_fleet"]),
        "rank_within_site": int(row["rank_site"]),
        "n_equipment_on_site": int(row["n_equipment_site"]),
        "why_selected": why,
    }

    comparison = {
        "incidents_all_severities": _compare(
            int(row["n_incidents"]), _round(on_site["n_incidents"].median())
        ),
        "severe_incidents": _compare(
            int(row["n_severe"]), _round(on_site["n_severe"].median())
        ),
        "cost_all_severities_eur": _compare(
            _round(row["total_cost"], 0), _round(on_site["total_cost"].median(), 0)
        ),
        "downtime_all_severities_h": _compare(
            _round(row["total_downtime"]), _round(on_site["total_downtime"].median())
        ),
    }

    key_figures = {
        "n_incidents": len(d),
        "n_moderate": int((~severe).sum()),
        "n_severe": int(severe.sum()),
        "severe_share_of_incidents_pct": _round(100 * severe.mean()),
        "cost_total_eur": _round(total_cost, 0),
        "cost_mean_eur": _round(d["estimated_cost_eur"].mean(), 0),
        "cost_median_eur": _round(d["estimated_cost_eur"].median(), 0),
        "severe_share_of_cost_pct": _round(
            100 * d.loc[severe, "estimated_cost_eur"].sum() / total_cost
        ),
        "downtime_total_h": _round(d["downtime_hours"].sum()),
        "downtime_mean_h": _round(d["downtime_hours"].mean()),
        "mean_days_between_incidents": _round(d["date"].diff().dt.days.mean(), 0),
        "first_incident": f"#1 on {d['date'].iloc[0]:%Y-%m-%d}",
        "last_incident": f"#{len(d)} on {d['date'].iloc[-1]:%Y-%m-%d}",
    }

    years = range(df["date"].dt.year.min(), df["date"].dt.year.max() + 1)
    yearly = _yearly_trend(d, years)

    seasonality = []
    for season in ("winter", "spring", "summer", "autumn"):
        g = d[d["date"].dt.month.map(SEASONS) == season]
        seasonality.append(
            {
                "season": season,
                "n_incidents": len(g),
                "n_severe": int((g["severity"] == SEVERE).sum()),
                "cost_eur": _round(g["estimated_cost_eur"].sum(), 0),
                "downtime_h": _round(g["downtime_hours"].sum()),
                "sample": sample_flag(len(g)),
            }
        )

    top = d.nlargest(3, "estimated_cost_eur")
    most_costly = {
        "incidents": [
            {
                "ref": r["ref"],
                "date": f"{r['date']:%Y-%m-%d}",
                "severity": r["severity"],
                "failure_mode": r["cluster_name"],
                "weather_condition": r["weather_condition"],
                "cost_eur": _round(r["estimated_cost_eur"], 0),
                "downtime_h": _round(r["downtime_hours"]),
                "share_of_total_cost_pct": _round(
                    100 * r["estimated_cost_eur"] / total_cost
                ),
            }
            for _, r in top.iterrows()
        ],
        "top3_combined_cost_eur": _round(top["estimated_cost_eur"].sum(), 0),
        "top3_combined_share_of_total_cost_pct": _round(
            100 * top["estimated_cost_eur"].sum() / total_cost
        ),
    }

    modes = _failure_modes(d, focus_site)
    weather = weather_table(d, focus_site)
    noise = d[d["cluster_name"] == UNCLASSIFIED]
    unclassified = {
        "n_incidents": len(noise),
        "incidents": noise["ref"].tolist(),
        "cost_eur": _round(noise["estimated_cost_eur"].sum(), 0),
        "cost_share_pct": _round(100 * noise["estimated_cost_eur"].sum() / total_cost),
    }

    register = [
        {
            "ref": r["ref"],
            "date": f"{r['date']:%Y-%m-%d}",
            "severity": r["severity"],
            "failure_mode": r["cluster_name"],
            "cost_eur": _round(r["estimated_cost_eur"], 0),
            "downtime_h": _round(r["downtime_hours"]),
            "weather_condition": r["weather_condition"],
        }
        for _, r in d.iterrows()
    ]

    return {
        "equipment": equipment,
        "period": {
            "first_record": f"{d_all['date'].min():%Y-%m-%d}",
            "last_record": f"{d_all['date'].max():%Y-%m-%d}",
        },
        "comparison_with_site_median": comparison,
        "key_figures": key_figures,
        "yearly_trend": yearly,
        "seasonality": seasonality,
        "most_costly_incidents": most_costly,
        f"close_sequences_within_{SEQUENCE_DAYS}_days": _close_sequences(d),
        "failure_modes": modes,
        "unclassified_incidents": unclassified,
        "register": register,
        "facts": _facts(
            comparison, key_figures, yearly, most_costly, modes, weather, unclassified
        ),
        # Local number -> global incident_id; never sent to the agents
        "incident_mapping": [
            {"ref": r["ref"], "incident_id": int(r["incident_id"])}
            for _, r in d.iterrows()
        ],
    }


def _facts(
    comparison, key_figures, yearly, most_costly, modes, weather, unclassified
) -> dict[str, list[str]]:
    """Ready-made sentences for the figures that are easy to misread, by topic."""

    def versus(label: str, block: dict, unit: str = "", fmt=str) -> str:
        ratio = block["ratio_to_site_median"]
        if ratio is None:
            reading = "no comparison possible"
        elif ratio >= 1.1:
            reading = "ABOVE the site median"
        elif ratio <= 0.9:
            reading = "BELOW the site median"
        else:
            reading = "IN LINE with the site median"
        return (
            f"{label}: {fmt(block['this_equipment'])}{unit} on this equipment vs "
            f"{fmt(block['site_median_equipment'])}{unit} for the median equipment of the site "
            f"(ratio ×{ratio}, {reading})."
        )

    benchmark = [
        versus("Incidents of all severities", comparison["incidents_all_severities"]),
        versus("Severe incidents", comparison["severe_incidents"]),
        versus(
            "Estimated cost of all incidents",
            comparison["cost_all_severities_eur"],
            " EUR",
            format_eur,
        ),
        versus(
            "Downtime of all incidents", comparison["downtime_all_severities_h"], " h"
        ),
    ]

    top_incident = most_costly["incidents"][0]
    top_mode = modes[0]
    cost = [
        (
            f"Moderate and severe incidents: {key_figures['n_incidents']} "
            f"({key_figures['n_severe']} severe), {format_eur(key_figures['cost_total_eur'])} EUR in total; "
            f"severe incidents account for {key_figures['severe_share_of_cost_pct']}% of this cost."
        ),
        (
            f"The most costly single incident is {top_incident['ref']} "
            f"({top_incident['failure_mode']}, {top_incident['severity']}, {top_incident['date']}): "
            f"{format_eur(top_incident['cost_eur'])} EUR, {top_incident['share_of_total_cost_pct']}% "
            "of the cost of moderate and severe incidents."
        ),
        (
            f"The most costly failure mode is {top_mode['failure_mode']}: "
            f"{format_eur(top_mode['cost_total_eur'])} EUR over {top_mode['n_incidents']} incident(s), "
            f"{top_mode['cost_share_pct']}% of the cost."
        ),
    ]
    if top_incident["failure_mode"] != top_mode["failure_mode"]:
        cost.append(
            "The most costly incident and the most costly failure mode are different: "
            "do not attribute one to the other."
        )
    if unclassified["n_incidents"]:
        cost.append(
            f"{unclassified['n_incidents']} incident(s) ({', '.join(unclassified['incidents'])}) "
            f"could not be assigned to a failure mode ({format_eur(unclassified['cost_eur'])} EUR, "
            f"{unclassified['cost_share_pct']}% of the cost): they count in every total but "
            "belong to no failure mode."
        )

    trend = []
    for year in yearly["by_year"]:
        change = year["cost_change_vs_previous_year_pct"]
        trend.append(
            f"{year['year']}: {year['n_incidents']} incident(s) ({year['n_severe']} severe), "
            f"{format_eur(year['cost_eur'])} EUR"
            + (f" ({change:+}% vs previous year)." if change is not None else ".")
        )
    overall = yearly["overall"]
    if overall["cost_change_first_to_last_year_pct"] is not None:
        trend.append(
            f"From {overall['first_year']} to {overall['last_year']} the cost changed by "
            f"{overall['cost_change_first_to_last_year_pct']:+}% (trend: {overall['label']})."
        )

    top_weather = weather[0]
    weather_facts = [
        (
            f"Most downtime occurs under '{top_weather['weather_condition']}': "
            f"{top_weather['downtime_total_h']} h over {top_weather['n_incidents']} incident(s), "
            f"{top_weather['share_of_equipment_downtime_pct']}% of the downtime "
            f"({top_weather['representation']})."
        ),
        *(
            f"'{w['weather_condition']}' is {w['representation']}: {w['share_of_equipment_incidents_pct']}% "
            f"of the incidents of this equipment vs {w['share_of_site_incidents_pct']}% on the site"
            + (" (indicative only)." if w["sample"] != "ok" else ".")
            for w in weather
            if w["representation"] != "in line with site"
        ),
    ]

    priorities = [
        f"{m['failure_mode']}: priority {m['recommendation_priority']} ({m['priority_reason']})."
        for m in modes
    ]
    return {
        "benchmark": benchmark,
        "cost": cost,
        "trend": trend,
        "weather": weather_facts,
        "priorities": priorities,
    }
