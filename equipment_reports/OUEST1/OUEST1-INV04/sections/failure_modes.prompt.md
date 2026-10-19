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

You are writing the section "5. Failure modes" of the incident report of equipment OUEST1-INV04 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. For each failure mode, in this order: "Dégradation et court-circuit câblage"; "Salissure et nettoyage modules PV"; "Défaillance chaîne et boîtier de jonction"; "Incendie toiture et panneaux PV"; "Dommages superficiels modules PV"; "Remplacement préventif connecteurs", give (a) its probable physical mechanism on a PV inverter and its DC field, and (b) the evidence on this equipment — incidents (only from that failure mode's `incidents`), dates, severity, cost, recurrences — and its impact.

Statistics and figure data for this section (every value is already computed):
```json
{
 "failure_modes": [
  {
   "failure_mode": "Dégradation et court-circuit câblage",
   "recommendation_priority": "P1",
   "priority_reason": "2 severe incident(s) + 38.1% of the equipment cost + 1 recurrence(s) within 90 days",
   "n_incidents": 3,
   "n_moderate": 1,
   "n_severe": 2,
   "sample": "ok",
   "cost_total_eur": 88376,
   "cost_mean_eur": 29459,
   "cost_share_pct": 38.1,
   "downtime_total_h": 163.3,
   "first_date": "2023-05-30",
   "last_date": "2024-02-18",
   "median_days_between_recurrences": 132,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 18.8,
   "share_of_site_incidents_pct": 14.4,
   "representation": "over-represented vs site",
   "weather_counts": {
    "pluie modérée": 3
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#1",
     "date": "2023-05-30",
     "severity": "sévère",
     "cost_eur": 40158,
     "downtime_h": 68.0,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#2",
     "date": "2023-06-22",
     "severity": "sévère",
     "cost_eur": 40740,
     "downtime_h": 71.6,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#6",
     "date": "2024-02-18",
     "severity": "modérée",
     "cost_eur": 7477,
     "downtime_h": 23.7,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Salissure et nettoyage modules PV",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 25.9% of the equipment cost + 1 recurrence(s) within 90 days",
   "n_incidents": 2,
   "n_moderate": 1,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 60105,
   "cost_mean_eur": 30052,
   "cost_share_pct": 25.9,
   "downtime_total_h": 102.3,
   "first_date": "2025-07-23",
   "last_date": "2025-07-23",
   "median_days_between_recurrences": 0,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 12.5,
   "share_of_site_incidents_pct": 7.6,
   "representation": "over-represented vs site",
   "weather_counts": {
    "conditions nominales": 1,
    "pluie modérée": 1
   },
   "dominant_weather": [
    "conditions nominales",
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#12",
     "date": "2025-07-23",
     "severity": "modérée",
     "cost_eur": 4179,
     "downtime_h": 13.5,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#13",
     "date": "2025-07-23",
     "severity": "sévère",
     "cost_eur": 55925,
     "downtime_h": 88.8,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Défaillance chaîne et boîtier de jonction",
   "recommendation_priority": "P2",
   "priority_reason": "1 severe incident(s), 13.4% of the cost, no recurrence within 90 days",
   "n_incidents": 1,
   "n_moderate": 0,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 31133,
   "cost_mean_eur": 31133,
   "cost_share_pct": 13.4,
   "downtime_total_h": 68.0,
   "first_date": "2024-07-24",
   "last_date": "2024-07-24",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 6.2,
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
     "ref": "#9",
     "date": "2024-07-24",
     "severity": "sévère",
     "cost_eur": 31133,
     "downtime_h": 68.0,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Incendie toiture et panneaux PV",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 8.8% of the cost",
   "n_incidents": 4,
   "n_moderate": 4,
   "n_severe": 0,
   "sample": "ok",
   "cost_total_eur": 20423,
   "cost_mean_eur": 5106,
   "cost_share_pct": 8.8,
   "downtime_total_h": 65.1,
   "first_date": "2023-07-17",
   "last_date": "2025-07-26",
   "median_days_between_recurrences": 288,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 25.0,
   "share_of_site_incidents_pct": 15.9,
   "representation": "over-represented vs site",
   "weather_counts": {
    "ciel dégagé": 1,
    "temps calme": 3
   },
   "dominant_weather": [
    "temps calme"
   ],
   "dominant_weather_share_pct": 75.0,
   "incidents": [
    {
     "ref": "#3",
     "date": "2023-07-17",
     "severity": "modérée",
     "cost_eur": 3207,
     "downtime_h": 10.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#7",
     "date": "2024-05-31",
     "severity": "modérée",
     "cost_eur": 6401,
     "downtime_h": 22.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#10",
     "date": "2025-03-15",
     "severity": "modérée",
     "cost_eur": 3009,
     "downtime_h": 9.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#14",
     "date": "2025-07-26",
     "severity": "modérée",
     "cost_eur": 7805,
     "downtime_h": 22.3,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Dommages superficiels modules PV",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 7.4% of the cost",
   "n_incidents": 3,
   "n_moderate": 3,
   "n_severe": 0,
   "sample": "ok",
   "cost_total_eur": 17146,
   "cost_mean_eur": 5715,
   "cost_share_pct": 7.4,
   "downtime_total_h": 51.5,
   "first_date": "2025-06-11",
   "last_date": "2025-12-08",
   "median_days_between_recurrences": 90,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 18.8,
   "share_of_site_incidents_pct": 28.0,
   "representation": "under-represented vs site",
   "weather_counts": {
    "vent fort / tempête": 1,
    "orage avec grêle": 2
   },
   "dominant_weather": [
    "orage avec grêle"
   ],
   "dominant_weather_share_pct": 66.7,
   "incidents": [
    {
     "ref": "#11",
     "date": "2025-06-11",
     "severity": "modérée",
     "cost_eur": 6986,
     "downtime_h": 21.1,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#15",
     "date": "2025-08-03",
     "severity": "modérée",
     "cost_eur": 4023,
     "downtime_h": 10.8,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#16",
     "date": "2025-12-08",
     "severity": "modérée",
     "cost_eur": 6137,
     "downtime_h": 19.6,
     "weather_condition": "orage avec grêle"
    }
   ]
  },
  {
   "failure_mode": "Remplacement préventif connecteurs",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 6.4% of the cost",
   "n_incidents": 3,
   "n_moderate": 3,
   "n_severe": 0,
   "sample": "ok",
   "cost_total_eur": 14953,
   "cost_mean_eur": 4984,
   "cost_share_pct": 6.4,
   "downtime_total_h": 44.4,
   "first_date": "2023-10-25",
   "last_date": "2024-07-20",
   "median_days_between_recurrences": 134,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 18.8,
   "share_of_site_incidents_pct": 11.4,
   "representation": "over-represented vs site",
   "weather_counts": {
    "ciel dégagé": 1,
    "temps calme": 2
   },
   "dominant_weather": [
    "temps calme"
   ],
   "dominant_weather_share_pct": 66.7,
   "incidents": [
    {
     "ref": "#4",
     "date": "2023-10-25",
     "severity": "modérée",
     "cost_eur": 3778,
     "downtime_h": 13.4,
     "weather_condition": "ciel dégagé"
    },
    {
     "ref": "#5",
     "date": "2024-01-03",
     "severity": "modérée",
     "cost_eur": 7390,
     "downtime_h": 19.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#8",
     "date": "2024-07-20",
     "severity": "modérée",
     "cost_eur": 3785,
     "downtime_h": 11.4,
     "weather_condition": "temps calme"
    }
   ]
  }
 ],
 "facts": [
  "Dégradation et court-circuit câblage: priority P1 (2 severe incident(s) + 38.1% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Salissure et nettoyage modules PV: priority P1 (1 severe incident(s) + 25.9% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Défaillance chaîne et boîtier de jonction: priority P2 (1 severe incident(s), 13.4% of the cost, no recurrence within 90 days).",
  "Incendie toiture et panneaux PV: priority P3 (no severe incident and 8.8% of the cost).",
  "Dommages superficiels modules PV: priority P3 (no severe incident and 7.4% of the cost).",
  "Remplacement préventif connecteurs: priority P3 (no severe incident and 6.4% of the cost)."
 ]
}
```
