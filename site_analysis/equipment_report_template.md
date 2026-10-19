# {{ report_title }}

**Equipment:** {{ equipment_id }} · **Site:** {{ site }} · **Asset type:** {{ asset_label }} · **Generated on:** {{ generation_date }}

> {{ synopsis }}

**Risk level: {{ risk_level }}** — {{ risk_justification }}

---

## 1. Key figures

| Indicator | This equipment | Median equipment of the site |
| --- | ---: | ---: |
| Incidents (all severities) | {{ n_incidents_all }} | {{ site_median_n_incidents }} |
| Severe incidents | {{ n_severe }} | {{ site_median_n_severe }} |
| Total estimated cost (all severities) | {{ total_cost_all_eur }} EUR | {{ site_median_cost_eur }} EUR |
| Total downtime (all severities) | {{ total_downtime_all_hours }} h | {{ site_median_downtime_hours }} h |

| Moderate + severe incidents (scope of this report) | Value |
| --- | ---: |
| Incidents analysed | {{ n_focus }} ({{ n_moderate }} moderate · {{ n_severe }} severe) |
| Period covered | {{ period_start }} → {{ period_end }} |
| Total estimated cost | {{ total_cost_focus_eur }} EUR |
| Average cost per incident | {{ avg_cost_focus_eur }} EUR |
| Total downtime | {{ total_downtime_focus_hours }} h |
| Most costly cluster | {{ top_cluster_by_cost }} |
| Weather with most downtime | {{ top_weather_by_downtime }} |

**Criticality score:** {{ score_site }}/100 within the site (rank {{ rank_in_site }}/{{ n_equipment_site }}) · {{ score_fleet }}/100 against the whole solar fleet.

## 2. Methodology

{{ methodology }}

## 3. Cost timeline

{{ figure_cost_timeline }}

*Estimated cost of each moderate (hollow) and severe (filled) incident over time. Colour = cluster family, marker shape = cluster.*

{{ yearly_table }}

{{ timeline_analysis }}

## 4. Weather exposure

### 4.1 Downtime vs weather condition

{{ figure_downtime_weather }}

*Downtime of each moderate/severe incident per weather condition; the black tick is the median.*

{{ downtime_weather_table }}

{{ weather_downtime_analysis }}

### 4.2 Failure modes vs weather condition

{{ figure_cluster_weather }}

*Number of moderate/severe incidents per cluster and weather condition.*

{{ cluster_weather_analysis }}

## 5. Failure modes (clusters)

{{ cluster_table }}

{{ cluster_sections }}

## 6. Root-cause hypotheses

{{ root_causes }}

## 7. Recommendations

{{ recommendations }}

## 8. Data limitations

{{ limitations }}

## 9. Conclusion

{{ conclusion }}
