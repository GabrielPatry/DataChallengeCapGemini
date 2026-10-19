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

You are writing the section "5. Failure modes" of the incident report of equipment OUEST1-INV06 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. For each failure mode, in this order: "Dommages superficiels modules PV"; "Défaillance chaîne et boîtier de jonction"; "Incendie toiture et panneaux PV"; "Dégradation et court-circuit câblage"; "Remplacement préventif connecteurs", give (a) its probable physical mechanism on a PV inverter and its DC field, and (b) the evidence on this equipment — incidents (only from that failure mode's `incidents`), dates, severity, cost, recurrences — and its impact.

Statistics and figure data for this section (every value is already computed):
```json
{
 "failure_modes": [
  {
   "failure_mode": "Dommages superficiels modules PV",
   "recommendation_priority": "P1",
   "priority_reason": "6 severe incident(s) + 59.9% of the equipment cost + 4 recurrence(s) within 90 days",
   "n_incidents": 8,
   "n_moderate": 2,
   "n_severe": 6,
   "sample": "ok",
   "cost_total_eur": 232939,
   "cost_mean_eur": 29117,
   "cost_share_pct": 59.9,
   "downtime_total_h": 428.9,
   "first_date": "2023-12-08",
   "last_date": "2025-09-02",
   "median_days_between_recurrences": 83,
   "recurrences_within_90_days": 4,
   "share_of_equipment_incidents_pct": 40.0,
   "share_of_site_incidents_pct": 28.0,
   "representation": "over-represented vs site",
   "weather_counts": {
    "vent fort / tempête": 4,
    "orage avec grêle": 4
   },
   "dominant_weather": [
    "vent fort / tempête",
    "orage avec grêle"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#6",
     "date": "2023-12-08",
     "severity": "sévère",
     "cost_eur": 9267,
     "downtime_h": 18.8,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#7",
     "date": "2024-02-14",
     "severity": "sévère",
     "cost_eur": 32669,
     "downtime_h": 57.5,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#9",
     "date": "2024-06-19",
     "severity": "modérée",
     "cost_eur": 2359,
     "downtime_h": 7.0,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#11",
     "date": "2024-11-26",
     "severity": "sévère",
     "cost_eur": 60221,
     "downtime_h": 98.3,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#12",
     "date": "2025-01-10",
     "severity": "sévère",
     "cost_eur": 41211,
     "downtime_h": 73.5,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#14",
     "date": "2025-04-03",
     "severity": "sévère",
     "cost_eur": 40943,
     "downtime_h": 86.2,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#17",
     "date": "2025-08-10",
     "severity": "modérée",
     "cost_eur": 5137,
     "downtime_h": 13.0,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#19",
     "date": "2025-09-02",
     "severity": "sévère",
     "cost_eur": 41132,
     "downtime_h": 74.6,
     "weather_condition": "orage avec grêle"
    }
   ]
  },
  {
   "failure_mode": "Défaillance chaîne et boîtier de jonction",
   "recommendation_priority": "P2",
   "priority_reason": "2 severe incident(s), 19.9% of the cost, no recurrence within 90 days",
   "n_incidents": 2,
   "n_moderate": 0,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 77502,
   "cost_mean_eur": 38751,
   "cost_share_pct": 19.9,
   "downtime_total_h": 145.5,
   "first_date": "2023-07-02",
   "last_date": "2024-05-09",
   "median_days_between_recurrences": 312,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 10.0,
   "share_of_site_incidents_pct": 7.6,
   "representation": "over-represented vs site",
   "weather_counts": {
    "pluie modérée": 2
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#3",
     "date": "2023-07-02",
     "severity": "sévère",
     "cost_eur": 36364,
     "downtime_h": 78.0,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#8",
     "date": "2024-05-09",
     "severity": "sévère",
     "cost_eur": 41138,
     "downtime_h": 67.5,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Incendie toiture et panneaux PV",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 1 recurrence(s) within 90 days",
   "n_incidents": 5,
   "n_moderate": 4,
   "n_severe": 1,
   "sample": "ok",
   "cost_total_eur": 55997,
   "cost_mean_eur": 11199,
   "cost_share_pct": 14.4,
   "downtime_total_h": 122.0,
   "first_date": "2023-07-01",
   "last_date": "2025-02-17",
   "median_days_between_recurrences": 148,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 25.0,
   "share_of_site_incidents_pct": 15.9,
   "representation": "over-represented vs site",
   "weather_counts": {
    "conditions nominales": 1,
    "temps calme": 1,
    "pluie modérée": 3
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 60.0,
   "incidents": [
    {
     "ref": "#2",
     "date": "2023-07-01",
     "severity": "modérée",
     "cost_eur": 1733,
     "downtime_h": 5.2,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#4",
     "date": "2023-10-24",
     "severity": "sévère",
     "cost_eur": 43919,
     "downtime_h": 86.9,
     "weather_condition": "conditions nominales"
    },
    {
     "ref": "#5",
     "date": "2023-11-19",
     "severity": "modérée",
     "cost_eur": 1635,
     "downtime_h": 4.8,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#10",
     "date": "2024-08-21",
     "severity": "modérée",
     "cost_eur": 4298,
     "downtime_h": 12.0,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#13",
     "date": "2025-02-17",
     "severity": "modérée",
     "cost_eur": 4412,
     "downtime_h": 13.1,
     "weather_condition": "temps calme"
    }
   ]
  },
  {
   "failure_mode": "Dégradation et court-circuit câblage",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 4.4% of the cost",
   "n_incidents": 4,
   "n_moderate": 4,
   "n_severe": 0,
   "sample": "ok",
   "cost_total_eur": 17007,
   "cost_mean_eur": 4252,
   "cost_share_pct": 4.4,
   "downtime_total_h": 51.4,
   "first_date": "2023-05-18",
   "last_date": "2025-12-26",
   "median_days_between_recurrences": 131,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 20.0,
   "share_of_site_incidents_pct": 14.4,
   "representation": "over-represented vs site",
   "weather_counts": {
    "ciel dégagé": 1,
    "conditions nominales": 1,
    "temps calme": 1,
    "vent modéré": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "conditions nominales",
    "temps calme",
    "vent modéré"
   ],
   "dominant_weather_share_pct": 25.0,
   "incidents": [
    {
     "ref": "#1",
     "date": "2023-05-18",
     "severity": "modérée",
     "cost_eur": 5297,
     "downtime_h": 14.5,
     "weather_condition": "vent modéré"
    },
    {
     "ref": "#15",
     "date": "2025-04-30",
     "severity": "modérée",
     "cost_eur": 3540,
     "downtime_h": 11.7,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#18",
     "date": "2025-08-17",
     "severity": "modérée",
     "cost_eur": 2669,
     "downtime_h": 8.7,
     "weather_condition": "conditions nominales"
    },
    {
     "ref": "#20",
     "date": "2025-12-26",
     "severity": "modérée",
     "cost_eur": 5501,
     "downtime_h": 16.5,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Remplacement préventif connecteurs",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 1.4% of the cost",
   "n_incidents": 1,
   "n_moderate": 1,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 5529,
   "cost_mean_eur": 5529,
   "cost_share_pct": 1.4,
   "downtime_total_h": 14.4,
   "first_date": "2025-06-15",
   "last_date": "2025-06-15",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 5.0,
   "share_of_site_incidents_pct": 11.4,
   "representation": "under-represented vs site",
   "weather_counts": {
    "ciel dégagé": 1
   },
   "dominant_weather": [
    "ciel dégagé"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#16",
     "date": "2025-06-15",
     "severity": "modérée",
     "cost_eur": 5529,
     "downtime_h": 14.4,
     "weather_condition": "ciel dégagé"
    }
   ]
  }
 ],
 "facts": [
  "Dommages superficiels modules PV: priority P1 (6 severe incident(s) + 59.9% of the equipment cost + 4 recurrence(s) within 90 days).",
  "Défaillance chaîne et boîtier de jonction: priority P2 (2 severe incident(s), 19.9% of the cost, no recurrence within 90 days).",
  "Incendie toiture et panneaux PV: priority P1 (1 severe incident(s) + 1 recurrence(s) within 90 days).",
  "Dégradation et court-circuit câblage: priority P3 (no severe incident and 4.4% of the cost).",
  "Remplacement préventif connecteurs: priority P3 (no severe incident and 1.4% of the cost)."
 ]
}
```
