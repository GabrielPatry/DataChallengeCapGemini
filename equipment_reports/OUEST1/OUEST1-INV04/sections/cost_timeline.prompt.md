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

You are writing the section "3. Cost timeline" of the incident report of equipment OUEST1-INV04 (site: Centrale PV Ouest-1).

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
   "#13",
   "#2",
   "#1"
  ],
  "points": [
   {
    "ref": "#1",
    "date": "2023-05-30",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 40158,
    "downtime_h": 68.0,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": null,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#2",
    "date": "2023-06-22",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 40740,
    "downtime_h": 71.6,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 23,
    "days_since_previous_same_failure_mode": 23
   },
   {
    "ref": "#3",
    "date": "2023-07-17",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 3207,
    "downtime_h": 10.6,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 25,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#4",
    "date": "2023-10-25",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 3778,
    "downtime_h": 13.4,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 100,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#5",
    "date": "2024-01-03",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 7390,
    "downtime_h": 19.6,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 70,
    "days_since_previous_same_failure_mode": 70
   },
   {
    "ref": "#6",
    "date": "2024-02-18",
    "severity": "modérée",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 7477,
    "downtime_h": 23.7,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 46,
    "days_since_previous_same_failure_mode": 241
   },
   {
    "ref": "#7",
    "date": "2024-05-31",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 6401,
    "downtime_h": 22.6,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 103,
    "days_since_previous_same_failure_mode": 319
   },
   {
    "ref": "#8",
    "date": "2024-07-20",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 3785,
    "downtime_h": 11.4,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 50,
    "days_since_previous_same_failure_mode": 199
   },
   {
    "ref": "#9",
    "date": "2024-07-24",
    "severity": "sévère",
    "failure_mode": "Défaillance chaîne et boîtier de jonction",
    "cost_eur": 31133,
    "downtime_h": 68.0,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 4,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#10",
    "date": "2025-03-15",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 3009,
    "downtime_h": 9.6,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 234,
    "days_since_previous_same_failure_mode": 288
   },
   {
    "ref": "#11",
    "date": "2025-06-11",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 6986,
    "downtime_h": 21.1,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 88,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#12",
    "date": "2025-07-23",
    "severity": "modérée",
    "failure_mode": "Salissure et nettoyage modules PV",
    "cost_eur": 4179,
    "downtime_h": 13.5,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 42,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#13",
    "date": "2025-07-23",
    "severity": "sévère",
    "failure_mode": "Salissure et nettoyage modules PV",
    "cost_eur": 55925,
    "downtime_h": 88.8,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": 0,
    "days_since_previous_same_failure_mode": 0
   },
   {
    "ref": "#14",
    "date": "2025-07-26",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 7805,
    "downtime_h": 22.3,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 3,
    "days_since_previous_same_failure_mode": 133
   },
   {
    "ref": "#15",
    "date": "2025-08-03",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 4023,
    "downtime_h": 10.8,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 8,
    "days_since_previous_same_failure_mode": 53
   },
   {
    "ref": "#16",
    "date": "2025-12-08",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 6137,
    "downtime_h": 19.6,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 127,
    "days_since_previous_same_failure_mode": 127
   }
  ]
 },
 "yearly_trend": {
  "by_year": [
   {
    "year": 2023,
    "n_incidents": 4,
    "n_severe": 2,
    "cost_eur": 87884,
    "downtime_h": 163.6,
    "cost_change_vs_previous_year_pct": null,
    "incident_count_change_vs_previous_year": null
   },
   {
    "year": 2024,
    "n_incidents": 5,
    "n_severe": 1,
    "cost_eur": 56186,
    "downtime_h": 145.3,
    "cost_change_vs_previous_year_pct": -36.1,
    "incident_count_change_vs_previous_year": 1
   },
   {
    "year": 2025,
    "n_incidents": 7,
    "n_severe": 1,
    "cost_eur": 88065,
    "downtime_h": 185.7,
    "cost_change_vs_previous_year_pct": 56.7,
    "incident_count_change_vs_previous_year": 2
   }
  ],
  "overall": {
   "first_year": 2023,
   "last_year": 2025,
   "cost_change_first_to_last_year_pct": 0.2,
   "label": "stable"
  }
 },
 "seasonality": [
  {
   "season": "winter",
   "n_incidents": 3,
   "n_severe": 0,
   "cost_eur": 21004,
   "downtime_h": 62.9,
   "sample": "ok"
  },
  {
   "season": "spring",
   "n_incidents": 3,
   "n_severe": 1,
   "cost_eur": 49569,
   "downtime_h": 100.2,
   "sample": "ok"
  },
  {
   "season": "summer",
   "n_incidents": 9,
   "n_severe": 3,
   "cost_eur": 157784,
   "downtime_h": 318.1,
   "sample": "ok"
  },
  {
   "season": "autumn",
   "n_incidents": 1,
   "n_severe": 0,
   "cost_eur": 3778,
   "downtime_h": 13.4,
   "sample": "indicative only (fewer than 3 incidents)"
  }
 ],
 "most_costly_incidents": {
  "incidents": [
   {
    "ref": "#13",
    "date": "2025-07-23",
    "severity": "sévère",
    "failure_mode": "Salissure et nettoyage modules PV",
    "weather_condition": "conditions nominales",
    "cost_eur": 55925,
    "downtime_h": 88.8,
    "share_of_total_cost_pct": 24.1
   },
   {
    "ref": "#2",
    "date": "2023-06-22",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "weather_condition": "pluie modérée",
    "cost_eur": 40740,
    "downtime_h": 71.6,
    "share_of_total_cost_pct": 17.6
   },
   {
    "ref": "#1",
    "date": "2023-05-30",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "weather_condition": "pluie modérée",
    "cost_eur": 40158,
    "downtime_h": 68.0,
    "share_of_total_cost_pct": 17.3
   }
  ],
  "top3_combined_cost_eur": 136824,
  "top3_combined_share_of_total_cost_pct": 58.9
 },
 "close_sequences_within_30_days": [
  {
   "incidents": [
    "#1",
    "#2",
    "#3"
   ],
   "from": "2023-05-30",
   "to": "2023-07-17",
   "span_days": 48,
   "n_severe": 2,
   "combined_cost_eur": 84106,
   "failure_modes": [
    "Dégradation et court-circuit câblage",
    "Incendie toiture et panneaux PV"
   ]
  },
  {
   "incidents": [
    "#8",
    "#9"
   ],
   "from": "2024-07-20",
   "to": "2024-07-24",
   "span_days": 4,
   "n_severe": 1,
   "combined_cost_eur": 34918,
   "failure_modes": [
    "Défaillance chaîne et boîtier de jonction",
    "Remplacement préventif connecteurs"
   ]
  },
  {
   "incidents": [
    "#12",
    "#13",
    "#14",
    "#15"
   ],
   "from": "2025-07-23",
   "to": "2025-08-03",
   "span_days": 11,
   "n_severe": 1,
   "combined_cost_eur": 71932,
   "failure_modes": [
    "Dommages superficiels modules PV",
    "Incendie toiture et panneaux PV",
    "Salissure et nettoyage modules PV"
   ]
  }
 ],
 "facts": [
  "2023: 4 incident(s) (2 severe), 87 884 EUR.",
  "2024: 5 incident(s) (1 severe), 56 186 EUR (-36.1% vs previous year).",
  "2025: 7 incident(s) (1 severe), 88 065 EUR (+56.7% vs previous year).",
  "From 2023 to 2025 the cost changed by +0.2% (trend: stable).",
  "The most costly single incident is #13 (Salissure et nettoyage modules PV, sévère, 2025-07-23): 55 925 EUR, 24.1% of the cost of moderate and severe incidents.",
  "The most costly failure mode is Dégradation et court-circuit câblage: 88 376 EUR over 3 incident(s), 38.1% of the cost.",
  "The most costly incident and the most costly failure mode are different: do not attribute one to the other."
 ]
}
```
