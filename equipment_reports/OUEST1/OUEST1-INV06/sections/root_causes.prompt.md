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

You are writing the section "6. Root-cause hypotheses" of the incident report of equipment OUEST1-INV06 (site: Centrale PV Ouest-1).

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
   "n_incidents": 8,
   "n_severe": 6,
   "sample": "ok",
   "weather_counts": {
    "vent fort / tempête": 4,
    "orage avec grêle": 4
   },
   "dominant_weather": [
    "vent fort / tempête",
    "orage avec grêle"
   ],
   "median_days_between_recurrences": 83,
   "recurrences_within_90_days": 4,
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
   "n_incidents": 2,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "pluie modérée": 2
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "median_days_between_recurrences": 312,
   "recurrences_within_90_days": 0,
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
   "n_incidents": 5,
   "n_severe": 1,
   "sample": "ok",
   "weather_counts": {
    "conditions nominales": 1,
    "temps calme": 1,
    "pluie modérée": 3
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "median_days_between_recurrences": 148,
   "recurrences_within_90_days": 1,
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
   "n_incidents": 4,
   "n_severe": 0,
   "sample": "ok",
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
   "median_days_between_recurrences": 131,
   "recurrences_within_90_days": 0,
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
   "n_incidents": 1,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "ciel dégagé": 1
   },
   "dominant_weather": [
    "ciel dégagé"
   ],
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
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
 "facts": [
  "Most downtime occurs under 'vent fort / tempête': 315.5 h over 4 incident(s), 41.4% of the downtime (in line with site).",
  "'pluie modérée' is over-represented vs site: 25.0% of the incidents of this equipment vs 18.9% on the site.",
  "'orage avec grêle' is over-represented vs site: 20.0% of the incidents of this equipment vs 12.1% on the site.",
  "'temps calme' is under-represented vs site: 10.0% of the incidents of this equipment vs 17.4% on the site (indicative only).",
  "'vent modéré' is under-represented vs site: 5.0% of the incidents of this equipment vs 9.8% on the site (indicative only)."
 ]
}
```
