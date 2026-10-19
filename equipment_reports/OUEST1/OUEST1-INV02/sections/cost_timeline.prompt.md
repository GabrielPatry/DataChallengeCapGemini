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

You are writing the section "3. Cost timeline" of the incident report of equipment OUEST1-INV02 (site: Centrale PV Ouest-1).

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
   "#7",
   "#6",
   "#11"
  ],
  "points": [
   {
    "ref": "#1",
    "date": "2023-03-03",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 2445,
    "downtime_h": 7.4,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": null,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#2",
    "date": "2023-03-24",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 3672,
    "downtime_h": 12.9,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 21,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#3",
    "date": "2023-05-26",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 4111,
    "downtime_h": 11.7,
    "weather_condition": "vent modéré",
    "days_since_previous_incident": 63,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#4",
    "date": "2023-07-14",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 4882,
    "downtime_h": 16.6,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 49,
    "days_since_previous_same_failure_mode": 49
   },
   {
    "ref": "#5",
    "date": "2023-08-17",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 33875,
    "downtime_h": 56.2,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 34,
    "days_since_previous_same_failure_mode": 146
   },
   {
    "ref": "#6",
    "date": "2023-08-21",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 44420,
    "downtime_h": 94.0,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 4,
    "days_since_previous_same_failure_mode": 4
   },
   {
    "ref": "#7",
    "date": "2023-11-30",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 45736,
    "downtime_h": 77.7,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 101,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#8",
    "date": "2024-01-16",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 3279,
    "downtime_h": 8.4,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 47,
    "days_since_previous_same_failure_mode": 148
   },
   {
    "ref": "#9",
    "date": "2024-06-22",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 2001,
    "downtime_h": 5.6,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 158,
    "days_since_previous_same_failure_mode": 477
   },
   {
    "ref": "#10",
    "date": "2024-07-27",
    "severity": "sévère",
    "failure_mode": "Défaillance chaîne et boîtier de jonction",
    "cost_eur": 31553,
    "downtime_h": 52.2,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": 35,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#11",
    "date": "2025-09-05",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 39357,
    "downtime_h": 72.9,
    "weather_condition": "vent modéré",
    "days_since_previous_incident": 405,
    "days_since_previous_same_failure_mode": 645
   },
   {
    "ref": "#12",
    "date": "2025-11-30",
    "severity": "modérée",
    "failure_mode": "Baisse de rendement onduleur",
    "cost_eur": 6780,
    "downtime_h": 23.3,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": 86,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#13",
    "date": "2025-12-19",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 6057,
    "downtime_h": 17.3,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 19,
    "days_since_previous_same_failure_mode": 703
   }
  ]
 },
 "yearly_trend": {
  "by_year": [
   {
    "year": 2023,
    "n_incidents": 7,
    "n_severe": 3,
    "cost_eur": 139141,
    "downtime_h": 276.5,
    "cost_change_vs_previous_year_pct": null,
    "incident_count_change_vs_previous_year": null
   },
   {
    "year": 2024,
    "n_incidents": 3,
    "n_severe": 1,
    "cost_eur": 36833,
    "downtime_h": 66.2,
    "cost_change_vs_previous_year_pct": -73.5,
    "incident_count_change_vs_previous_year": -4
   },
   {
    "year": 2025,
    "n_incidents": 3,
    "n_severe": 1,
    "cost_eur": 52194,
    "downtime_h": 113.5,
    "cost_change_vs_previous_year_pct": 41.7,
    "incident_count_change_vs_previous_year": 0
   }
  ],
  "overall": {
   "first_year": 2023,
   "last_year": 2025,
   "cost_change_first_to_last_year_pct": -62.5,
   "label": "decreasing"
  }
 },
 "seasonality": [
  {
   "season": "winter",
   "n_incidents": 2,
   "n_severe": 0,
   "cost_eur": 9336,
   "downtime_h": 25.7,
   "sample": "indicative only (fewer than 3 incidents)"
  },
  {
   "season": "spring",
   "n_incidents": 3,
   "n_severe": 0,
   "cost_eur": 10229,
   "downtime_h": 32.0,
   "sample": "ok"
  },
  {
   "season": "summer",
   "n_incidents": 5,
   "n_severe": 3,
   "cost_eur": 116730,
   "downtime_h": 224.6,
   "sample": "ok"
  },
  {
   "season": "autumn",
   "n_incidents": 3,
   "n_severe": 2,
   "cost_eur": 91873,
   "downtime_h": 173.9,
   "sample": "ok"
  }
 ],
 "most_costly_incidents": {
  "incidents": [
   {
    "ref": "#7",
    "date": "2023-11-30",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "weather_condition": "temps calme",
    "cost_eur": 45736,
    "downtime_h": 77.7,
    "share_of_total_cost_pct": 20.0
   },
   {
    "ref": "#6",
    "date": "2023-08-21",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "weather_condition": "vent fort / tempête",
    "cost_eur": 44420,
    "downtime_h": 94.0,
    "share_of_total_cost_pct": 19.5
   },
   {
    "ref": "#11",
    "date": "2025-09-05",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "weather_condition": "vent modéré",
    "cost_eur": 39357,
    "downtime_h": 72.9,
    "share_of_total_cost_pct": 17.2
   }
  ],
  "top3_combined_cost_eur": 129512,
  "top3_combined_share_of_total_cost_pct": 56.8
 },
 "close_sequences_within_30_days": [
  {
   "incidents": [
    "#1",
    "#2"
   ],
   "from": "2023-03-03",
   "to": "2023-03-24",
   "span_days": 21,
   "n_severe": 0,
   "combined_cost_eur": 6117,
   "failure_modes": [
    "Dommages superficiels modules PV",
    "Incendie toiture et panneaux PV"
   ]
  },
  {
   "incidents": [
    "#5",
    "#6"
   ],
   "from": "2023-08-17",
   "to": "2023-08-21",
   "span_days": 4,
   "n_severe": 2,
   "combined_cost_eur": 78295,
   "failure_modes": [
    "Dommages superficiels modules PV"
   ]
  },
  {
   "incidents": [
    "#12",
    "#13"
   ],
   "from": "2025-11-30",
   "to": "2025-12-19",
   "span_days": 19,
   "n_severe": 0,
   "combined_cost_eur": 12837,
   "failure_modes": [
    "Baisse de rendement onduleur",
    "Dommages superficiels modules PV"
   ]
  }
 ],
 "facts": [
  "2023: 7 incident(s) (3 severe), 139 141 EUR.",
  "2024: 3 incident(s) (1 severe), 36 833 EUR (-73.5% vs previous year).",
  "2025: 3 incident(s) (1 severe), 52 194 EUR (+41.7% vs previous year).",
  "From 2023 to 2025 the cost changed by -62.5% (trend: decreasing).",
  "The most costly single incident is #7 (Dégradation et court-circuit câblage, sévère, 2023-11-30): 45 736 EUR, 20.0% of the cost of moderate and severe incidents.",
  "The most costly failure mode is Dommages superficiels modules PV: 91 303 EUR over 5 incident(s), 40.0% of the cost.",
  "The most costly incident and the most costly failure mode are different: do not attribute one to the other."
 ]
}
```
