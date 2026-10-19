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

You are writing the section "3. Cost timeline" of the incident report of equipment OUEST1-INV10 (site: Centrale PV Ouest-1).

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
   "#3",
   "#10",
   "#4"
  ],
  "points": [
   {
    "ref": "#1",
    "date": "2023-05-15",
    "severity": "modérée",
    "failure_mode": "Baisse de rendement onduleur",
    "cost_eur": 7670,
    "downtime_h": 24.0,
    "weather_condition": "conditions nominales",
    "days_since_previous_incident": null,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#2",
    "date": "2023-05-18",
    "severity": "modérée",
    "failure_mode": "Salissure et nettoyage modules PV",
    "cost_eur": 9476,
    "downtime_h": 24.2,
    "weather_condition": "vent modéré",
    "days_since_previous_incident": 3,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#3",
    "date": "2023-11-21",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "cost_eur": 49142,
    "downtime_h": 82.4,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 187,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#4",
    "date": "2023-12-22",
    "severity": "sévère",
    "failure_mode": "Baisse de rendement onduleur",
    "cost_eur": 24165,
    "downtime_h": 42.6,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 31,
    "days_since_previous_same_failure_mode": 221
   },
   {
    "ref": "#5",
    "date": "2024-02-26",
    "severity": "modérée",
    "failure_mode": "Dommages superficiels modules PV",
    "cost_eur": 2540,
    "downtime_h": 7.0,
    "weather_condition": "vent fort / tempête",
    "days_since_previous_incident": 66,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#6",
    "date": "2024-03-23",
    "severity": "modérée",
    "failure_mode": "Baisse de rendement onduleur",
    "cost_eur": 5780,
    "downtime_h": 14.7,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 26,
    "days_since_previous_same_failure_mode": 92
   },
   {
    "ref": "#7",
    "date": "2024-04-12",
    "severity": "modérée",
    "failure_mode": "Salissure et nettoyage modules PV",
    "cost_eur": 6643,
    "downtime_h": 20.6,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 20,
    "days_since_previous_same_failure_mode": 330
   },
   {
    "ref": "#8",
    "date": "2024-05-22",
    "severity": "sévère",
    "failure_mode": "Salissure et nettoyage modules PV",
    "cost_eur": 12817,
    "downtime_h": 21.5,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 40,
    "days_since_previous_same_failure_mode": 40
   },
   {
    "ref": "#9",
    "date": "2024-06-21",
    "severity": "sévère",
    "failure_mode": "Incendie bâtiment support PV",
    "cost_eur": 13226,
    "downtime_h": 22.5,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 30,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#10",
    "date": "2024-07-13",
    "severity": "sévère",
    "failure_mode": "Incendie bâtiment support PV",
    "cost_eur": 37904,
    "downtime_h": 65.5,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 22,
    "days_since_previous_same_failure_mode": 22
   },
   {
    "ref": "#11",
    "date": "2024-10-06",
    "severity": "sévère",
    "failure_mode": "Défaillance chaîne et boîtier de jonction",
    "cost_eur": 17578,
    "downtime_h": 28.9,
    "weather_condition": "vent modéré",
    "days_since_previous_incident": 85,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#12",
    "date": "2025-03-18",
    "severity": "modérée",
    "failure_mode": "Baisse de rendement onduleur",
    "cost_eur": 6954,
    "downtime_h": 18.9,
    "weather_condition": "ciel dégagé",
    "days_since_previous_incident": 163,
    "days_since_previous_same_failure_mode": 360
   },
   {
    "ref": "#13",
    "date": "2025-03-22",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 4506,
    "downtime_h": 13.7,
    "weather_condition": "temps calme",
    "days_since_previous_incident": 4,
    "days_since_previous_same_failure_mode": null
   },
   {
    "ref": "#14",
    "date": "2025-04-10",
    "severity": "modérée",
    "failure_mode": "Incendie toiture et panneaux PV",
    "cost_eur": 5254,
    "downtime_h": 17.9,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 19,
    "days_since_previous_same_failure_mode": 19
   },
   {
    "ref": "#15",
    "date": "2025-10-23",
    "severity": "modérée",
    "failure_mode": "Salissure et nettoyage modules PV",
    "cost_eur": 3108,
    "downtime_h": 9.6,
    "weather_condition": "pluie modérée",
    "days_since_previous_incident": 196,
    "days_since_previous_same_failure_mode": 519
   }
  ]
 },
 "yearly_trend": {
  "by_year": [
   {
    "year": 2023,
    "n_incidents": 4,
    "n_severe": 2,
    "cost_eur": 90452,
    "downtime_h": 173.2,
    "cost_change_vs_previous_year_pct": null,
    "incident_count_change_vs_previous_year": null
   },
   {
    "year": 2024,
    "n_incidents": 7,
    "n_severe": 4,
    "cost_eur": 96489,
    "downtime_h": 180.7,
    "cost_change_vs_previous_year_pct": 6.7,
    "incident_count_change_vs_previous_year": 3
   },
   {
    "year": 2025,
    "n_incidents": 4,
    "n_severe": 0,
    "cost_eur": 19821,
    "downtime_h": 60.1,
    "cost_change_vs_previous_year_pct": -79.5,
    "incident_count_change_vs_previous_year": -3
   }
  ],
  "overall": {
   "first_year": 2023,
   "last_year": 2025,
   "cost_change_first_to_last_year_pct": -78.1,
   "label": "decreasing"
  }
 },
 "seasonality": [
  {
   "season": "winter",
   "n_incidents": 2,
   "n_severe": 1,
   "cost_eur": 26704,
   "downtime_h": 49.6,
   "sample": "indicative only (fewer than 3 incidents)"
  },
  {
   "season": "spring",
   "n_incidents": 8,
   "n_severe": 1,
   "cost_eur": 59100,
   "downtime_h": 155.5,
   "sample": "ok"
  },
  {
   "season": "summer",
   "n_incidents": 2,
   "n_severe": 2,
   "cost_eur": 51131,
   "downtime_h": 88.0,
   "sample": "indicative only (fewer than 3 incidents)"
  },
  {
   "season": "autumn",
   "n_incidents": 3,
   "n_severe": 2,
   "cost_eur": 69828,
   "downtime_h": 120.9,
   "sample": "ok"
  }
 ],
 "most_costly_incidents": {
  "incidents": [
   {
    "ref": "#3",
    "date": "2023-11-21",
    "severity": "sévère",
    "failure_mode": "Dégradation et court-circuit câblage",
    "weather_condition": "temps calme",
    "cost_eur": 49142,
    "downtime_h": 82.4,
    "share_of_total_cost_pct": 23.8
   },
   {
    "ref": "#10",
    "date": "2024-07-13",
    "severity": "sévère",
    "failure_mode": "Incendie bâtiment support PV",
    "weather_condition": "pluie modérée",
    "cost_eur": 37904,
    "downtime_h": 65.5,
    "share_of_total_cost_pct": 18.3
   },
   {
    "ref": "#4",
    "date": "2023-12-22",
    "severity": "sévère",
    "failure_mode": "Baisse de rendement onduleur",
    "weather_condition": "temps calme",
    "cost_eur": 24165,
    "downtime_h": 42.6,
    "share_of_total_cost_pct": 11.7
   }
  ],
  "top3_combined_cost_eur": 111211,
  "top3_combined_share_of_total_cost_pct": 53.8
 },
 "close_sequences_within_30_days": [
  {
   "incidents": [
    "#1",
    "#2"
   ],
   "from": "2023-05-15",
   "to": "2023-05-18",
   "span_days": 3,
   "n_severe": 0,
   "combined_cost_eur": 17146,
   "failure_modes": [
    "Baisse de rendement onduleur",
    "Salissure et nettoyage modules PV"
   ]
  },
  {
   "incidents": [
    "#5",
    "#6",
    "#7"
   ],
   "from": "2024-02-26",
   "to": "2024-04-12",
   "span_days": 46,
   "n_severe": 0,
   "combined_cost_eur": 14963,
   "failure_modes": [
    "Baisse de rendement onduleur",
    "Dommages superficiels modules PV",
    "Salissure et nettoyage modules PV"
   ]
  },
  {
   "incidents": [
    "#8",
    "#9",
    "#10"
   ],
   "from": "2024-05-22",
   "to": "2024-07-13",
   "span_days": 52,
   "n_severe": 3,
   "combined_cost_eur": 63948,
   "failure_modes": [
    "Incendie bâtiment support PV",
    "Salissure et nettoyage modules PV"
   ]
  },
  {
   "incidents": [
    "#12",
    "#13",
    "#14"
   ],
   "from": "2025-03-18",
   "to": "2025-04-10",
   "span_days": 23,
   "n_severe": 0,
   "combined_cost_eur": 16714,
   "failure_modes": [
    "Baisse de rendement onduleur",
    "Incendie toiture et panneaux PV"
   ]
  }
 ],
 "facts": [
  "2023: 4 incident(s) (2 severe), 90 452 EUR.",
  "2024: 7 incident(s) (4 severe), 96 489 EUR (+6.7% vs previous year).",
  "2025: 4 incident(s) (0 severe), 19 821 EUR (-79.5% vs previous year).",
  "From 2023 to 2025 the cost changed by -78.1% (trend: decreasing).",
  "The most costly single incident is #3 (Dégradation et court-circuit câblage, sévère, 2023-11-21): 49 142 EUR, 23.8% of the cost of moderate and severe incidents.",
  "The most costly failure mode is Incendie bâtiment support PV: 51 131 EUR over 2 incident(s), 24.7% of the cost.",
  "The most costly incident and the most costly failure mode are different: do not attribute one to the other."
 ]
}
```
