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

You are writing the section "3. Cost timeline" of the incident report of equipment OUEST1-INV08 (site: Centrale PV Ouest-1).

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
   "#5",
   "#12"
  ],
  "points": [
   {
    "ref": "#1",
    "date": "2023-02-28",
    "severity": "sévère",
    "failure_mode": "Défaillance chaîne et boîtier de jonction",
    "cost_eur": 14647,
    "downtime_h": 25.1,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": null,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#2",
    "date": "2023-04-15",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 3355,
    "downtime_h": 10.5,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 46,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#3",
    "date": "2023-06-05",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 4703,
    "downtime_h": 15.5,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 51,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#4",
    "date": "2023-06-19",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 4156,
    "downtime_h": 10.6,
    "weather_condition": "vent modéré",
    "days_since_previous_incident": 14,
    "days_since_previous_same_failure_mode": 14
   },
   {
    "ref": "#5",
    "date": "2023-08-06",
    "severity": "sévère",
    "failure_mode": "Incendie bâtiment support PV",
    "cost_eur": 34465,
    "downtime_h": 60.7,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 48,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#6",
    "date": "2023-10-15",
    "severity": "sévère",
    "failure_mode": "Défaillance chaîne et boîtier de jonction",
    "cost_eur": 10363,
    "downtime_h": 21.8,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 70,
    "days_since_previous_same_failure_mode": 229
   },
   {
    "ref": "#7",
    "date": "2024-07-05",
    "severity": "sévère",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 48714,
    "downtime_h": 99.2,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": 264,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#8",
    "date": "2024-09-26",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 8671,
    "downtime_h": 22.7,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 83,
    "days_since_previous_same_failure_mode": 530
   },
   {
    "ref": "#9",
    "date": "2025-02-11",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 4961,
    "downtime_h": 12.9,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 138,
    "days_since_previous_same_failure_mode": 138
   },
   {
    "ref": "#10",
    "date": "2025-02-19",
    "severity": "modérée",
    "failure_mode": "Remplacement préventif connecteurs",
    "cost_eur": 6713,
    "downtime_h": 18.6,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 8,
    "days_since_previous_same_failure_mode": 611
   },
   {
    "ref": "#11",
    "date": "2025-02-28",
    "severity": "modérée",
    "failure_mode": "Salissure et nettoyage modules PV",
    "cost_eur": 6080,
    "downtime_h": 18.5,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": 9,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#12",
    "date": "2025-06-20",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 26429,
    "downtime_h": 55.8,
    "weather_condition": "vent modéré",
    "days_since_previous_incident": 112,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#13",
    "date": "2025-07-08",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 6266,
    "downtime_h": 17.4,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 18,
    "days_since_previous_same_failure_mode": 147
   },
   {
    "ref": "#14",
    "date": "2025-07-09",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 3110,
    "downtime_h": 10.1,
    "weather_condition": "orage avec grêle",
    "days_since_previous_incident": 1,
    "days_since_previous_same_failure_mode": 1
   },
   {
    "ref": "#15",
    "date": "2025-07-14",
    "severity": "modérée",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 9721,
    "downtime_h": 24.6,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 5,
    "days_since_previous_same_failure_mode": 24
   }
  ]
 },
 "yearly_trend": {
  "by_year": [
   {
    "year": 2023,
    "n_incidents": 6,
    "n_severe": 3,
    "cost_eur": 71689,
    "downtime_h": 144.2,
    "cost_change_vs_previous_year_pct": null,
    "incident_count_change_vs_previous_year": null
   },
   {
    "year": 2024,
    "n_incidents": 2,
    "n_severe": 1,
    "cost_eur": 57385,
    "downtime_h": 121.9,
    "cost_change_vs_previous_year_pct": -20.0,
    "incident_count_change_vs_previous_year": -4
   },
   {
    "year": 2025,
    "n_incidents": 7,
    "n_severe": 1,
    "cost_eur": 63281,
    "downtime_h": 157.9,
    "cost_change_vs_previous_year_pct": 10.3,
    "incident_count_change_vs_previous_year": 5
   }
  ],
  "overall": {
   "first_year": 2023,
   "last_year": 2025,
   "cost_change_first_to_last_year_pct": -11.7,
   "label": "stable"
  }
 },
 "seasonality": [
  {
   "season": "winter",
   "n_incidents": 4,
   "n_severe": 1,
   "cost_eur": 32401,
   "downtime_h": 75.1,
   "sample": "ok"
  },
  {
   "season": "spring",
   "n_incidents": 1,
   "n_severe": 0,
   "cost_eur": 3355,
   "downtime_h": 10.5,
   "sample": "indicative only (fewer than 3 incidents)"
  },
  {
   "season": "summer",
   "n_incidents": 8,
   "n_severe": 3,
   "cost_eur": 137565,
   "downtime_h": 293.9,
   "sample": "ok"
  },
  {
   "season": "autumn",
   "n_incidents": 2,
   "n_severe": 1,
   "cost_eur": 19034,
   "downtime_h": 44.5,
   "sample": "indicative only (fewer than 3 incidents)"
  }
 ],
 "most_costly_incidents": {
  "incidents": [
   {
    "ref": "#7",
    "date": "2024-07-05",
    "severity": "sévère",
    "failure_mode": "Incendie toiture et panneaux PV",
    "weather_condition": "conditions nominales",
    "cost_eur": 48714,
    "downtime_h": 99.2,
    "share_of_total_cost_pct": 25.3
   },
   {
    "ref": "#5",
    "date": "2023-08-06",
    "severity": "sévère",
    "failure_mode": "Incendie bâtiment support PV",
    "weather_condition": "ciel dégagé",
    "cost_eur": 34465,
    "downtime_h": 60.7,
    "share_of_total_cost_pct": 17.9
   },
   {
    "ref": "#12",
    "date": "2025-06-20",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "weather_condition": "vent modéré",
    "cost_eur": 26429,
    "downtime_h": 55.8,
    "share_of_total_cost_pct": 13.7
   }
  ],
  "top3_combined_cost_eur": 109608,
  "top3_combined_share_of_total_cost_pct": 57.0
 },
 "close_sequences_within_30_days": [
  {
   "incidents": [
    "#3",
    "#4"
   ],
   "from": "2023-06-05",
   "to": "2023-06-19",
   "span_days": 14,
   "n_severe": 0,
   "combined_cost_eur": 8860,
   "failure_modes": [
    "Remplacement préventif connecteurs"
   ]
  },
  {
   "incidents": [
    "#9",
    "#10",
    "#11"
   ],
   "from": "2025-02-11",
   "to": "2025-02-28",
   "span_days": 17,
   "n_severe": 0,
   "combined_cost_eur": 17755,
   "failure_modes": [
    "Dommages superficiels modules PV",
    "Remplacement préventif connecteurs",
    "Salissure et nettoyage modules PV"
   ]
  },
  {
   "incidents": [
    "#12",
    "#13",
    "#14",
    "#15"
   ],
   "from": "2025-06-20",
   "to": "2025-07-14",
   "span_days": 24,
   "n_severe": 1,
   "combined_cost_eur": 45527,
   "failure_modes": [
    "Dommages superficiels modules PV",
    "Dégradation et court-circuit câblage"
   ]
  }
 ],
 "facts": [
  "2023: 6 incident(s) (3 severe), 71 689 EUR.",
  "2024: 2 incident(s) (1 severe), 57 385 EUR (-20.0% vs previous year).",
  "2025: 7 incident(s) (1 severe), 63 281 EUR (+10.3% vs previous year).",
  "From 2023 to 2025 the cost changed by -11.7% (trend: stable).",
  "The most costly single incident is #7 (Incendie toiture et panneaux PV, sévère, 2024-07-05): 48 714 EUR, 25.3% of the cost of moderate and severe incidents.",
  "The most costly failure mode is Incendie toiture et panneaux PV: 48 714 EUR over 1 incident(s), 25.3% of the cost."
 ]
}
```
