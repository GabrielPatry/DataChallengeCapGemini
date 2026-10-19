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

You are writing the section "4. Weather exposure" of the incident report of equipment OUEST1-INV03 (site: Centrale PV Ouest-1).

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
    "weather_condition": "ciel dégagé",
    "n_incidents": 2,
    "n_severe": 2,
    "incidents": [
     "#4",
     "#10"
    ],
    "downtime_total_h": 159.0,
    "downtime_median_h": 79.5,
    "downtime_max_h": 91.8,
    "share_of_equipment_downtime_pct": 28.7,
    "share_of_equipment_incidents_pct": 15.4,
    "share_of_site_incidents_pct": 13.6,
    "representation": "in line with site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "temps calme",
    "n_incidents": 3,
    "n_severe": 3,
    "incidents": [
     "#1",
     "#11",
     "#13"
    ],
    "downtime_total_h": 113.8,
    "downtime_median_h": 41.4,
    "downtime_max_h": 46.5,
    "share_of_equipment_downtime_pct": 20.6,
    "share_of_equipment_incidents_pct": 23.1,
    "share_of_site_incidents_pct": 17.4,
    "representation": "over-represented vs site",
    "sample": "ok"
   },
   {
    "weather_condition": "vent fort / tempête",
    "n_incidents": 3,
    "n_severe": 1,
    "incidents": [
     "#2",
     "#5",
     "#9"
    ],
    "downtime_total_h": 101.7,
    "downtime_median_h": 14.0,
    "downtime_max_h": 74.0,
    "share_of_equipment_downtime_pct": 18.4,
    "share_of_equipment_incidents_pct": 23.1,
    "share_of_site_incidents_pct": 15.9,
    "representation": "over-represented vs site",
    "sample": "ok"
   },
   {
    "weather_condition": "vent modéré",
    "n_incidents": 1,
    "n_severe": 1,
    "incidents": [
     "#3"
    ],
    "downtime_total_h": 78.3,
    "downtime_median_h": 78.3,
    "downtime_max_h": 78.3,
    "share_of_equipment_downtime_pct": 14.1,
    "share_of_equipment_incidents_pct": 7.7,
    "share_of_site_incidents_pct": 9.8,
    "representation": "in line with site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "orage avec grêle",
    "n_incidents": 1,
    "n_severe": 1,
    "incidents": [
     "#8"
    ],
    "downtime_total_h": 51.9,
    "downtime_median_h": 51.9,
    "downtime_max_h": 51.9,
    "share_of_equipment_downtime_pct": 9.4,
    "share_of_equipment_incidents_pct": 7.7,
    "share_of_site_incidents_pct": 12.1,
    "representation": "under-represented vs site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "conditions nominales",
    "n_incidents": 2,
    "n_severe": 0,
    "incidents": [
     "#6",
     "#12"
    ],
    "downtime_total_h": 42.5,
    "downtime_median_h": 21.2,
    "downtime_max_h": 24.0,
    "share_of_equipment_downtime_pct": 7.7,
    "share_of_equipment_incidents_pct": 15.4,
    "share_of_site_incidents_pct": 12.1,
    "representation": "in line with site",
    "sample": "indicative only (fewer than 3 incidents)"
   },
   {
    "weather_condition": "pluie modérée",
    "n_incidents": 1,
    "n_severe": 0,
    "incidents": [
     "#7"
    ],
    "downtime_total_h": 6.5,
    "downtime_median_h": 6.5,
    "downtime_max_h": 6.5,
    "share_of_equipment_downtime_pct": 1.2,
    "share_of_equipment_incidents_pct": 7.7,
    "share_of_site_incidents_pct": 18.9,
    "representation": "under-represented vs site",
    "sample": "indicative only (fewer than 3 incidents)"
   }
  ]
 },
 "failure_modes_vs_weather_figure": {
  "figure": "Failure modes vs weather condition",
  "how_to_read": "Number of incidents per failure mode (rows) and weather condition. A weather condition absent from a failure mode's row never occurred with that failure mode.",
  "matrix": {
   "Baisse de rendement onduleur": {
    "ciel dégagé": 1,
    "temps calme": 1
   },
   "Dommages superficiels modules PV": {
    "vent fort / tempête": 3,
    "orage avec grêle": 1
   },
   "Dégradation et court-circuit câblage": {
    "ciel dégagé": 1,
    "vent modéré": 1
   },
   "Incendie bâtiment support PV": {
    "temps calme": 1
   },
   "Incendie toiture et panneaux PV": {
    "conditions nominales": 1,
    "temps calme": 1
   },
   "Remplacement préventif connecteurs": {
    "conditions nominales": 1
   },
   "Salissure et nettoyage modules PV": {
    "pluie modérée": 1
   }
  }
 },
 "facts": [
  "Most downtime occurs under 'ciel dégagé': 159.0 h over 2 incident(s), 28.7% of the downtime (in line with site).",
  "'temps calme' is over-represented vs site: 23.1% of the incidents of this equipment vs 17.4% on the site.",
  "'vent fort / tempête' is over-represented vs site: 23.1% of the incidents of this equipment vs 15.9% on the site.",
  "'orage avec grêle' is under-represented vs site: 7.7% of the incidents of this equipment vs 12.1% on the site (indicative only).",
  "'pluie modérée' is under-represented vs site: 7.7% of the incidents of this equipment vs 18.9% on the site (indicative only)."
 ]
}
```
