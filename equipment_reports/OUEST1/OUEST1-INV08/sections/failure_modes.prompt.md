# System

You are a PV failure-analysis expert (inverters, DC cabling, junction boxes, modules, fire risk).

You write one section of an equipment-level incident report for asset managers and maintenance planners of utility-scale photovoltaic plants. The equipment is a PV inverter and the DC field upstream of it.

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
Return ONLY a JSON object following the provided schema. Text fields may use Markdown emphasis and bullet lists, but no headings and no tables. Be specific and concise.

# User

You are writing the section "5. Failure modes" of the incident report of equipment OUEST1-INV08 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. For each failure mode, in this order: "Incendie toiture et panneaux PV"; "Dégradation et court-circuit câblage"; "Incendie bâtiment support PV"; "Dommages superficiels modules PV"; "Défaillance chaîne et boîtier de jonction"; "Remplacement préventif connecteurs"; "Salissure et nettoyage modules PV", give (a) its probable physical mechanism on a PV inverter and its DC field, and (b) the evidence on this equipment — incidents (only from that failure mode's `incidents`), dates, severity, cost, recurrences — and its impact.

Statistics and figure data for this section (every value is already computed):
```json
{
 "failure_modes": [
  {
   "failure_mode": "Incendie toiture et panneaux PV",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 25.3% of the equipment cost",
   "n_incidents": 1,
   "n_moderate": 0,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 48714,
   "cost_mean_eur": 48714,
   "cost_share_pct": 25.3,
   "downtime_total_h": 99.2,
   "first_date": "2024-07-05",
   "last_date": "2024-07-05",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 6.7,
   "share_of_site_incidents_pct": 15.9,
   "representation": "under-represented vs site",
   "weather_counts": {
    "conditions nominales": 1
   },
   "dominant_weather": [
    "conditions nominales"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#7",
     "date": "2024-07-05",
     "severity": "sévère",
     "cost_eur": 48714,
     "downtime_h": 99.2,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Dégradation et court-circuit câblage",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 1 recurrence(s) within 90 days",
   "n_incidents": 2,
   "n_moderate": 1,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 36150,
   "cost_mean_eur": 18075,
   "cost_share_pct": 18.8,
   "downtime_total_h": 80.4,
   "first_date": "2025-06-20",
   "last_date": "2025-07-14",
   "median_days_between_recurrences": 24,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 13.3,
   "share_of_site_incidents_pct": 14.4,
   "representation": "in line with site",
   "weather_counts": {
    "vent modéré": 1,
    "pluie modérée": 1
   },
   "dominant_weather": [
    "vent modéré",
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#12",
     "date": "2025-06-20",
     "severity": "sévère",
     "cost_eur": 26429,
     "downtime_h": 55.8,
     "weather_condition": "vent modéré"
    },
    {
     "ref": "#15",
     "date": "2025-07-14",
     "severity": "modérée",
     "cost_eur": 9721,
     "downtime_h": 24.6,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Incendie bâtiment support PV",
   "recommendation_priority": "P2",
   "priority_reason": "1 severe incident(s), 17.9% of the cost, no recurrence within 90 days",
   "n_incidents": 1,
   "n_moderate": 0,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 34465,
   "cost_mean_eur": 34465,
   "cost_share_pct": 17.9,
   "downtime_total_h": 60.7,
   "first_date": "2023-08-06",
   "last_date": "2023-08-06",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 6.7,
   "share_of_site_incidents_pct": 6.1,
   "representation": "in line with site",
   "weather_counts": {
    "ciel dégagé": 1
   },
   "dominant_weather": [
    "ciel dégagé"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#5",
     "date": "2023-08-06",
     "severity": "sévère",
     "cost_eur": 34465,
     "downtime_h": 60.7,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Dommages superficiels modules PV",
   "recommendation_priority": "P2",
   "priority_reason": "no severe incident but 13.7% of the equipment cost",
   "n_incidents": 5,
   "n_moderate": 5,
   "n_severe": 0,
   "sample": "ok",
   "cost_total_eur": 26364,
   "cost_mean_eur": 5273,
   "cost_share_pct": 13.7,
   "downtime_total_h": 73.6,
   "first_date": "2023-04-15",
   "last_date": "2025-07-09",
   "median_days_between_recurrences": 142,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 33.3,
   "share_of_site_incidents_pct": 28.0,
   "representation": "in line with site",
   "weather_counts": {
    "vent fort / tempête": 2,
    "orage avec grêle": 3
   },
   "dominant_weather": [
    "orage avec grêle"
   ],
   "dominant_weather_share_pct": 60.0,
   "incidents": [
    {
     "ref": "#2",
     "date": "2023-04-15",
     "severity": "modérée",
     "cost_eur": 3355,
     "downtime_h": 10.5,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#8",
     "date": "2024-09-26",
     "severity": "modérée",
     "cost_eur": 8671,
     "downtime_h": 22.7,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#9",
     "date": "2025-02-11",
     "severity": "modérée",
     "cost_eur": 4961,
     "downtime_h": 12.9,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#13",
     "date": "2025-07-08",
     "severity": "modérée",
     "cost_eur": 6266,
     "downtime_h": 17.4,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#14",
     "date": "2025-07-09",
     "severity": "modérée",
     "cost_eur": 3110,
     "downtime_h": 10.1,
     "weather_condition": "orage avec grêle"
    }
   ]
  },
  {
   "failure_mode": "Défaillance chaîne et boîtier de jonction",
   "recommendation_priority": "P2",
   "priority_reason": "2 severe incident(s), 13.0% of the cost, no recurrence within 90 days",
   "n_incidents": 2,
   "n_moderate": 0,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 25010,
   "cost_mean_eur": 12505,
   "cost_share_pct": 13.0,
   "downtime_total_h": 46.9,
   "first_date": "2023-02-28",
   "last_date": "2023-10-15",
   "median_days_between_recurrences": 229,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 13.3,
   "share_of_site_incidents_pct": 7.6,
   "representation": "over-represented vs site",
   "weather_counts": {
    "ciel dégagé": 1,
    "conditions nominales": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "conditions nominales"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#1",
     "date": "2023-02-28",
     "severity": "sévère",
     "cost_eur": 14647,
     "downtime_h": 25.1,
     "weather_condition": "conditions nominales"
    },
    {
     "ref": "#6",
     "date": "2023-10-15",
     "severity": "sévère",
     "cost_eur": 10363,
     "downtime_h": 21.8,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Remplacement préventif connecteurs",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 8.1% of the cost",
   "n_incidents": 3,
   "n_moderate": 3,
   "n_severe": 0,
   "sample": "ok",
   "cost_total_eur": 15573,
   "cost_mean_eur": 5191,
   "cost_share_pct": 8.1,
   "downtime_total_h": 44.7,
   "first_date": "2023-06-05",
   "last_date": "2025-02-19",
   "median_days_between_recurrences": 312,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 20.0,
   "share_of_site_incidents_pct": 11.4,
   "representation": "over-represented vs site",
   "weather_counts": {
    "ciel dégagé": 1,
    "temps calme": 1,
    "vent modéré": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "temps calme",
    "vent modéré"
   ],
   "dominant_weather_share_pct": 33.3,
   "incidents": [
    {
     "ref": "#3",
     "date": "2023-06-05",
     "severity": "modérée",
     "cost_eur": 4703,
     "downtime_h": 15.5,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#4",
     "date": "2023-06-19",
     "severity": "modérée",
     "cost_eur": 4156,
     "downtime_h": 10.6,
     "weather_condition": "vent modéré"
    },
    {
     "ref": "#10",
     "date": "2025-02-19",
     "severity": "modérée",
     "cost_eur": 6713,
     "downtime_h": 18.6,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Salissure et nettoyage modules PV",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 3.2% of the cost",
   "n_incidents": 1,
   "n_moderate": 1,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 6080,
   "cost_mean_eur": 6080,
   "cost_share_pct": 3.2,
   "downtime_total_h": 18.5,
   "first_date": "2025-02-28",
   "last_date": "2025-02-28",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 6.7,
   "share_of_site_incidents_pct": 7.6,
   "representation": "in line with site",
   "weather_counts": {
    "conditions nominales": 1
   },
   "dominant_weather": [
    "conditions nominales"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#11",
     "date": "2025-02-28",
     "severity": "modérée",
     "cost_eur": 6080,
     "downtime_h": 18.5,
     "weather_condition": "conditions nominales"
    }
   ]
  }
 ],
 "facts": [
  "Incendie toiture et panneaux PV: priority P1 (1 severe incident(s) + 25.3% of the equipment cost).",
  "Dégradation et court-circuit câblage: priority P1 (1 severe incident(s) + 1 recurrence(s) within 90 days).",
  "Incendie bâtiment support PV: priority P2 (1 severe incident(s), 17.9% of the cost, no recurrence within 90 days).",
  "Dommages superficiels modules PV: priority P2 (no severe incident but 13.7% of the equipment cost).",
  "Défaillance chaîne et boîtier de jonction: priority P2 (2 severe incident(s), 13.0% of the cost, no recurrence within 90 days).",
  "Remplacement préventif connecteurs: priority P3 (no severe incident and 8.1% of the cost).",
  "Salissure et nettoyage modules PV: priority P3 (no severe incident and 3.2% of the cost)."
 ]
}
```
