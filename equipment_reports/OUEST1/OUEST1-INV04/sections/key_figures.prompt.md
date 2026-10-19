# System

You are an asset-performance analyst who benchmarks PV inverters against the other inverters of their site.

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

You are writing the section "1. Key figures" of the incident report of equipment OUEST1-INV04 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. On which indicators does this equipment stand out from the median equipment of its site, and on which is it in line? Quote the ratios as written in `facts`.
2. Why was this equipment selected (`why_selected`) and what does its priority mean for the reader?
3. How concentrated is the cost on severe incidents?

Statistics and figure data for this section (every value is already computed):
```json
{
 "equipment": {
  "equipment_id": "OUEST1-INV04",
  "site": "Centrale PV Ouest-1",
  "asset_type": "PV inverter and the DC field upstream of it",
  "equipment_priority": "P2",
  "risk_level": "high",
  "criticality_score_within_site": 56.4,
  "criticality_score_vs_fleet": 88.8,
  "rank_within_site": 5,
  "n_equipment_on_site": 10,
  "why_selected": "criticality score 56.4 (below the threshold of 75) against the other equipment of the site and 88.8 (at or above the threshold of 75) against the whole solar fleet"
 },
 "comparison_with_site_median_equipment": {
  "incidents_all_severities": {
   "this_equipment": 38,
   "site_median_equipment": 31.5,
   "ratio_to_site_median": 1.21
  },
  "severe_incidents": {
   "this_equipment": 4,
   "site_median_equipment": 4.5,
   "ratio_to_site_median": 0.89
  },
  "cost_all_severities_eur": {
   "this_equipment": 247736,
   "site_median_equipment": 212067,
   "ratio_to_site_median": 1.17
  },
  "downtime_all_severities_h": {
   "this_equipment": 563.4,
   "site_median_equipment": 473.8,
   "ratio_to_site_median": 1.19
  }
 },
 "key_figures_moderate_and_severe": {
  "n_incidents": 16,
  "n_moderate": 12,
  "n_severe": 4,
  "severe_share_of_incidents_pct": 25.0,
  "cost_total_eur": 232135,
  "cost_mean_eur": 14508,
  "cost_median_eur": 6694,
  "severe_share_of_cost_pct": 72.4,
  "downtime_total_h": 494.6,
  "downtime_mean_h": 30.9,
  "mean_days_between_incidents": 62,
  "first_incident": "#1 on 2023-05-30",
  "last_incident": "#16 on 2025-12-08"
 },
 "facts": [
  "Incidents of all severities: 38 on this equipment vs 31.5 for the median equipment of the site (ratio ×1.21, ABOVE the site median).",
  "Severe incidents: 4 on this equipment vs 4.5 for the median equipment of the site (ratio ×0.89, BELOW the site median).",
  "Estimated cost of all incidents: 247 736 EUR on this equipment vs 212 067 EUR for the median equipment of the site (ratio ×1.17, ABOVE the site median).",
  "Downtime of all incidents: 563.4 h on this equipment vs 473.8 h for the median equipment of the site (ratio ×1.19, ABOVE the site median).",
  "Moderate and severe incidents: 16 (4 severe), 232 135 EUR in total; severe incidents account for 72.4% of this cost."
 ]
}
```
