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

You are writing the section "6. Root-cause hypotheses" of the incident report of equipment OUEST1-INV08 (site: Centrale PV Ouest-1).

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
   "failure_mode": "Incendie toiture et panneaux PV",
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
     "ref": "#7",
     "date": "2024-07-05",
     "severity": "sévère",
     "cost_eur": 48714,
     "downtime_h": 99.2,
     "weather_condition": "conditions nominales"
    }
   ]
  },
  {
   "failure_mode": "Dégradation et court-circuit câblage",
   "n_incidents": 2,
   "n_severe": 1,
   "sample": "indicative only (fewer than 3 incidents)",
   "weather_counts": {
    "vent modéré": 1,
    "pluie modérée": 1
   },
   "dominant_weather": [
    "vent modéré",
    "pluie modérée"
   ],
   "median_days_between_recurrences": 24,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#12",
     "date": "2025-06-20",
     "severity": "sévère",
     "cost_eur": 26429,
     "downtime_h": 55.8,
     "weather_condition": "vent modéré"
    },
    {
     "ref": "#15",
     "date": "2025-07-14",
     "severity": "modérée",
     "cost_eur": 9721,
     "downtime_h": 24.6,
     "weather_condition": "pluie modérée"
    }
   ]
  },
  {
   "failure_mode": "Incendie bâtiment support PV",
   "n_incidents": 1,
   "n_severe": 1,
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
     "ref": "#5",
     "date": "2023-08-06",
     "severity": "sévère",
     "cost_eur": 34465,
     "downtime_h": 60.7,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Dommages superficiels modules PV",
   "n_incidents": 5,
   "n_severe": 0,
   "sample": "ok",
   "weather_counts": {
    "vent fort / tempête": 2,
    "orage avec grêle": 3
   },
   "dominant_weather": [
    "orage avec grêle"
   ],
   "median_days_between_recurrences": 142,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#2",
     "date": "2023-04-15",
     "severity": "modérée",
     "cost_eur": 3355,
     "downtime_h": 10.5,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#8",
     "date": "2024-09-26",
     "severity": "modérée",
     "cost_eur": 8671,
     "downtime_h": 22.7,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#9",
     "date": "2025-02-11",
     "severity": "modérée",
     "cost_eur": 4961,
     "downtime_h": 12.9,
     "weather_condition": "orage avec grêle"
    },
    {
     "ref": "#13",
     "date": "2025-07-08",
     "severity": "modérée",
     "cost_eur": 6266,
     "downtime_h": 17.4,
     "weather_condition": "vent fort / tempête"
    },
    {
     "ref": "#14",
     "date": "2025-07-09",
     "severity": "modérée",
     "cost_eur": 3110,
     "downtime_h": 10.1,
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
    "ciel dégagé": 1,
    "conditions nominales": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "conditions nominales"
   ],
   "median_days_between_recurrences": 229,
   "recurrences_within_90_days": 0,
   "incidents": [
    {
     "ref": "#1",
     "date": "2023-02-28",
     "severity": "sévère",
     "cost_eur": 14647,
     "downtime_h": 25.1,
     "weather_condition": "conditions nominales"
    },
    {
     "ref": "#6",
     "date": "2023-10-15",
     "severity": "sévère",
     "cost_eur": 10363,
     "downtime_h": 21.8,
     "weather_condition": "ciel dégagé"
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
    "temps calme": 1,
    "vent modéré": 1
   },
   "dominant_weather": [
    "ciel dégagé",
    "temps calme",
    "vent modéré"
   ],
   "median_days_between_recurrences": 312,
   "recurrences_within_90_days": 1,
   "incidents": [
    {
     "ref": "#3",
     "date": "2023-06-05",
     "severity": "modérée",
     "cost_eur": 4703,
     "downtime_h": 15.5,
     "weather_condition": "temps calme"
    },
    {
     "ref": "#4",
     "date": "2023-06-19",
     "severity": "modérée",
     "cost_eur": 4156,
     "downtime_h": 10.6,
     "weather_condition": "vent modéré"
    },
    {
     "ref": "#10",
     "date": "2025-02-19",
     "severity": "modérée",
     "cost_eur": 6713,
     "downtime_h": 18.6,
     "weather_condition": "ciel dégagé"
    }
   ]
  },
  {
   "failure_mode": "Salissure et nettoyage modules PV",
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
     "ref": "#11",
     "date": "2025-02-28",
     "severity": "modérée",
     "cost_eur": 6080,
     "downtime_h": 18.5,
     "weather_condition": "conditions nominales"
    }
   ]
  }
 ],
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
 "facts": [
  "Most downtime occurs under 'conditions nominales': 142.8 h over 3 incident(s), 33.7% of the downtime (over-represented vs site).",
  "'conditions nominales' is over-represented vs site: 20.0% of the incidents of this equipment vs 12.1% on the site.",
  "'ciel dégagé' is over-represented vs site: 20.0% of the incidents of this equipment vs 13.6% on the site.",
  "'vent modéré' is over-represented vs site: 13.3% of the incidents of this equipment vs 9.8% on the site (indicative only).",
  "'orage avec grêle' is over-represented vs site: 20.0% of the incidents of this equipment vs 12.1% on the site.",
  "'pluie modérée' is under-represented vs site: 6.7% of the incidents of this equipment vs 18.9% on the site (indicative only).",
  "'temps calme' is under-represented vs site: 6.7% of the incidents of this equipment vs 17.4% on the site (indicative only)."
 ]
}
```
