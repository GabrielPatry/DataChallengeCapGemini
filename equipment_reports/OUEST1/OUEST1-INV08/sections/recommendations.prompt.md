# System

You are an O&M maintenance planner for utility-scale PV plants.

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

You are writing the section "7. Recommendations" of the incident report of equipment OUEST1-INV08 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. Propose 4 to 7 concrete actions for the maintenance team, each addressing one failure mode of this equipment (thermography, IV-curve tracing, insulation resistance tests, connector torque checks, surge protection inspection, cleaning schedule, fire-risk inspection, spare parts…).
2. Address every failure mode of priority P1 ("Incendie toiture et panneaux PV"; "Dégradation et court-circuit câblage") with at least one action.
3. Use the root-cause hypotheses to choose the actions. For each action, state the expected impact qualitatively, citing only figures from the input.

Statistics and figure data for this section (every value is already computed):
```json
{
 "failure_modes": [
  {
   "failure_mode": "Incendie toiture et panneaux PV",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 25.3% of the equipment cost",
   "n_incidents": 1,
   "n_severe": 1,
   "cost_share_pct": 25.3,
   "recurrences_within_90_days": 0,
   "dominant_weather": [
    "conditions nominales"
   ]
  },
  {
   "failure_mode": "Dégradation et court-circuit câblage",
   "recommendation_priority": "P1",
   "priority_reason": "1 severe incident(s) + 1 recurrence(s) within 90 days",
   "n_incidents": 2,
   "n_severe": 1,
   "cost_share_pct": 18.8,
   "recurrences_within_90_days": 1,
   "dominant_weather": [
    "vent modéré",
    "pluie modérée"
   ]
  },
  {
   "failure_mode": "Incendie bâtiment support PV",
   "recommendation_priority": "P2",
   "priority_reason": "1 severe incident(s), 17.9% of the cost, no recurrence within 90 days",
   "n_incidents": 1,
   "n_severe": 1,
   "cost_share_pct": 17.9,
   "recurrences_within_90_days": 0,
   "dominant_weather": [
    "ciel dégagé"
   ]
  },
  {
   "failure_mode": "Dommages superficiels modules PV",
   "recommendation_priority": "P2",
   "priority_reason": "no severe incident but 13.7% of the equipment cost",
   "n_incidents": 5,
   "n_severe": 0,
   "cost_share_pct": 13.7,
   "recurrences_within_90_days": 1,
   "dominant_weather": [
    "orage avec grêle"
   ]
  },
  {
   "failure_mode": "Défaillance chaîne et boîtier de jonction",
   "recommendation_priority": "P2",
   "priority_reason": "2 severe incident(s), 13.0% of the cost, no recurrence within 90 days",
   "n_incidents": 2,
   "n_severe": 2,
   "cost_share_pct": 13.0,
   "recurrences_within_90_days": 0,
   "dominant_weather": [
    "ciel dégagé",
    "conditions nominales"
   ]
  },
  {
   "failure_mode": "Remplacement préventif connecteurs",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 8.1% of the cost",
   "n_incidents": 3,
   "n_severe": 0,
   "cost_share_pct": 8.1,
   "recurrences_within_90_days": 1,
   "dominant_weather": [
    "ciel dégagé",
    "temps calme",
    "vent modéré"
   ]
  },
  {
   "failure_mode": "Salissure et nettoyage modules PV",
   "recommendation_priority": "P3",
   "priority_reason": "no severe incident and 3.2% of the cost",
   "n_incidents": 1,
   "n_severe": 0,
   "cost_share_pct": 3.2,
   "recurrences_within_90_days": 0,
   "dominant_weather": [
    "conditions nominales"
   ]
  }
 ],
 "root_cause_hypotheses": [
  {
   "hypothesis": "The incidents of this equipment are primarily caused by weather-related stresses, especially during summer, leading to damages such as superficial module damage and cable degradation.",
   "failure_modes": [
    "Dommages superficiels modules PV",
    "Dégradation et court-circuit câblage"
   ]
  },
  {
   "hypothesis": "Electrical connection issues, including connector failures and junction box faults, are a significant root cause, often triggered or exacerbated by environmental factors such as wind and temperature variations.",
   "failure_modes": [
    "Remplacement préventif connecteurs",
    "Défaillance chaîne et boîtier de jonction"
   ]
  },
  {
   "hypothesis": "Certain incidents, such as the fire in the building support PV, are caused by internal faults or material failures unrelated to weather, possibly due to aging or manufacturing defects.",
   "failure_modes": [
    "Incendie bâtiment support PV"
   ]
  },
  {
   "hypothesis": "Maintenance activities, such as cleaning modules or preventive connector replacements, contribute to incident occurrence, especially when performed under favorable weather conditions.",
   "failure_modes": [
    "Salissure et nettoyage modules PV",
    "Remplacement préventif connecteurs"
   ]
  },
  {
   "hypothesis": "The overall failure pattern indicates that severe weather events, particularly hail and storms, are associated with superficial module damages, but other failure modes are more influenced by environmental conditions like wind and temperature.",
   "failure_modes": [
    "Dommages superficiels modules PV"
   ]
  }
 ]
}
```
