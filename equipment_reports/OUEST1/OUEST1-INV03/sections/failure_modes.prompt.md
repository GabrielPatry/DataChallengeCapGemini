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

You are writing the section "5. Failure modes" of the incident report of equipment OUEST1-INV03 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. For each failure mode, in this order: "Dégradation et court-circuit câblage"; "Dommages superficiels modules PV"; "Baisse de rendement onduleur"; "Incendie toiture et panneaux PV"; "Incendie bâtiment support PV"; "Remplacement préventif connecteurs"; "Salissure et nettoyage modules PV", give (a) its probable physical mechanism on a PV inverter and its DC field, and (b) the evidence on this equipment — incidents (only from that failure mode's `incidents`), dates, severity, cost, recurrences — and its impact.

Statistics and figure data for this section (every value is already computed):
```json
{
 "failure_modes": [
  {
   "failure_mode": "Dégradation et court-circuit câblage",
   "recommendation_priority": "P1",
   "priority_reason": "2 severe incident(s) + 34.4% of the equipment cost + 1 recurrence(s) within 90 days",
   "n_incidents": 2,
   "n_moderate": 0,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 97989,
   "cost_mean_eur": 48994,
   "cost_share_pct": 34.4,
   "downtime_total_h": 170.1,
   "first_date": "2023-11-05",
   "last_date": "2024-01-22",
   "median_days_between_recurrences": 78,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 15.4,
   "share_of_site_incidents_pct": 14.4,
   "representation": "in line with site",
   "weather_counts": {
    "ciel dégagé": 1,
    "vent modéré": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "vent modéré"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#3",
     "date": "2023-11-05",
     "severity": "sévère",
     "cost_eur": 43675,
     "downtime_h": 78.3,
     "weather_condition": "vent modéré"
    },
    {
     "ref": "#4",
     "date": "2024-01-22",
     "severity": "sévère",
     "cost_eur": 54313,
     "downtime_h": 91.8,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Dommages superficiels modules PV",
   "recommendation_priority": "P1",
   "priority_reason": "2 severe incident(s) + 24.7% of the equipment cost + 1 recurrence(s) within 90 days",
   "n_incidents": 4,
   "n_moderate": 2,
   "n_severe": 2,
   "sample": "ok",
   "cost_total_eur": 70510,
   "cost_mean_eur": 17627,
   "cost_share_pct": 24.7,
   "downtime_total_h": 153.6,
   "first_date": "2023-09-21",
   "last_date": "2025-02-28",
   "median_days_between_recurrences": 142,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 30.8,
   "share_of_site_incidents_pct": 28.0,
   "representation": "in line with site",
   "weather_counts": {
    "vent fort / tempête": 3,
    "orage avec grêle": 1
   },
   "dominant_weather": [
    "vent fort / tempête"
   ],
   "dominant_weather_share_pct": 75.0,
   "incidents": [
    {
     "ref": "#2",
     "date": "2023-09-21",
     "severity": "modérée",
     "cost_eur": 3870,
     "downtime_h": 13.7,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#5",
     "date": "2024-02-10",
     "severity": "sévère",
     "cost_eur": 37539,
     "downtime_h": 74.0,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#8",
     "date": "2025-01-17",
     "severity": "sévère",
     "cost_eur": 25134,
     "downtime_h": 51.9,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#9",
     "date": "2025-02-28",
     "severity": "modérée",
     "cost_eur": 3967,
     "downtime_h": 14.0,
     "weather_condition": "vent fort / tempête"
    }
   ]
  },
  {
   "failure_mode": "Baisse de rendement onduleur",
   "recommendation_priority": "P2",
   "priority_reason": "2 severe incident(s), 18.0% of the cost, no recurrence within 90 days",
   "n_incidents": 2,
   "n_moderate": 0,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 51357,
   "cost_mean_eur": 25678,
   "cost_share_pct": 18.0,
   "downtime_total_h": 93.1,
   "first_date": "2025-06-21",
   "last_date": "2025-11-27",
   "median_days_between_recurrences": 159,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 15.4,
   "share_of_site_incidents_pct": 9.1,
   "representation": "over-represented vs site",
   "weather_counts": {
    "ciel dégagé": 1,
    "temps calme": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "temps calme"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#10",
     "date": "2025-06-21",
     "severity": "sévère",
     "cost_eur": 38931,
     "downtime_h": 67.2,
     "weather_condition": "ciel dégagé"
    },
    {
     "ref": "#13",
     "date": "2025-11-27",
     "severity": "sévère",
     "cost_eur": 12425,
     "downtime_h": 25.9,
     "weather_condition": "temps calme"
    }
   ]
  },
  {
   "failure_mode": "Incendie toiture et panneaux PV",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 1 recurrence(s) within 90 days",
   "n_incidents": 2,
   "n_moderate": 1,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 34127,
   "cost_mean_eur": 17064,
   "cost_share_pct": 12.0,
   "downtime_total_h": 65.0,
   "first_date": "2025-07-24",
   "last_date": "2025-08-19",
   "median_days_between_recurrences": 26,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 15.4,
   "share_of_site_incidents_pct": 15.9,
   "representation": "in line with site",
   "weather_counts": {
    "conditions nominales": 1,
    "temps calme": 1
   },
   "dominant_weather": [
    "conditions nominales",
    "temps calme"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#11",
     "date": "2025-07-24",
     "severity": "sévère",
     "cost_eur": 27461,
     "downtime_h": 46.5,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#12",
     "date": "2025-08-19",
     "severity": "modérée",
     "cost_eur": 6667,
     "downtime_h": 18.5,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Incendie bâtiment support PV",
   "recommendation_priority": "P2",
   "priority_reason": "1 severe incident(s), 7.4% of the cost, no recurrence within 90 days",
   "n_incidents": 1,
   "n_moderate": 0,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 21116,
   "cost_mean_eur": 21116,
   "cost_share_pct": 7.4,
   "downtime_total_h": 41.4,
   "first_date": "2023-03-23",
   "last_date": "2023-03-23",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 7.7,
   "share_of_site_incidents_pct": 6.1,
   "representation": "in line with site",
   "weather_counts": {
    "temps calme": 1
   },
   "dominant_weather": [
    "temps calme"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#1",
     "date": "2023-03-23",
     "severity": "sévère",
     "cost_eur": 21116,
     "downtime_h": 41.4,
     "weather_condition": "temps calme"
    }
   ]
  },
  {
   "failure_mode": "Remplacement préventif connecteurs",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 2.8% of the cost",
   "n_incidents": 1,
   "n_moderate": 1,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 7961,
   "cost_mean_eur": 7961,
   "cost_share_pct": 2.8,
   "downtime_total_h": 24.0,
   "first_date": "2024-02-26",
   "last_date": "2024-02-26",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 7.7,
   "share_of_site_incidents_pct": 11.4,
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
     "ref": "#6",
     "date": "2024-02-26",
     "severity": "modérée",
     "cost_eur": 7961,
     "downtime_h": 24.0,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Salissure et nettoyage modules PV",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 0.7% of the cost",
   "n_incidents": 1,
   "n_moderate": 1,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 2006,
   "cost_mean_eur": 2006,
   "cost_share_pct": 0.7,
   "downtime_total_h": 6.5,
   "first_date": "2024-11-26",
   "last_date": "2024-11-26",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 7.7,
   "share_of_site_incidents_pct": 7.6,
   "representation": "in line with site",
   "weather_counts": {
    "pluie modérée": 1
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#7",
     "date": "2024-11-26",
     "severity": "modérée",
     "cost_eur": 2006,
     "downtime_h": 6.5,
     "weather_condition": "pluie modérée"
    }
   ]
  }
 ],
 "facts": [
  "Dégradation et court-circuit câblage: priority P1 (2 severe incident(s) + 34.4% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Dommages superficiels modules PV: priority P1 (2 severe incident(s) + 24.7% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Baisse de rendement onduleur: priority P2 (2 severe incident(s), 18.0% of the cost, no recurrence within 90 days).",
  "Incendie toiture et panneaux PV: priority P1 (1 severe incident(s) + 1 recurrence(s) within 90 days).",
  "Incendie bâtiment support PV: priority P2 (1 severe incident(s), 7.4% of the cost, no recurrence within 90 days).",
  "Remplacement préventif connecteurs: priority P3 (no severe incident and 2.8% of the cost).",
  "Salissure et nettoyage modules PV: priority P3 (no severe incident and 0.7% of the cost)."
 ]
}
```
