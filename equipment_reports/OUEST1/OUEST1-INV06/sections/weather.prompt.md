# System

You are an engineer specialised in the weather and environmental exposure of PV plants.

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

You are writing the section "4. Weather exposure" of the incident report of equipment OUEST1-INV06 (site: Centrale PV Ouest-1).

Language of every text field: English.

Answer these questions:
1. Under which weather conditions does this equipment lose the most hours? Are these conditions over- or under-represented compared with the rest of the site (`representation`)?
2. Which failure modes occur under which weather conditions? Read each row of the matrix: link a weather condition to a failure mode only if it appears in that row. What does it imply for operations (e.g. inspections after a given weather event)?

Statistics and figure data for this section (every value is already computed):
```json
{
 "downtime_vs_weather_figure": {
  "figure": "Downtime vs weather condition",
  "how_to_read": "Rows sorted by total downtime. 'representation' compares the share of the equipment's incidents under this weather with the share on the whole site.",
  "rows": [
   {
    "weather_condition": "vent fort / tempête",
    "n_incidents": 4,
    "n_severe": 4,
    "incidents": [
     "#7",
     "#11",
     "#12",
     "#14"
    ],
    "downtime_total_h": 315.5,
    "downtime_median_h": 79.8,
    "downtime_max_h": 98.3,
    "share_of_equipment_downtime_pct": 41.4,
    "share_of_equipment_incidents_pct": 20.0,
    "share_of_site_incidents_pct": 15.9,
    "representation": "in line with site",
    "sample": "ok"
   },
   {
    "weather_condition": "pluie modérée",
    "n_incidents": 5,
    "n_severe": 2,
    "incidents": [
     "#2",
     "#3",
     "#5",
     "#8",
     "#10"
    ],
    "downtime_total_h": 167.5,
    "downtime_median_h": 12.0,
    "downtime_max_h": 78.0,
    "share_of_equipment_downtime_pct": 22.0,
    "share_of_equipment_incidents_pct": 25.0,
    "share_of_site_incidents_pct": 18.9,
    "representation": "over-represented vs site",
    "sample": "ok"
   },
   {
    "weather_condition": "orage avec grêle",
    "n_incidents": 4,
    "n_severe": 2,
    "incidents": [
     "#6",
     "#9",
     "#17",
     "#19"
    ],
    "downtime_total_h": 113.4,
    "downtime_median_h": 15.9,
    "downtime_max_h": 74.6,
    "share_of_equipment_downtime_pct": 14.9,
    "share_of_equipment_incidents_pct": 20.0,
    "share_of_site_incidents_pct": 12.1,
    "representation": "over-represented vs site",
    "sample": "ok"
   },
   {
    "weather_condition": "conditions nominales",
    "n_incidents": 2,
    "n_severe": 1,
    "incidents": [
     "#4",
     "#18"
    ],
    "downtime_total_h": 95.6,
    "downtime_median_h": 47.8,
    "downtime_max_h": 86.9,
    "share_of_equipment_downtime_pct": 12.5,
    "share_of_equipment_incidents_pct": 10.0,
    "share_of_site_incidents_pct": 12.1,
    "representation": "in line with site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "ciel dégagé",
    "n_incidents": 2,
    "n_severe": 0,
    "incidents": [
     "#16",
     "#20"
    ],
    "downtime_total_h": 30.9,
    "downtime_median_h": 15.4,
    "downtime_max_h": 16.5,
    "share_of_equipment_downtime_pct": 4.1,
    "share_of_equipment_incidents_pct": 10.0,
    "share_of_site_incidents_pct": 13.6,
    "representation": "in line with site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "temps calme",
    "n_incidents": 2,
    "n_severe": 0,
    "incidents": [
     "#13",
     "#15"
    ],
    "downtime_total_h": 24.8,
    "downtime_median_h": 12.4,
    "downtime_max_h": 13.1,
    "share_of_equipment_downtime_pct": 3.3,
    "share_of_equipment_incidents_pct": 10.0,
    "share_of_site_incidents_pct": 17.4,
    "representation": "under-represented vs site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "vent modéré",
    "n_incidents": 1,
    "n_severe": 0,
    "incidents": [
     "#1"
    ],
    "downtime_total_h": 14.5,
    "downtime_median_h": 14.5,
    "downtime_max_h": 14.5,
    "share_of_equipment_downtime_pct": 1.9,
    "share_of_equipment_incidents_pct": 5.0,
    "share_of_site_incidents_pct": 9.8,
    "representation": "under-represented vs site",
    "sample": "indicative only (fewer than 3 incidents)"
   }
  ]
 },
 "failure_modes_vs_weather_figure": {
  "figure": "Failure modes vs weather condition",
  "how_to_read": "Number of incidents per failure mode (rows) and weather condition. A weather condition absent from a failure mode's row never occurred with that failure mode.",
  "matrix": {
   "Dommages superficiels modules PV": {
    "vent fort / tempête": 4,
    "orage avec grêle": 4
   },
   "Défaillance chaîne et boîtier de jonction": {
    "pluie modérée": 2
   },
   "Dégradation et court-circuit câblage": {
    "ciel dégagé": 1,
    "conditions nominales": 1,
    "temps calme": 1,
    "vent modéré": 1
   },
   "Incendie toiture et panneaux PV": {
    "conditions nominales": 1,
    "temps calme": 1,
    "pluie modérée": 3
   },
   "Remplacement préventif connecteurs": {
    "ciel dégagé": 1
   }
  }
 },
 "facts": [
  "Most downtime occurs under 'vent fort / tempête': 315.5 h over 4 incident(s), 41.4% of the downtime (in line with site).",
  "'pluie modérée' is over-represented vs site: 25.0% of the incidents of this equipment vs 18.9% on the site.",
  "'orage avec grêle' is over-represented vs site: 20.0% of the incidents of this equipment vs 12.1% on the site.",
  "'temps calme' is under-represented vs site: 10.0% of the incidents of this equipment vs 17.4% on the site (indicative only).",
  "'vent modéré' is under-represented vs site: 5.0% of the incidents of this equipment vs 9.8% on the site (indicative only)."
 ]
}
```
