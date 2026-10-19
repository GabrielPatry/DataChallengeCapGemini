# System

You are a root-cause analysis (RCA) engineer for PV plants.

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

You are writing the section "6. Root-cause hypotheses" of the incident report of equipment OUEST1-INV02 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. Propose 3 to 5 root-cause hypotheses explaining the incidents of this equipment. A hypothesis may cover one failure mode or a common cause behind several (e.g. heat stress, poor connections, lightning exposure).
2. For each hypothesis, list the failure modes it explains and the incidents supporting it — only incidents belonging to those failure modes.
3. Explain the reasoning in 1-3 sentences (mechanism, weather or timing patterns).

Statistics and figure data for this section (every value is already computed):
```json
{
 "failure_modes": [
  {
   "failure_mode": "Dommages superficiels modules PV",
   "n_incidents": 5,
   "n_severe": 2,
   "sample": "ok",
   "weather_counts": {
    "vent fort / tempête": 4,
    "orage avec grêle": 1
   },
   "dominant_weather": [
    "vent fort / tempête"
   ],
   "median_days_between_recurrences": 147,
   "recurrences_within_90_days": 1,
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
   "n_incidents": 2,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "temps calme": 1,
    "vent modéré": 1
   },
   "dominant_weather": [
    "temps calme",
    "vent modéré"
   ],
   "median_days_between_recurrences": 645,
   "recurrences_within_90_days": 0,
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
   "n_incidents": 1,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "conditions nominales": 1
   },
   "dominant_weather": [
    "conditions nominales"
   ],
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
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
   "n_incidents": 2,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "ciel dégagé": 1,
    "vent modéré": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "vent modéré"
   ],
   "median_days_between_recurrences": 49,
   "recurrences_within_90_days": 1,
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
   "n_incidents": 1,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "conditions nominales": 1
   },
   "dominant_weather": [
    "conditions nominales"
   ],
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
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
   "n_incidents": 2,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "pluie modérée": 2
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "median_days_between_recurrences": 477,
   "recurrences_within_90_days": 0,
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
 "facts": [
  "Most downtime occurs under 'vent fort / tempête': 171.5 h over 4 incident(s), 37.6% of the downtime (over-represented vs site).",
  "'vent fort / tempête' is over-represented vs site: 30.8% of the incidents of this equipment vs 15.9% on the site.",
  "'vent modéré' is over-represented vs site: 15.4% of the incidents of this equipment vs 9.8% on the site (indicative only).",
  "'temps calme' is under-represented vs site: 7.7% of the incidents of this equipment vs 17.4% on the site (indicative only).",
  "'orage avec grêle' is under-represented vs site: 7.7% of the incidents of this equipment vs 12.1% on the site (indicative only).",
  "'ciel dégagé' is under-represented vs site: 7.7% of the incidents of this equipment vs 13.6% on the site (indicative only)."
 ]
}
```
