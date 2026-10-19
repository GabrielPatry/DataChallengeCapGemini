# System

You are the reliability manager who signs off equipment reports.

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

You are writing the section "8. Conclusion" of the incident report of equipment OUEST1-INV04 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. In 2-3 sentences: the main issue of this equipment, what to do first (the actions given) and the expected benefit.

Statistics and figure data for this section (every value is already computed):
```json
{
 "equipment": {
  "equipment_id": "OUEST1-INV04",
  "equipment_priority": "P2",
  "risk_level": "high"
 },
 "facts": [
  "Moderate and severe incidents: 16 (4 severe), 232 135 EUR in total; severe incidents account for 72.4% of this cost.",
  "The most costly single incident is #13 (Salissure et nettoyage modules PV, sévère, 2025-07-23): 55 925 EUR, 24.1% of the cost of moderate and severe incidents.",
  "The most costly failure mode is Dégradation et court-circuit câblage: 88 376 EUR over 3 incident(s), 38.1% of the cost.",
  "The most costly incident and the most costly failure mode are different: do not attribute one to the other.",
  "Incidents of all severities: 38 on this equipment vs 31.5 for the median equipment of the site (ratio ×1.21, ABOVE the site median).",
  "Severe incidents: 4 on this equipment vs 4.5 for the median equipment of the site (ratio ×0.89, BELOW the site median)."
 ],
 "failure_mode_priorities": [
  "Dégradation et court-circuit câblage: priority P1 (2 severe incident(s) + 38.1% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Salissure et nettoyage modules PV: priority P1 (1 severe incident(s) + 25.9% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Défaillance chaîne et boîtier de jonction: priority P2 (1 severe incident(s), 13.4% of the cost, no recurrence within 90 days).",
  "Incendie toiture et panneaux PV: priority P3 (no severe incident and 8.8% of the cost).",
  "Dommages superficiels modules PV: priority P3 (no severe incident and 7.4% of the cost).",
  "Remplacement préventif connecteurs: priority P3 (no severe incident and 6.4% of the cost)."
 ],
 "first_actions": [
  {
   "priority": "P1",
   "action": "Perform thermography inspections to identify hot spots and potential short circuits in wiring, especially after rainy conditions.",
   "failure_mode": "Dégradation et court-circuit câblage"
  },
  {
   "priority": "P1",
   "action": "Conduct IV-curve tracing and insulation resistance tests to verify electrical integrity of the PV strings and identify degradation or insulation issues.",
   "failure_mode": "Dégradation et court-circuit câblage"
  },
  {
   "priority": "P1",
   "action": "Implement a regular cleaning schedule for modules to prevent dirt accumulation, especially after moderate rain events, to mitigate contamination.",
   "failure_mode": "Salissure et nettoyage modules PV"
  },
  {
   "priority": "P1",
   "action": "Review and stock spare parts for critical components such as connectors and junction boxes to enable prompt corrective actions when failures occur.",
   "failure_mode": "Dégradation et court-circuit câblage"
  }
 ]
}
```
