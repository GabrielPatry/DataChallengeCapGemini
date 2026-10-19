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

You are writing the section "6. Root-cause hypotheses" of the incident report of equipment OUEST1-INV03 (site: Centrale PV Ouest-1).

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
   "failure_mode": "Dégradation et court-circuit câblage",
   "n_incidents": 2,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "ciel dégagé": 1,
    "vent modéré": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "vent modéré"
   ],
   "median_days_between_recurrences": 78,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#3",
     "date": "2023-11-05",
     "severity": "sévère",
     "cost_eur": 43675,
     "downtime_h": 78.3,
     "weather_condition": "vent modéré"
    },
    {
     "ref": "#4",
     "date": "2024-01-22",
     "severity": "sévère",
     "cost_eur": 54313,
     "downtime_h": 91.8,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Dommages superficiels modules PV",
   "n_incidents": 4,
   "n_severe": 2,
   "sample": "ok",
   "weather_counts": {
    "vent fort / tempête": 3,
    "orage avec grêle": 1
   },
   "dominant_weather": [
    "vent fort / tempête"
   ],
   "median_days_between_recurrences": 142,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#2",
     "date": "2023-09-21",
     "severity": "modérée",
     "cost_eur": 3870,
     "downtime_h": 13.7,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#5",
     "date": "2024-02-10",
     "severity": "sévère",
     "cost_eur": 37539,
     "downtime_h": 74.0,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#8",
     "date": "2025-01-17",
     "severity": "sévère",
     "cost_eur": 25134,
     "downtime_h": 51.9,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#9",
     "date": "2025-02-28",
     "severity": "modérée",
     "cost_eur": 3967,
     "downtime_h": 14.0,
     "weather_condition": "vent fort / tempête"
    }
   ]
  },
  {
   "failure_mode": "Baisse de rendement onduleur",
   "n_incidents": 2,
   "n_severe": 2,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "ciel dégagé": 1,
    "temps calme": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "temps calme"
   ],
   "median_days_between_recurrences": 159,
   "recurrences_within_90_days": 0,
   "incidents": [
    {
     "ref": "#10",
     "date": "2025-06-21",
     "severity": "sévère",
     "cost_eur": 38931,
     "downtime_h": 67.2,
     "weather_condition": "ciel dégagé"
    },
    {
     "ref": "#13",
     "date": "2025-11-27",
     "severity": "sévère",
     "cost_eur": 12425,
     "downtime_h": 25.9,
     "weather_condition": "temps calme"
    }
   ]
  },
  {
   "failure_mode": "Incendie toiture et panneaux PV",
   "n_incidents": 2,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "conditions nominales": 1,
    "temps calme": 1
   },
   "dominant_weather": [
    "conditions nominales",
    "temps calme"
   ],
   "median_days_between_recurrences": 26,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#11",
     "date": "2025-07-24",
     "severity": "sévère",
     "cost_eur": 27461,
     "downtime_h": 46.5,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#12",
     "date": "2025-08-19",
     "severity": "modérée",
     "cost_eur": 6667,
     "downtime_h": 18.5,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Incendie bâtiment support PV",
   "n_incidents": 1,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "temps calme": 1
   },
   "dominant_weather": [
    "temps calme"
   ],
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "incidents": [
    {
     "ref": "#1",
     "date": "2023-03-23",
     "severity": "sévère",
     "cost_eur": 21116,
     "downtime_h": 41.4,
     "weather_condition": "temps calme"
    }
   ]
  },
  {
   "failure_mode": "Remplacement préventif connecteurs",
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
     "ref": "#6",
     "date": "2024-02-26",
     "severity": "modérée",
     "cost_eur": 7961,
     "downtime_h": 24.0,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Salissure et nettoyage modules PV",
   "n_incidents": 1,
   "n_severe": 0,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "pluie modérée": 1
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "median_days_between_recurrences": null,
   "recurrences_within_90_days": 0,
   "incidents": [
    {
     "ref": "#7",
     "date": "2024-11-26",
     "severity": "modérée",
     "cost_eur": 2006,
     "downtime_h": 6.5,
     "weather_condition": "pluie modérée"
    }
   ]
  }
 ],
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
 "facts": [
  "Most downtime occurs under 'ciel dégagé': 159.0 h over 2 incident(s), 28.7% of the downtime (in line with site).",
  "'temps calme' is over-represented vs site: 23.1% of the incidents of this equipment vs 17.4% on the site.",
  "'vent fort / tempête' is over-represented vs site: 23.1% of the incidents of this equipment vs 15.9% on the site.",
  "'orage avec grêle' is under-represented vs site: 7.7% of the incidents of this equipment vs 12.1% on the site (indicative only).",
  "'pluie modérée' is under-represented vs site: 7.7% of the incidents of this equipment vs 18.9% on the site (indicative only)."
 ]
}
```
