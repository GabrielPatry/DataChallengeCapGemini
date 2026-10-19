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

You are writing the section "4. Weather exposure" of the incident report of equipment OUEST1-INV02 (site: Centrale PV Ouest-1).

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
    "n_severe": 2,
    "incidents": [
     "#2",
     "#5",
     "#6",
     "#8"
    ],
    "downtime_total_h": 171.5,
    "downtime_median_h": 34.6,
    "downtime_max_h": 94.0,
    "share_of_equipment_downtime_pct": 37.6,
    "share_of_equipment_incidents_pct": 30.8,
    "share_of_site_incidents_pct": 15.9,
    "representation": "over-represented vs site",
    "sample": "ok"
   },
   {
    "weather_condition": "vent modéré",
    "n_incidents": 2,
    "n_severe": 1,
    "incidents": [
     "#3",
     "#11"
    ],
    "downtime_total_h": 84.6,
    "downtime_median_h": 42.3,
    "downtime_max_h": 72.9,
    "share_of_equipment_downtime_pct": 18.5,
    "share_of_equipment_incidents_pct": 15.4,
    "share_of_site_incidents_pct": 9.8,
    "representation": "over-represented vs site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "temps calme",
    "n_incidents": 1,
    "n_severe": 1,
    "incidents": [
     "#7"
    ],
    "downtime_total_h": 77.7,
    "downtime_median_h": 77.7,
    "downtime_max_h": 77.7,
    "share_of_equipment_downtime_pct": 17.0,
    "share_of_equipment_incidents_pct": 7.7,
    "share_of_site_incidents_pct": 17.4,
    "representation": "under-represented vs site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "conditions nominales",
    "n_incidents": 2,
    "n_severe": 1,
    "incidents": [
     "#10",
     "#12"
    ],
    "downtime_total_h": 75.5,
    "downtime_median_h": 37.8,
    "downtime_max_h": 52.2,
    "share_of_equipment_downtime_pct": 16.5,
    "share_of_equipment_incidents_pct": 15.4,
    "share_of_site_incidents_pct": 12.1,
    "representation": "in line with site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "orage avec grêle",
    "n_incidents": 1,
    "n_severe": 0,
    "incidents": [
     "#13"
    ],
    "downtime_total_h": 17.3,
    "downtime_median_h": 17.3,
    "downtime_max_h": 17.3,
    "share_of_equipment_downtime_pct": 3.8,
    "share_of_equipment_incidents_pct": 7.7,
    "share_of_site_incidents_pct": 12.1,
    "representation": "under-represented vs site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "ciel dégagé",
    "n_incidents": 1,
    "n_severe": 0,
    "incidents": [
     "#4"
    ],
    "downtime_total_h": 16.6,
    "downtime_median_h": 16.6,
    "downtime_max_h": 16.6,
    "share_of_equipment_downtime_pct": 3.6,
    "share_of_equipment_incidents_pct": 7.7,
    "share_of_site_incidents_pct": 13.6,
    "representation": "under-represented vs site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "pluie modérée",
    "n_incidents": 2,
    "n_severe": 0,
    "incidents": [
     "#1",
     "#9"
    ],
    "downtime_total_h": 13.0,
    "downtime_median_h": 6.5,
    "downtime_max_h": 7.4,
    "share_of_equipment_downtime_pct": 2.8,
    "share_of_equipment_incidents_pct": 15.4,
    "share_of_site_incidents_pct": 18.9,
    "representation": "in line with site",
    "sample": "indicative only (fewer than 3 incidents)"
   }
  ]
 },
 "failure_modes_vs_weather_figure": {
  "figure": "Failure modes vs weather condition",
  "how_to_read": "Number of incidents per failure mode (rows) and weather condition. A weather condition absent from a failure mode's row never occurred with that failure mode.",
  "matrix": {
   "Baisse de rendement onduleur": {
    "conditions nominales": 1
   },
   "Dommages superficiels modules PV": {
    "vent fort / tempête": 4,
    "orage avec grêle": 1
   },
   "Défaillance chaîne et boîtier de jonction": {
    "conditions nominales": 1
   },
   "Dégradation et court-circuit câblage": {
    "temps calme": 1,
    "vent modéré": 1
   },
   "Incendie toiture et panneaux PV": {
    "pluie modérée": 2
   },
   "Remplacement préventif connecteurs": {
    "ciel dégagé": 1,
    "vent modéré": 1
   }
  }
 },
 "facts": [
  "Most downtime occurs under 'vent fort / tempête': 171.5 h over 4 incident(s), 37.6% of the downtime (over-represented vs site).",
  "'vent fort / tempête' is over-represented vs site: 30.8% of the incidents of this equipment vs 15.9% on the site.",
  "'vent modéré' is over-represented vs site: 15.4% of the incidents of this equipment vs 9.8% on the site (indicative only).",
  "'temps calme' is under-represented vs site: 7.7% of the incidents of this equipment vs 17.4% on the site (indicative only).",
  "'orage avec grêle' is under-represented vs site: 7.7% of the incidents of this equipment vs 12.1% on the site (indicative only).",
  "'ciel dégagé' is under-represented vs site: 7.7% of the incidents of this equipment vs 13.6% on the site (indicative only)."
 ]
}
```
