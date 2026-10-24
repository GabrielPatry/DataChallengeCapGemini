# {{ report_title }}

**Type d'actif :** {{ asset_label }} · **Généré le :** {{ generation_date }}

## Synopsis
> {{ synopsis }}

---

## 1. Chiffres clés

| Indicateur | Valeur |
| --- | ---: |
| Incidents analysed | {{ n_incidents }} |
| Sites covered | {{ n_sites }} |
| Equipment monitored | {{ n_equipment }} |
| Period covered | {{ period_start }} → {{ period_end }} |
| Total estimated cost | {{ total_cost_eur }} EUR |
| Total downtime | {{ total_downtime_hours }} h |
| Average cost per incident | {{ avg_cost_per_incident }} EUR |
| Median cost per incident | {{ median_cost_per_incident }} EUR |
| Average downtime per incident | {{ avg_downtime_per_incident }} h |
| Median downtime per incident | {{ median_downtime_per_incident }} h |
| Average cost per downtime hour | {{ avg_cost_per_downtime_hour }} EUR/h |

**Répartition par sévérité :** {{ n_minor }} mineure · {{ n_moderate }} modérée · {{ n_severe }} sévère

**Most costly site:** {{ top_site_by_cost }} — **most costly equipment:** {{ top_equipment_by_cost }}

{{ figure_plot_yearly_incidents }}
*Annual Incident Trends and Estimated Total Costs.*

{{ figure_plot_yearly_variation }}

*Year-over-Year Change in Incident Costs and Downtime.*

## 2. Analyse des coûts

{{ methodology }}

### 2.1 Coût par site

{{ figure_plot_total_cost_by_site }}

*Coût total estimé (barres rouges) et nombre d'incidents (courbe bleue) par site.*

{{ interpretation_plot_total_cost_by_site }}

### 2.2 Distribution du coût par équipement

{{ figure_plot_cost_distribution_per_equipment_by_site }}

*Distribution du coût total estimé par équipement, groupée par site.*

### 2.3 Top 3 des équipements les plus coûteux du site le plus impacté

{{ figure_plot_daily_cost_top_equipment_at_top_site }}

*Coût estimé quotidien des 3 équipements les plus coûteux du site dont le coût total estimé est le plus élevé.*

## 3. Analyse temporelle et par sévérité

### 3.1 Nombre d'incidents et coût par mois

{{ figure_plot_monthly_incident_count }}

*Nombre d'incidents (barres bleues) et coût total estimé (courbe rouge) par mois sur la période.*

{{ interpretation_plot_monthly_incident_count }}

### 3.2 Incidents et coût par sévérité

{{ figure_plot_incident_count_by_severity }}

*Nombre d'incidents (barres bleues) et coût total estimé (courbe rouge) par niveau de sévérité.*

{{ interpretation_plot_incident_count_by_severity }}

### 3.3 Conditions météorologiques

{{ figure_plot_total_cost_by_weather_condition }}

*Coût total estimé (barres rouges) et nombre d'incidents (courbe bleue) par condition météorologique.*

{{ interpretation_plot_total_cost_by_weather_condition }}

## 4. Clusters thématiques

{{ n_clusters }} clusters d'incidents ont été identifiés à partir des descriptions des rapports.

{{ top_clusters_table }}

### 4.1 Fréquence et coût par cluster

{{ figure_plot_cluster_frequency_cost }}

*Nombre d'incidents (barres bleues) et coût total estimé (courbe rouge) par cluster thématique.*

{{ interpretation_plot_cluster_frequency_cost }}

{{ cluster_sections }}

## 5. Recommandations

{{ recommendations }}

## 6. Synthesis

{{ synthesis }}

