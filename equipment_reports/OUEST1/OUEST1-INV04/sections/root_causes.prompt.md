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

You are writing the section "6. Root-cause hypotheses" of the incident report of equipment OUEST1-INV04 (site: Centrale PV Ouest-1).

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
   "n_incidents": 3,
   "n_severe": 2,
   "sample": "ok",
   "weather_counts": {
    "pluie modérée": 3
   },
   "dominant_weather": [
    "pluie modérée"
   ],
   "median_days_between_recurrences": 132,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#1",
     "date": "2023-05-30",
     "severity": "sévère",
     "cost_eur": 40158,
     "downtime_h": 68.0,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#2",
     "date": "2023-06-22",
     "severity": "sévère",
     "cost_eur": 40740,
     "downtime_h": 71.6,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#6",
     "date": "2024-02-18",
     "severity": "modérée",
     "cost_eur": 7477,
     "downtime_h": 23.7,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Salissure et nettoyage modules PV",
   "n_incidents": 2,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "conditions nominales": 1,
    "pluie modérée": 1
   },
   "dominant_weather": [
    "conditions nominales",
    "pluie modérée"
   ],
   "median_days_between_recurrences": 0,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#12",
     "date": "2025-07-23",
     "severity": "modérée",
     "cost_eur": 4179,
     "downtime_h": 13.5,
     "weather_condition": "pluie modérée"
    },
    {
     "ref": "#13",
     "date": "2025-07-23",
     "severity": "sévère",
     "cost_eur": 55925,
     "downtime_h": 88.8,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Défaillance chaîne et boîtier de jonction",
   "n_incidents": 1,
   "n_severe": 1,
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
     "ref": "#9",
     "date": "2024-07-24",
     "severity": "sévère",
     "cost_eur": 31133,
     "downtime_h": 68.0,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Incendie toiture et panneaux PV",
   "n_incidents": 4,
   "n_severe": 0,
   "sample": "ok",
   "weather_counts": {
    "ciel dégagé": 1,
    "temps calme": 3
   },
   "dominant_weather": [
    "temps calme"
   ],
   "median_days_between_recurrences": 288,
   "recurrences_within_90_days": 0,
   "incidents": [
    {
     "ref": "#3",
     "date": "2023-07-17",
     "severity": "modérée",
     "cost_eur": 3207,
     "downtime_h": 10.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#7",
     "date": "2024-05-31",
     "severity": "modérée",
     "cost_eur": 6401,
     "downtime_h": 22.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#10",
     "date": "2025-03-15",
     "severity": "modérée",
     "cost_eur": 3009,
     "downtime_h": 9.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#14",
     "date": "2025-07-26",
     "severity": "modérée",
     "cost_eur": 7805,
     "downtime_h": 22.3,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Dommages superficiels modules PV",
   "n_incidents": 3,
   "n_severe": 0,
   "sample": "ok",
   "weather_counts": {
    "vent fort / tempête": 1,
    "orage avec grêle": 2
   },
   "dominant_weather": [
    "orage avec grêle"
   ],
   "median_days_between_recurrences": 90,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#11",
     "date": "2025-06-11",
     "severity": "modérée",
     "cost_eur": 6986,
     "downtime_h": 21.1,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#15",
     "date": "2025-08-03",
     "severity": "modérée",
     "cost_eur": 4023,
     "downtime_h": 10.8,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#16",
     "date": "2025-12-08",
     "severity": "modérée",
     "cost_eur": 6137,
     "downtime_h": 19.6,
     "weather_condition": "orage avec grêle"
    }
   ]
  },
  {
   "failure_mode": "Remplacement préventif connecteurs",
   "n_incidents": 3,
   "n_severe": 0,
   "sample": "ok",
   "weather_counts": {
    "ciel dégagé": 1,
    "temps calme": 2
   },
   "dominant_weather": [
    "temps calme"
   ],
   "median_days_between_recurrences": 134,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#4",
     "date": "2023-10-25",
     "severity": "modérée",
     "cost_eur": 3778,
     "downtime_h": 13.4,
     "weather_condition": "ciel dégagé"
    },
    {
     "ref": "#5",
     "date": "2024-01-03",
     "severity": "modérée",
     "cost_eur": 7390,
     "downtime_h": 19.6,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#8",
     "date": "2024-07-20",
     "severity": "modérée",
     "cost_eur": 3785,
     "downtime_h": 11.4,
     "weather_condition": "temps calme"
    }
   ]
  }
 ],
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
 "facts": [
  "Most downtime occurs under 'pluie modérée': 244.8 h over 5 incident(s), 49.5% of the downtime (over-represented vs site).",
  "'pluie modérée' is over-represented vs site: 31.2% of the incidents of this equipment vs 18.9% on the site.",
  "'conditions nominales' is under-represented vs site: 6.2% of the incidents of this equipment vs 12.1% on the site (indicative only).",
  "'temps calme' is over-represented vs site: 31.2% of the incidents of this equipment vs 17.4% on the site.",
  "'vent fort / tempête' is under-represented vs site: 6.2% of the incidents of this equipment vs 15.9% on the site (indicative only)."
 ]
}
```
