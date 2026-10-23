# {{ report_title }}

**Asset type:** {{ asset_label }} · **Generated on:** {{ generation_date }}
# Synopsis
> {{ synopsis }}

---

## 1. Key figures

| Indicator | Value |
| --- | ---: |
| Incidents analysed | {{ n_incidents }} |
| Sites covered | {{ n_sites }} |
| Equipment monitored | {{ n_equipment }} |
| Period covered | {{ period_start }} → {{ period_end }} |
| Total estimated cost | {{ total_cost_eur }} EUR |
| Total downtime | {{ total_downtime_hours }} h |
| Average cost per incident | {{ avg_cost_per_incident }} EUR |

**Severity breakdown:** {{ n_minor }} minor · {{ n_moderate }} moderate · {{ n_severe }} severe

**Most costly site:** {{ top_site_by_cost }} — **most costly equipment:** {{ top_equipment_by_cost }}

## 2. Cost analysis

{{ methodology }}

### 2.1 Cost per site

{{ figure_plot_total_cost_by_site }}

*Total estimated cost per site, split by asset type.*

### 2.2 Cost distribution per equipment

{{ figure_plot_cost_distribution_per_equipment_by_site }}

*Distribution of the total estimated cost per equipment, grouped by site.*

### 2.3 Daily cost of the most impacted equipment

{{ figure_plot_daily_cost_for_equipment }}

*Daily estimated cost over time for the equipment with the highest total cost.*

### 2.4 Top equipment at the highest-cost site

{{ figure_plot_daily_cost_top_equipment_at_top_site }}

*Daily estimated cost of the top-3 equipment at the site with the highest total cost.*

### 2.5 Downtime vs cost

{{ figure_plot_downtime_vs_cost }}

*Estimated cost against downtime duration, coloured by severity.*

## 3. Temporal and severity analysis

### 3.1 Monthly incident count

{{ figure_plot_monthly_incident_count }}

*Number of incidents per month over the period, split by asset type.*

### 3.2 Incidents by severity

{{ figure_plot_incident_count_by_severity }}

*Number of incidents per severity level, split by asset type.*

### 3.3 Weather conditions

{{ figure_plot_total_cost_by_weather_condition }}

*Total estimated cost per weather condition, split by asset type.*

## 4. Thematic clusters

{{ n_clusters }} incident clusters were identified from the report descriptions.

{{ top_clusters_table }}

{{ cluster_sections }}

## 5. Recommendations

{{ recommendations }}

## 6. Conclusion

{{ conclusion }}
