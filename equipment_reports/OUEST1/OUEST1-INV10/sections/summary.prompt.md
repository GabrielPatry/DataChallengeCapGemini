# System

You are an executive-summary writer for asset managers of PV plants.

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

You are writing the section "Title and executive summary" of the incident report of equipment OUEST1-INV10 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. Give the report a short title naming the equipment ID and its main failure modes.
2. Write a 3-4 sentence executive summary: what fails, how much it costs, how the equipment compares with its site and what to do first.

Statistics and figure data for this section (every value is already computed):
```json
{
 "equipment": {
  "equipment_id": "OUEST1-INV10",
  "site": "Centrale PV Ouest-1",
  "asset_type": "PV inverter and the DC field upstream of it",
  "equipment_priority": "P2",
  "risk_level": "high",
  "criticality_score_within_site": 64.3,
  "criticality_score_vs_fleet": 86.2,
  "rank_within_site": 3,
  "n_equipment_on_site": 10,
  "why_selected": "criticality score 64.3 (below the threshold of 75) against the other equipment of the site and 86.2 (at or above the threshold of 75) against the whole solar fleet"
 },
 "facts": [
  "Incidents of all severities: 29 on this equipment vs 31.5 for the median equipment of the site (ratio ×0.92, IN LINE with the site median).",
  "Severe incidents: 6 on this equipment vs 4.5 for the median equipment of the site (ratio ×1.33, ABOVE the site median).",
  "Moderate and severe incidents: 15 (6 severe), 206 762 EUR in total; severe incidents account for 74.9% of this cost.",
  "The most costly single incident is #3 (Dégradation et court-circuit câblage, sévère, 2023-11-21): 49 142 EUR, 23.8% of the cost of moderate and severe incidents.",
  "The most costly failure mode is Incendie bâtiment support PV: 51 131 EUR over 2 incident(s), 24.7% of the cost.",
  "The most costly incident and the most costly failure mode are different: do not attribute one to the other.",
  "From 2023 to 2025 the cost changed by -78.1% (trend: decreasing)."
 ],
 "failure_mode_priorities": [
  "Incendie bâtiment support PV: priority P1 (2 severe incident(s) + 24.7% of the equipment cost + 1 recurrence(s) within 90 days).",
  "Dégradation et court-circuit câblage: priority P1 (1 severe incident(s) + 23.8% of the equipment cost).",
  "Baisse de rendement onduleur: priority P1 (1 severe incident(s) + 21.6% of the equipment cost).",
  "Salissure et nettoyage modules PV: priority P1 (1 severe incident(s) + 1 recurrence(s) within 90 days).",
  "Défaillance chaîne et boîtier de jonction: priority P2 (1 severe incident(s), 8.5% of the cost, no recurrence within 90 days).",
  "Incendie toiture et panneaux PV: priority P3 (no severe incident and 4.7% of the cost).",
  "Dommages superficiels modules PV: priority P3 (no severe incident and 1.2% of the cost)."
 ],
 "first_actions": [
  {
   "priority": "P1",
   "action": "Perform thermography inspections on the inverter to identify hot spots indicating potential failure modes.",
   "failure_mode": "Baisse de rendement onduleur"
  },
  {
   "priority": "P1",
   "action": "Conduct IV-curve tracing and insulation resistance tests on the DC field upstream to detect degradation or short circuits.",
   "failure_mode": "Dégradation et court-circuit câblage"
  },
  {
   "priority": "P1",
   "action": "Implement a regular connector torque check schedule for all DC field connections.",
   "failure_mode": "Dégradation et court-circuit câblage"
  },
  {
   "priority": "P1",
   "action": "Inspect and upgrade surge protection devices in the DC field to prevent damage from electrical surges.",
   "failure_mode": "Incendie bâtiment support PV"
  },
  {
   "priority": "P1",
   "action": "Establish a cleaning schedule for modules to reduce dirt accumulation, especially under conditions of 'ciel dégagé' and 'vent modéré'.",
   "failure_mode": "Salissure et nettoyage modules PV"
  },
  {
   "priority": "P1",
   "action": "Maintain a stock of critical spare parts for the inverter and DC connectors to enable quick corrective actions.",
   "failure_mode": "Baisse de rendement onduleur"
  }
 ]
}
```
