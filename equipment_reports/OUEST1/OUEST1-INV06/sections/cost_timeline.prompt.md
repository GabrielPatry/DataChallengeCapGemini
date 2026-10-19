# System

You are a reliability engineer who analyses the cost history and recurrence of incidents on PV inverters.

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

You are writing the section "3. Cost timeline" of the incident report of equipment OUEST1-INV06 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. How did the number of incidents and their cost evolve year by year? Comment on every year, including the change in the last year, using the year-on-year changes given.
2. Which incidents dominate the cost (`most_costly_incidents`) and what are their failure modes?
3. Are there close sequences of incidents or quick recurrences of the same failure mode? Name the incidents and failure modes involved.
4. Is there a seasonal pattern? Flag seasons with few incidents as indicative.

Statistics and figure data for this section (every value is already computed):
```json
{
 "cost_timeline_figure": {
  "figure": "Cost timeline of moderate and severe incidents",
  "how_to_read": "One point per incident, in chronological order; the three most costly incidents are labelled on the figure.",
  "labelled_incidents": [
   "#11",
   "#4",
   "#12"
  ],
  "points": [
   {
    "ref": "#1",
    "date": "2023-05-18",
    "severity": "modérée",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 5297,
    "downtime_h": 14.5,
    "weather_condition": "vent modéré",
    "days_since_previous_incident": null,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#2",
    "date": "2023-07-01",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 1733,
    "downtime_h": 5.2,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 44,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#3",
    "date": "2023-07-02",
    "severity": "sévère",
    "failure_mode": "Défaillance chaîne et boîtier de jonction",
    "cost_eur": 36364,
    "downtime_h": 78.0,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 1,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#4",
    "date": "2023-10-24",
    "severity": "sévère",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 43919,
    "downtime_h": 86.9,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": 114,
    "days_since_previous_same_failure_mode": 115
   },
   {
    "ref": "#5",
    "date": "2023-11-19",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 1635,
    "downtime_h": 4.8,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 26,
    "days_since_previous_same_failure_mode": 26
   },
   {
    "ref": "#6",
    "date": "2023-12-08",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 9267,
    "downtime_h": 18.8,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 19,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#7",
    "date": "2024-02-14",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 32669,
    "downtime_h": 57.5,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 68,
    "days_since_previous_same_failure_mode": 68
   },
   {
    "ref": "#8",
    "date": "2024-05-09",
    "severity": "sévère",
    "failure_mode": "Défaillance chaîne et boîtier de jonction",
    "cost_eur": 41138,
    "downtime_h": 67.5,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 85,
    "days_since_previous_same_failure_mode": 312
   },
   {
    "ref": "#9",
    "date": "2024-06-19",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 2359,
    "downtime_h": 7.0,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 41,
    "days_since_previous_same_failure_mode": 126
   },
   {
    "ref": "#10",
    "date": "2024-08-21",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 4298,
    "downtime_h": 12.0,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 63,
    "days_since_previous_same_failure_mode": 276
   },
   {
    "ref": "#11",
    "date": "2024-11-26",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 60221,
    "downtime_h": 98.3,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 97,
    "days_since_previous_same_failure_mode": 160
   },
   {
    "ref": "#12",
    "date": "2025-01-10",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 41211,
    "downtime_h": 73.5,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 45,
    "days_since_previous_same_failure_mode": 45
   },
   {
    "ref": "#13",
    "date": "2025-02-17",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 4412,
    "downtime_h": 13.1,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 38,
    "days_since_previous_same_failure_mode": 180
   },
   {
    "ref": "#14",
    "date": "2025-04-03",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 40943,
    "downtime_h": 86.2,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 45,
    "days_since_previous_same_failure_mode": 83
   },
   {
    "ref": "#15",
    "date": "2025-04-30",
    "severity": "modérée",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 3540,
    "downtime_h": 11.7,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 27,
    "days_since_previous_same_failure_mode": 713
   },
   {
    "ref": "#16",
    "date": "2025-06-15",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 5529,
    "downtime_h": 14.4,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 46,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#17",
    "date": "2025-08-10",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 5137,
    "downtime_h": 13.0,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 56,
    "days_since_previous_same_failure_mode": 129
   },
   {
    "ref": "#18",
    "date": "2025-08-17",
    "severity": "modérée",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 2669,
    "downtime_h": 8.7,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": 7,
    "days_since_previous_same_failure_mode": 109
   },
   {
    "ref": "#19",
    "date": "2025-09-02",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 41132,
    "downtime_h": 74.6,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 16,
    "days_since_previous_same_failure_mode": 23
   },
   {
    "ref": "#20",
    "date": "2025-12-26",
    "severity": "modérée",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 5501,
    "downtime_h": 16.5,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 115,
    "days_since_previous_same_failure_mode": 131
   }
  ]
 },
 "yearly_trend": {
  "by_year": [
   {
    "year": 2023,
    "n_incidents": 6,
    "n_severe": 3,
    "cost_eur": 98215,
    "downtime_h": 208.2,
    "cost_change_vs_previous_year_pct": null,
    "incident_count_change_vs_previous_year": null
   },
   {
    "year": 2024,
    "n_incidents": 5,
    "n_severe": 3,
    "cost_eur": 140685,
    "downtime_h": 242.3,
    "cost_change_vs_previous_year_pct": 43.2,
    "incident_count_change_vs_previous_year": -1
   },
   {
    "year": 2025,
    "n_incidents": 9,
    "n_severe": 3,
    "cost_eur": 150075,
    "downtime_h": 311.7,
    "cost_change_vs_previous_year_pct": 6.7,
    "incident_count_change_vs_previous_year": 4
   }
  ],
  "overall": {
   "first_year": 2023,
   "last_year": 2025,
   "cost_change_first_to_last_year_pct": 52.8,
   "label": "increasing"
  }
 },
 "seasonality": [
  {
   "season": "winter",
   "n_incidents": 5,
   "n_severe": 3,
   "cost_eur": 93060,
   "downtime_h": 179.4,
   "sample": "ok"
  },
  {
   "season": "spring",
   "n_incidents": 4,
   "n_severe": 2,
   "cost_eur": 90919,
   "downtime_h": 179.9,
   "sample": "ok"
  },
  {
   "season": "summer",
   "n_incidents": 7,
   "n_severe": 1,
   "cost_eur": 58089,
   "downtime_h": 138.3,
   "sample": "ok"
  },
  {
   "season": "autumn",
   "n_incidents": 4,
   "n_severe": 3,
   "cost_eur": 146907,
   "downtime_h": 264.6,
   "sample": "ok"
  }
 ],
 "most_costly_incidents": {
  "incidents": [
   {
    "ref": "#11",
    "date": "2024-11-26",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "weather_condition": "vent fort / tempête",
    "cost_eur": 60221,
    "downtime_h": 98.3,
    "share_of_total_cost_pct": 15.5
   },
   {
    "ref": "#4",
    "date": "2023-10-24",
    "severity": "sévère",
    "failure_mode": "Incendie toiture et panneaux PV",
    "weather_condition": "conditions nominales",
    "cost_eur": 43919,
    "downtime_h": 86.9,
    "share_of_total_cost_pct": 11.3
   },
   {
    "ref": "#12",
    "date": "2025-01-10",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "weather_condition": "vent fort / tempête",
    "cost_eur": 41211,
    "downtime_h": 73.5,
    "share_of_total_cost_pct": 10.6
   }
  ],
  "top3_combined_cost_eur": 145351,
  "top3_combined_share_of_total_cost_pct": 37.4
 },
 "close_sequences_within_30_days": [
  {
   "incidents": [
    "#2",
    "#3"
   ],
   "from": "2023-07-01",
   "to": "2023-07-02",
   "span_days": 1,
   "n_severe": 1,
   "combined_cost_eur": 38096,
   "failure_modes": [
    "Défaillance chaîne et boîtier de jonction",
    "Incendie toiture et panneaux PV"
   ]
  },
  {
   "incidents": [
    "#4",
    "#5",
    "#6"
   ],
   "from": "2023-10-24",
   "to": "2023-12-08",
   "span_days": 45,
   "n_severe": 2,
   "combined_cost_eur": 54821,
   "failure_modes": [
    "Dommages superficiels modules PV",
    "Incendie toiture et panneaux PV"
   ]
  },
  {
   "incidents": [
    "#14",
    "#15"
   ],
   "from": "2025-04-03",
   "to": "2025-04-30",
   "span_days": 27,
   "n_severe": 1,
   "combined_cost_eur": 44483,
   "failure_modes": [
    "Dommages superficiels modules PV",
    "Dégradation et court-circuit câblage"
   ]
  },
  {
   "incidents": [
    "#17",
    "#18",
    "#19"
   ],
   "from": "2025-08-10",
   "to": "2025-09-02",
   "span_days": 23,
   "n_severe": 1,
   "combined_cost_eur": 48938,
   "failure_modes": [
    "Dommages superficiels modules PV",
    "Dégradation et court-circuit câblage"
   ]
  }
 ],
 "facts": [
  "2023: 6 incident(s) (3 severe), 98 215 EUR.",
  "2024: 5 incident(s) (3 severe), 140 685 EUR (+43.2% vs previous year).",
  "2025: 9 incident(s) (3 severe), 150 075 EUR (+6.7% vs previous year).",
  "From 2023 to 2025 the cost changed by +52.8% (trend: increasing).",
  "The most costly single incident is #11 (Dommages superficiels modules PV, sévère, 2024-11-26): 60 221 EUR, 15.5% of the cost of moderate and severe incidents.",
  "The most costly failure mode is Dommages superficiels modules PV: 232 939 EUR over 8 incident(s), 59.9% of the cost."
 ]
}
```
