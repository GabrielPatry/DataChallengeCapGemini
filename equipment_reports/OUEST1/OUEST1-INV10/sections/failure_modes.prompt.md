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

You are writing the section "5. Failure modes" of the incident report of equipment OUEST1-INV10 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. For each failure mode, in this order: "Incendie bâtiment support PV"; "Dégradation et court-circuit câblage"; "Baisse de rendement onduleur"; "Salissure et nettoyage modules PV"; "Défaillance chaîne et boîtier de jonction"; "Incendie toiture et panneaux PV"; "Dommages superficiels modules PV", give (a) its probable physical mechanism on a PV inverter and its DC field, and (b) the evidence on this equipment — incidents (only from that failure mode's `incidents`), dates, severity, cost, recurrences — and its impact.

Statistics and figure data for this section (every value is already computed):
```json
{
 "failure_modes": [
  {
   "failure_mode": "Incendie bâtiment support PV",
   "recommendation_priority": "P1",
   "priority_reason": "2 severe incident(s) + 24.7% of the equipment cost + 1 recurrence(s) within 90 days",
   "n_incidents": 2,
   "n_moderate": 0,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 51131,
   "cost_mean_eur": 25565,
   "cost_share_pct": 24.7,
   "downtime_total_h": 88.0,
   "first_date": "2024-06-21",
   "last_date": "2024-07-13",
   "median_days_between_recurrences": 22,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 13.3,
   "share_of_site_incidents_pct": 6.1,
   "representation": "over-represented vs site",
   "weather_counts": {
    "temps calme": 1,
    "pluie modérée": 1
   },
   "dominant_weather": [
    "temps calme",
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#9",
     "date": "2024-06-21",
     "severity": "sévère",
     "cost_eur": 13226,
     "downtime_h": 22.5,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#10",
     "date": "2024-07-13",
     "severity": "sévère",
     "cost_eur": 37904,
     "downtime_h": 65.5,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Dégradation et court-circuit câblage",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 23.8% of the equipment cost",
   "n_incidents": 1,
   "n_moderate": 0,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 49142,
   "cost_mean_eur": 49142,
   "cost_share_pct": 23.8,
   "downtime_total_h": 82.4,
   "first_date": "2023-11-21",
   "last_date": "2023-11-21",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 6.7,
   "share_of_site_incidents_pct": 14.4,
   "representation": "under-represented vs site",
   "weather_counts": {
    "temps calme": 1
   },
   "dominant_weather": [
    "temps calme"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#3",
     "date": "2023-11-21",
     "severity": "sévère",
     "cost_eur": 49142,
     "downtime_h": 82.4,
     "weather_condition": "temps calme"
    }
   ]
  },
  {
   "failure_mode": "Baisse de rendement onduleur",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 21.6% of the equipment cost",
   "n_incidents": 4,
   "n_moderate": 3,
   "n_severe": 1,
   "sample": "ok",
   "cost_total_eur": 44568,
   "cost_mean_eur": 11142,
   "cost_share_pct": 21.6,
   "downtime_total_h": 100.2,
   "first_date": "2023-05-15",
   "last_date": "2025-03-18",
   "median_days_between_recurrences": 221,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 26.7,
   "share_of_site_incidents_pct": 9.1,
   "representation": "over-represented vs site",
   "weather_counts": {
    "ciel dégagé": 1,
    "conditions nominales": 1,
    "temps calme": 2
   },
   "dominant_weather": [
    "temps calme"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#1",
     "date": "2023-05-15",
     "severity": "modérée",
     "cost_eur": 7670,
     "downtime_h": 24.0,
     "weather_condition": "conditions nominales"
    },
    {
     "ref": "#4",
     "date": "2023-12-22",
     "severity": "sévère",
     "cost_eur": 24165,
     "downtime_h": 42.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#6",
     "date": "2024-03-23",
     "severity": "modérée",
     "cost_eur": 5780,
     "downtime_h": 14.7,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#12",
     "date": "2025-03-18",
     "severity": "modérée",
     "cost_eur": 6954,
     "downtime_h": 18.9,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Salissure et nettoyage modules PV",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 1 recurrence(s) within 90 days",
   "n_incidents": 4,
   "n_moderate": 3,
   "n_severe": 1,
   "sample": "ok",
   "cost_total_eur": 32044,
   "cost_mean_eur": 8011,
   "cost_share_pct": 15.5,
   "downtime_total_h": 75.9,
   "first_date": "2023-05-18",
   "last_date": "2025-10-23",
   "median_days_between_recurrences": 330,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 26.7,
   "share_of_site_incidents_pct": 7.6,
   "representation": "over-represented vs site",
   "weather_counts": {
    "ciel dégagé": 1,
    "temps calme": 1,
    "vent modéré": 1,
    "pluie modérée": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "temps calme",
    "vent modéré",
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 25.0,
   "incidents": [
    {
     "ref": "#2",
     "date": "2023-05-18",
     "severity": "modérée",
     "cost_eur": 9476,
     "downtime_h": 24.2,
     "weather_condition": "vent modéré"
    },
    {
     "ref": "#7",
     "date": "2024-04-12",
     "severity": "modérée",
     "cost_eur": 6643,
     "downtime_h": 20.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#8",
     "date": "2024-05-22",
     "severity": "sévère",
     "cost_eur": 12817,
     "downtime_h": 21.5,
     "weather_condition": "ciel dégagé"
    },
    {
     "ref": "#15",
     "date": "2025-10-23",
     "severity": "modérée",
     "cost_eur": 3108,
     "downtime_h": 9.6,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Défaillance chaîne et boîtier de jonction",
   "recommendation_priority": "P2",
   "priority_reason": "1 severe incident(s), 8.5% of the cost, no recurrence within 90 days",
   "n_incidents": 1,
   "n_moderate": 0,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 17578,
   "cost_mean_eur": 17578,
   "cost_share_pct": 8.5,
   "downtime_total_h": 28.9,
   "first_date": "2024-10-06",
   "last_date": "2024-10-06",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 6.7,
   "share_of_site_incidents_pct": 7.6,
   "representation": "in line with site",
   "weather_counts": {
    "vent modéré": 1
   },
   "dominant_weather": [
    "vent modéré"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#11",
     "date": "2024-10-06",
     "severity": "sévère",
     "cost_eur": 17578,
     "downtime_h": 28.9,
     "weather_condition": "vent modéré"
    }
   ]
  },
  {
   "failure_mode": "Incendie toiture et panneaux PV",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 4.7% of the cost",
   "n_incidents": 2,
   "n_moderate": 2,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 9760,
   "cost_mean_eur": 4880,
   "cost_share_pct": 4.7,
   "downtime_total_h": 31.6,
   "first_date": "2025-03-22",
   "last_date": "2025-04-10",
   "median_days_between_recurrences": 19,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 13.3,
   "share_of_site_incidents_pct": 15.9,
   "representation": "in line with site",
   "weather_counts": {
    "temps calme": 1,
    "pluie modérée": 1
   },
   "dominant_weather": [
    "temps calme",
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#13",
     "date": "2025-03-22",
     "severity": "modérée",
     "cost_eur": 4506,
     "downtime_h": 13.7,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#14",
     "date": "2025-04-10",
     "severity": "modérée",
     "cost_eur": 5254,
     "downtime_h": 17.9,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Dommages superficiels modules PV",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 1.2% of the cost",
   "n_incidents": 1,
   "n_moderate": 1,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 2540,
   "cost_mean_eur": 2540,
   "cost_share_pct": 1.2,
   "downtime_total_h": 7.0,
   "first_date": "2024-02-26",
   "last_date": "2024-02-26",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 6.7,
   "share_of_site_incidents_pct": 28.0,
   "representation": "under-represented vs site",
   "weather_counts": {
    "vent fort / tempête": 1
   },
   "dominant_weather": [
    "vent fort / tempête"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#5",
     "date": "2024-02-26",
     "severity": "modérée",
     "cost_eur": 2540,
     "downtime_h": 7.0,
     "weather_condition": "vent fort / tempête"
    }
   ]
  }
 ],
 "facts": [
  "Incendie bâtiment support PV: priority P1 (2 severe incident(s) + 24.7% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Dégradation et court-circuit câblage: priority P1 (1 severe incident(s) + 23.8% of the equipment cost).",
  "Baisse de rendement onduleur: priority P1 (1 severe incident(s) + 21.6% of the equipment cost).",
  "Salissure et nettoyage modules PV: priority P1 (1 severe incident(s) + 1 recurrence(s) within 90 days).",
  "Défaillance chaîne et boîtier de jonction: priority P2 (1 severe incident(s), 8.5% of the cost, no recurrence within 90 days).",
  "Incendie toiture et panneaux PV: priority P3 (no severe incident and 4.7% of the cost).",
  "Dommages superficiels modules PV: priority P3 (no severe incident and 1.2% of the cost)."
 ]
}
```
