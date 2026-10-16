# {{ report_title }}

**Asset type:** {{ asset_label }} · **Generated on:** {{ generation_date }}

> {{ synopsis }}

---

## 1. Key figures

| Indicator | Value |
| --- | ---: |
| Incidents analysed | {{ n_incidents }} |
| Sites covered | {{ n_sites }} |
| Turbines monitored | {{ n_equipment }} |
| Period covered | {{ period_start }} → {{ period_end }} |
| Total estimated cost | {{ total_cost_eur }} EUR |
| Total downtime | {{ total_downtime_hours }} h |
| Average cost per incident | {{ avg_cost_per_incident }} EUR |

**Severity breakdown:** {{ n_minor }} minor · {{ n_moderate }} moderate · {{ n_severe }} severe

**Most costly site:** {{ top_site_by_cost }} — **most costly turbine:** {{ top_equipment_by_cost }}

## 2. Cost analysis

{{ methodology }}

### 2.1 Cost per site

{{ figure_plot_total_cost_by_site }}

*Total estimated cost per wind farm, split by asset type.*

### 2.2 Cost distribution per turbine

{{ figure_plot_cost_distribution_per_equipment_by_site }}

*Distribution of the total estimated cost per turbine, grouped by site.*

### 2.3 Daily cost of the most impacted turbine

{{ figure_plot_daily_cost_for_equipment }}

*Daily estimated cost over time for the turbine with the highest total cost.*

### 2.4 Top turbines at the highest-cost site

{{ figure_plot_daily_cost_top_equipment_at_top_site }}

*Daily estimated cost of the top-3 turbines at the site with the highest total cost.*

### 2.5 Downtime vs cost

{{ figure_plot_downtime_vs_cost }}

*Estimated cost against downtime duration, coloured by severity.*

## 3. Weather exposure

Wind assets are directly exposed to meteorological conditions: the figures
below relate incident dynamics and costs to the weather recorded at the time
of each event.

### 3.1 Cost by weather condition

{{ figure_plot_total_cost_by_weather_condition }}

*Total estimated cost per weather condition, split by asset type — storm-related conditions stand out.*

### 3.2 Monthly incident count

{{ figure_plot_monthly_incident_count }}

*Number of incidents per month over the period, split by asset type.*

### 3.3 Incidents by severity

{{ figure_plot_incident_count_by_severity }}

*Number of incidents per severity level, split by asset type.*

## 4. Thematic clusters

{{ n_clusters }} incident clusters were identified from the report descriptions.

{{ top_clusters_table }}

{{ cluster_sections }}

## 5. Recommendations

{{ recommendations }}

## 6. Conclusion

{{ conclusion }}
