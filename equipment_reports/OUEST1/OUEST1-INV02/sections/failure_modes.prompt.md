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

You are writing the section "5. Failure modes" of the incident report of equipment OUEST1-INV02 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. For each failure mode, in this order: "Dommages superficiels modules PV"; "Dégradation et court-circuit câblage"; "Défaillance chaîne et boîtier de jonction"; "Remplacement préventif connecteurs"; "Baisse de rendement onduleur"; "Incendie toiture et panneaux PV", give (a) its probable physical mechanism on a PV inverter and its DC field, and (b) the evidence on this equipment — incidents (only from that failure mode's `incidents`), dates, severity, cost, recurrences — and its impact.

Statistics and figure data for this section (every value is already computed):
```json
{
 "failure_modes": [
  {
   "failure_mode": "Dommages superficiels modules PV",
   "recommendation_priority": "P1",
   "priority_reason": "2 severe incident(s) + 40.0% of the equipment cost + 1 recurrence(s) within 90 days",
   "n_incidents": 5,
   "n_moderate": 3,
   "n_severe": 2,
   "sample": "ok",
   "cost_total_eur": 91303,
   "cost_mean_eur": 18261,
   "cost_share_pct": 40.0,
   "downtime_total_h": 188.8,
   "first_date": "2023-03-24",
   "last_date": "2025-12-19",
   "median_days_between_recurrences": 147,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 38.5,
   "share_of_site_incidents_pct": 28.0,
   "representation": "over-represented vs site",
   "weather_counts": {
    "vent fort / tempête": 4,
    "orage avec grêle": 1
   },
   "dominant_weather": [
    "vent fort / tempête"
   ],
   "dominant_weather_share_pct": 80.0,
   "incidents": [
    {
     "ref": "#2",
     "date": "2023-03-24",
     "severity": "modérée",
     "cost_eur": 3672,
     "downtime_h": 12.9,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#5",
     "date": "2023-08-17",
     "severity": "sévère",
     "cost_eur": 33875,
     "downtime_h": 56.2,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#6",
     "date": "2023-08-21",
     "severity": "sévère",
     "cost_eur": 44420,
     "downtime_h": 94.0,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#8",
     "date": "2024-01-16",
     "severity": "modérée",
     "cost_eur": 3279,
     "downtime_h": 8.4,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#13",
     "date": "2025-12-19",
     "severity": "modérée",
     "cost_eur": 6057,
     "downtime_h": 17.3,
     "weather_condition": "orage avec grêle"
    }
   ]
  },
  {
   "failure_mode": "Dégradation et court-circuit câblage",
   "recommendation_priority": "P1",
   "priority_reason": "2 severe incident(s) + 37.3% of the equipment cost",
   "n_incidents": 2,
   "n_moderate": 0,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 85092,
   "cost_mean_eur": 42546,
   "cost_share_pct": 37.3,
   "downtime_total_h": 150.6,
   "first_date": "2023-11-30",
   "last_date": "2025-09-05",
   "median_days_between_recurrences": 645,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 15.4,
   "share_of_site_incidents_pct": 14.4,
   "representation": "in line with site",
   "weather_counts": {
    "temps calme": 1,
    "vent modéré": 1
   },
   "dominant_weather": [
    "temps calme",
    "vent modéré"
   ],
   "dominant_weather_share_pct": 50.0,
   "incidents": [
    {
     "ref": "#7",
     "date": "2023-11-30",
     "severity": "sévère",
     "cost_eur": 45736,
     "downtime_h": 77.7,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#11",
     "date": "2025-09-05",
     "severity": "sévère",
     "cost_eur": 39357,
     "downtime_h": 72.9,
     "weather_condition": "vent modéré"
    }
   ]
  },
  {
   "failure_mode": "Défaillance chaîne et boîtier de jonction",
   "recommendation_priority": "P2",
   "priority_reason": "1 severe incident(s), 13.8% of the cost, no recurrence within 90 days",
   "n_incidents": 1,
   "n_moderate": 0,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 31553,
   "cost_mean_eur": 31553,
   "cost_share_pct": 13.8,
   "downtime_total_h": 52.2,
   "first_date": "2024-07-27",
   "last_date": "2024-07-27",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 7.7,
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
     "ref": "#10",
     "date": "2024-07-27",
     "severity": "sévère",
     "cost_eur": 31553,
     "downtime_h": 52.2,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Remplacement préventif connecteurs",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 3.9% of the cost",
   "n_incidents": 2,
   "n_moderate": 2,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 8993,
   "cost_mean_eur": 4496,
   "cost_share_pct": 3.9,
   "downtime_total_h": 28.3,
   "first_date": "2023-05-26",
   "last_date": "2023-07-14",
   "median_days_between_recurrences": 49,
   "recurrences_within_90_days": 1,
   "share_of_equipment_incidents_pct": 15.4,
   "share_of_site_incidents_pct": 11.4,
   "representation": "over-represented vs site",
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
     "date": "2023-05-26",
     "severity": "modérée",
     "cost_eur": 4111,
     "downtime_h": 11.7,
     "weather_condition": "vent modéré"
    },
    {
     "ref": "#4",
     "date": "2023-07-14",
     "severity": "modérée",
     "cost_eur": 4882,
     "downtime_h": 16.6,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Baisse de rendement onduleur",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 3.0% of the cost",
   "n_incidents": 1,
   "n_moderate": 1,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 6780,
   "cost_mean_eur": 6780,
   "cost_share_pct": 3.0,
   "downtime_total_h": 23.3,
   "first_date": "2025-11-30",
   "last_date": "2025-11-30",
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 7.7,
   "share_of_site_incidents_pct": 9.1,
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
     "ref": "#12",
     "date": "2025-11-30",
     "severity": "modérée",
     "cost_eur": 6780,
     "downtime_h": 23.3,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Incendie toiture et panneaux PV",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 1.9% of the cost",
   "n_incidents": 2,
   "n_moderate": 2,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "cost_total_eur": 4446,
   "cost_mean_eur": 2223,
   "cost_share_pct": 1.9,
   "downtime_total_h": 13.0,
   "first_date": "2023-03-03",
   "last_date": "2024-06-22",
   "median_days_between_recurrences": 477,
   "recurrences_within_90_days": 0,
   "share_of_equipment_incidents_pct": 15.4,
   "share_of_site_incidents_pct": 15.9,
   "representation": "in line with site",
   "weather_counts": {
    "pluie modérée": 2
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "dominant_weather_share_pct": 100.0,
   "incidents": [
    {
     "ref": "#1",
     "date": "2023-03-03",
     "severity": "modérée",
     "cost_eur": 2445,
     "downtime_h": 7.4,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#9",
     "date": "2024-06-22",
     "severity": "modérée",
     "cost_eur": 2001,
     "downtime_h": 5.6,
     "weather_condition": "pluie modérée"
    }
   ]
  }
 ],
 "facts": [
  "Dommages superficiels modules PV: priority P1 (2 severe incident(s) + 40.0% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Dégradation et court-circuit câblage: priority P1 (2 severe incident(s) + 37.3% of the equipment cost).",
  "Défaillance chaîne et boîtier de jonction: priority P2 (1 severe incident(s), 13.8% of the cost, no recurrence within 90 days).",
  "Remplacement préventif connecteurs: priority P3 (no severe incident and 3.9% of the cost).",
  "Baisse de rendement onduleur: priority P3 (no severe incident and 3.0% of the cost).",
  "Incendie toiture et panneaux PV: priority P3 (no severe incident and 1.9% of the cost)."
 ]
}
```
