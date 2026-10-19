# {{ report_title }}

**Equipment:** {{ equipment_id }} · **Site:** {{ site }} · **Asset type:** {{ asset_label }} · **Generated on:** {{ generation_date }}

> {{ synopsis }}

**Equipment priority: {{ equipment_priority }} · Risk level: {{ risk_level }}** — {{ risk_justification }}

---

## 1. Key figures

| Indicator | This equipment | Median equipment of the site | Ratio |
| --- | ---: | ---: | ---: |
| Incidents (all severities) | {{ n_incidents_all }} | {{ site_median_n_incidents }} | ×{{ ratio_n_incidents }} |
| Severe incidents | {{ n_severe_all }} | {{ site_median_n_severe }} | ×{{ ratio_n_severe }} |
| Total estimated cost (all severities) | {{ total_cost_all_eur }} EUR | {{ site_median_cost_eur }} EUR | ×{{ ratio_cost }} |
| Total downtime (all severities) | {{ total_downtime_all_hours }} h | {{ site_median_downtime_hours }} h | ×{{ ratio_downtime }} |

| Moderate and severe incidents (scope of this report) | Value |
| --- | ---: |
| Incidents analysed | {{ n_focus }} ({{ n_moderate }} moderate · {{ n_severe }} severe) |
| Period covered | {{ period_start }} → {{ period_end }} |
| Total estimated cost | {{ total_cost_focus_eur }} EUR ({{ severe_share_of_cost }} % from severe incidents) |
| Average cost per incident | {{ avg_cost_focus_eur }} EUR |
| Total downtime | {{ total_downtime_focus_hours }} h |
| Average interval between incidents | {{ mean_days_between }} days |
| Most costly failure mode | {{ top_cluster_by_cost }} |
| Weather with most downtime | {{ top_weather_by_downtime }} |

## 2. How this report was built

{{ methodology }}

## 3. Cost timeline

{{ figure_cost_timeline }}

*Estimated cost of each moderate (hollow) and severe (filled) incident. Colour = family of failure modes, marker shape = failure mode; the three most costly incidents are labelled.*

{{ yearly_table }}

{{ timeline_analysis }}

## 4. Weather exposure

### 4.1 Downtime vs weather condition

{{ figure_downtime_weather }}

*Downtime of each incident per weather condition; the black tick is the median.*

{{ downtime_weather_table }}

{{ weather_downtime_analysis }}

### 4.2 Failure modes vs weather condition

{{ figure_cluster_weather }}

*Number of incidents per failure mode and weather condition.*

{{ cluster_weather_analysis }}

## 5. Failure modes

{{ cluster_table }}

{{ cluster_sections }}

## 6. Root-cause hypotheses

{{ root_causes }}

## 7. Recommendations

{{ recommendations }}

## 8. Conclusion

{{ conclusion }}

---

### Annex — Incident register

{{ incident_register }}
