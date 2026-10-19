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

You are writing the section "8. Conclusion" of the incident report of equipment OUEST1-INV02 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. In 2-3 sentences: the main issue of this equipment, what to do first (the actions given) and the expected benefit.

Statistics and figure data for this section (every value is already computed):
```json
{
 "equipment": {
  "equipment_id": "OUEST1-INV02",
  "equipment_priority": "P2",
  "risk_level": "high"
 },
 "facts": [
  "Moderate and severe incidents: 13 (5 severe), 228 167 EUR in total; severe incidents account for 85.4% of this cost.",
  "The most costly single incident is #7 (Dégradation et court-circuit câblage, sévère, 2023-11-30): 45 736 EUR, 20.0% of the cost of moderate and severe incidents.",
  "The most costly failure mode is Dommages superficiels modules PV: 91 303 EUR over 5 incident(s), 40.0% of the cost.",
  "The most costly incident and the most costly failure mode are different: do not attribute one to the other.",
  "Incidents of all severities: 29 on this equipment vs 31.5 for the median equipment of the site (ratio ×0.92, IN LINE with the site median).",
  "Severe incidents: 5 on this equipment vs 4.5 for the median equipment of the site (ratio ×1.11, ABOVE the site median)."
 ],
 "failure_mode_priorities": [
  "Dommages superficiels modules PV: priority P1 (2 severe incident(s) + 40.0% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Dégradation et court-circuit câblage: priority P1 (2 severe incident(s) + 37.3% of the equipment cost).",
  "Défaillance chaîne et boîtier de jonction: priority P2 (1 severe incident(s), 13.8% of the cost, no recurrence within 90 days).",
  "Remplacement préventif connecteurs: priority P3 (no severe incident and 3.9% of the cost).",
  "Baisse de rendement onduleur: priority P3 (no severe incident and 3.0% of the cost).",
  "Incendie toiture et panneaux PV: priority P3 (no severe incident and 1.9% of the cost)."
 ],
 "first_actions": [
  {
   "priority": "P1",
   "action": "Perform thermography inspections on PV modules to identify superficial damages caused by severe weather, especially 'vent fort / tempête', and address any hot spots.",
   "failure_mode": "Dommages superficiels modules PV"
  },
  {
   "priority": "P1",
   "action": "Conduct IV-curve tracing tests to detect degradation and short-circuit issues in the wiring, focusing on the DC field.",
   "failure_mode": "Dégradation et court-circuit câblage"
  },
  {
   "priority": "P1",
   "action": "Schedule regular insulation resistance tests on the DC field to monitor aging and environmental effects on wiring insulation.",
   "failure_mode": "Dégradation et court-circuit câblage"
  },
  {
   "priority": "P1",
   "action": "Establish a cleaning schedule for the PV modules and DC field to remove dirt and debris, particularly after moderate rain events.",
   "failure_mode": "Dommages superficiels modules PV"
  }
 ]
}
```
