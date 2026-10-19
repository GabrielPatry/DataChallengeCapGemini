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

You are writing the section "3. Cost timeline" of the incident report of equipment OUEST1-INV03 (site: Centrale PV Ouest-1).

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
   "#4",
   "#3",
   "#10"
  ],
  "points": [
   {
    "ref": "#1",
    "date": "2023-03-23",
    "severity": "sévère",
    "failure_mode": "Incendie bâtiment support PV",
    "cost_eur": 21116,
    "downtime_h": 41.4,
    "weather_condition": "temps calme",
    "days_since_previous_incident": null,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#2",
    "date": "2023-09-21",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 3870,
    "downtime_h": 13.7,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 182,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#3",
    "date": "2023-11-05",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 43675,
    "downtime_h": 78.3,
    "weather_condition": "vent modéré",
    "days_since_previous_incident": 45,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#4",
    "date": "2024-01-22",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 54313,
    "downtime_h": 91.8,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 78,
    "days_since_previous_same_failure_mode": 78
   },
   {
    "ref": "#5",
    "date": "2024-02-10",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 37539,
    "downtime_h": 74.0,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 19,
    "days_since_previous_same_failure_mode": 142
   },
   {
    "ref": "#6",
    "date": "2024-02-26",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 7961,
    "downtime_h": 24.0,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": 16,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#7",
    "date": "2024-11-26",
    "severity": "modérée",
    "failure_mode": "Salissure et nettoyage modules PV",
    "cost_eur": 2006,
    "downtime_h": 6.5,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 274,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#8",
    "date": "2025-01-17",
    "severity": "sévère",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 25134,
    "downtime_h": 51.9,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 52,
    "days_since_previous_same_failure_mode": 342
   },
   {
    "ref": "#9",
    "date": "2025-02-28",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 3967,
    "downtime_h": 14.0,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 42,
    "days_since_previous_same_failure_mode": 42
   },
   {
    "ref": "#10",
    "date": "2025-06-21",
    "severity": "sévère",
    "failure_mode": "Baisse de rendement onduleur",
    "cost_eur": 38931,
    "downtime_h": 67.2,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 113,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#11",
    "date": "2025-07-24",
    "severity": "sévère",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 27461,
    "downtime_h": 46.5,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 33,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#12",
    "date": "2025-08-19",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 6667,
    "downtime_h": 18.5,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": 26,
    "days_since_previous_same_failure_mode": 26
   },
   {
    "ref": "#13",
    "date": "2025-11-27",
    "severity": "sévère",
    "failure_mode": "Baisse de rendement onduleur",
    "cost_eur": 12425,
    "downtime_h": 25.9,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 100,
    "days_since_previous_same_failure_mode": 159
   }
  ]
 },
 "yearly_trend": {
  "by_year": [
   {
    "year": 2023,
    "n_incidents": 3,
    "n_severe": 2,
    "cost_eur": 68661,
    "downtime_h": 133.4,
    "cost_change_vs_previous_year_pct": null,
    "incident_count_change_vs_previous_year": null
   },
   {
    "year": 2024,
    "n_incidents": 4,
    "n_severe": 2,
    "cost_eur": 101819,
    "downtime_h": 196.3,
    "cost_change_vs_previous_year_pct": 48.3,
    "incident_count_change_vs_previous_year": 1
   },
   {
    "year": 2025,
    "n_incidents": 6,
    "n_severe": 4,
    "cost_eur": 114585,
    "downtime_h": 224.0,
    "cost_change_vs_previous_year_pct": 12.5,
    "incident_count_change_vs_previous_year": 2
   }
  ],
  "overall": {
   "first_year": 2023,
   "last_year": 2025,
   "cost_change_first_to_last_year_pct": 66.9,
   "label": "increasing"
  }
 },
 "seasonality": [
  {
   "season": "winter",
   "n_incidents": 5,
   "n_severe": 3,
   "cost_eur": 128915,
   "downtime_h": 255.7,
   "sample": "ok"
  },
  {
   "season": "spring",
   "n_incidents": 1,
   "n_severe": 1,
   "cost_eur": 21116,
   "downtime_h": 41.4,
   "sample": "indicative only (fewer than 3 incidents)"
  },
  {
   "season": "summer",
   "n_incidents": 3,
   "n_severe": 2,
   "cost_eur": 73059,
   "downtime_h": 132.2,
   "sample": "ok"
  },
  {
   "season": "autumn",
   "n_incidents": 4,
   "n_severe": 2,
   "cost_eur": 61976,
   "downtime_h": 124.4,
   "sample": "ok"
  }
 ],
 "most_costly_incidents": {
  "incidents": [
   {
    "ref": "#4",
    "date": "2024-01-22",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "weather_condition": "ciel dégagé",
    "cost_eur": 54313,
    "downtime_h": 91.8,
    "share_of_total_cost_pct": 19.1
   },
   {
    "ref": "#3",
    "date": "2023-11-05",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "weather_condition": "vent modéré",
    "cost_eur": 43675,
    "downtime_h": 78.3,
    "share_of_total_cost_pct": 15.3
   },
   {
    "ref": "#10",
    "date": "2025-06-21",
    "severity": "sévère",
    "failure_mode": "Baisse de rendement onduleur",
    "weather_condition": "ciel dégagé",
    "cost_eur": 38931,
    "downtime_h": 67.2,
    "share_of_total_cost_pct": 13.7
   }
  ],
  "top3_combined_cost_eur": 136920,
  "top3_combined_share_of_total_cost_pct": 48.0
 },
 "close_sequences_within_30_days": [
  {
   "incidents": [
    "#4",
    "#5",
    "#6"
   ],
   "from": "2024-01-22",
   "to": "2024-02-26",
   "span_days": 35,
   "n_severe": 2,
   "combined_cost_eur": 99814,
   "failure_modes": [
    "Dommages superficiels modules PV",
    "Dégradation et court-circuit câblage",
    "Remplacement préventif connecteurs"
   ]
  },
  {
   "incidents": [
    "#11",
    "#12"
   ],
   "from": "2025-07-24",
   "to": "2025-08-19",
   "span_days": 26,
   "n_severe": 1,
   "combined_cost_eur": 34127,
   "failure_modes": [
    "Incendie toiture et panneaux PV"
   ]
  }
 ],
 "facts": [
  "2023: 3 incident(s) (2 severe), 68 661 EUR.",
  "2024: 4 incident(s) (2 severe), 101 819 EUR (+48.3% vs previous year).",
  "2025: 6 incident(s) (4 severe), 114 585 EUR (+12.5% vs previous year).",
  "From 2023 to 2025 the cost changed by +66.9% (trend: increasing).",
  "The most costly single incident is #4 (Dégradation et court-circuit câblage, sévère, 2024-01-22): 54 313 EUR, 19.1% of the cost of moderate and severe incidents.",
  "The most costly failure mode is Dégradation et court-circuit câblage: 97 989 EUR over 2 incident(s), 34.4% of the cost."
 ]
}
```
