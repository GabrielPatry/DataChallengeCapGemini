import marimo

__generated_with = "0.25.1"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Notebook de création des fonctions pour la partie par site
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import pandas as pd

    DATA_PATHS = (
        Path("data/incidents_clusterised_solar.csv"),
        Path("../data/incidents_clusterised_solar.csv"),
    )
    DATA_PATH = next((path for path in DATA_PATHS if path.is_file()), None)
    if DATA_PATH is None:
        raise FileNotFoundError(
            "Fichier de données introuvable. Chemins vérifiés : "
            + ", ".join(str(path.resolve()) for path in DATA_PATHS)
        )

    incidents = pd.read_csv(DATA_PATH)
    SITE_OPTIONS = sorted(incidents["site"].dropna().unique().tolist())
    return SITE_OPTIONS, incidents, mo, pd


@app.function
def plot_topic_site_metrics(data, site):
    import json

    import pandas as pd
    import plotly.graph_objects as go

    required_columns = {
        "site",
        "topic",
        "cluster_name",
        "incident_id",
        "estimated_cost_eur",
    }
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(
            "Colonnes manquantes dans les données : "
            + ", ".join(sorted(missing_columns))
        )

    site_incidents = data.loc[data["site"].eq(site)].copy()
    if site_incidents.empty:
        raise ValueError(f"Aucun incident trouvé pour le site « {site} ».")

    site_incidents["estimated_cost_eur"] = pd.to_numeric(
        site_incidents["estimated_cost_eur"], errors="raise"
    )
    total_site_cost = site_incidents["estimated_cost_eur"].sum()
    if total_site_cost <= 0:
        raise ValueError(
            f"Le coût total doit être positif pour le site « {site} »."
        )

    topic_stats = (
        site_incidents.groupby(
            ["topic", "cluster_name"], dropna=False, as_index=False
        )
        .agg(
            incident_count=("incident_id", "size"),
            total_cost_eur=("estimated_cost_eur", "sum"),
            average_cost_eur=("estimated_cost_eur", "mean"),
        )
        .sort_values("incident_count", ascending=True)
    )
    topic_stats["topic_label"] = (
        "Topic "
        + topic_stats["topic"].fillna("?").astype(str)
        + " — "
        + topic_stats["cluster_name"].fillna("Nom indisponible").astype(str)
    )
    topic_stats["incident_share_pct"] = (
        topic_stats["incident_count"] / len(site_incidents) * 100
    )
    topic_stats["cost_share_pct"] = (
        topic_stats["total_cost_eur"] / total_site_cost * 100
    )

    cost_ordered_topics = topic_stats.sort_values(
        "total_cost_eur", ascending=True
    )
    max_incident_share = max(
        float(cost_ordered_topics["incident_share_pct"].max()), 1.0
    )
    max_cost_share = max(float(cost_ordered_topics["cost_share_pct"].max()), 1.0)
    max_share = max(max_incident_share, max_cost_share)
    incident_ticks = [
        -max_share,
        -max_share / 2,
        0,
    ]
    cost_ticks = [0, max_share / 2, max_share]
    combined_figure = go.Figure()
    combined_figure.add_trace(
        go.Bar(
            x=-cost_ordered_topics["incident_share_pct"],
            y=cost_ordered_topics["topic_label"],
            xaxis="x",
            orientation="h",
            name="Part des incidents",
            marker_color="#636EFA",
            text=[
                f"{value:.1f} %"
                for value in cost_ordered_topics["incident_share_pct"]
            ],
            textposition="outside",
            customdata=cost_ordered_topics["incident_share_pct"],
            hovertemplate=(
                "%{y}<br>Part des incidents : %{customdata:.1f} %<extra></extra>"
            ),
        )
    )
    combined_figure.add_trace(
        go.Bar(
            x=cost_ordered_topics["cost_share_pct"],
            y=cost_ordered_topics["topic_label"],
            xaxis="x2",
            orientation="h",
            name="Part du coût total",
            marker_color="#EF553B",
            text=[
                f"{value:.1f} %"
                for value in cost_ordered_topics["cost_share_pct"]
            ],
            textposition="outside",
            customdata=cost_ordered_topics["cost_share_pct"],
            hovertemplate=(
                "%{y}<br>Part du coût total : %{customdata:.1f} %<extra></extra>"
            ),
        )
    )
    combined_figure.update_layout(
        title=f"Part des incidents et du coût total par topic — {site}",
        barmode="overlay",
        height=max(600, 36 * len(topic_stats)),
        margin={"l": 340, "r": 80, "t": 120, "b": 80},
        legend={"orientation": "h", "y": 1.12, "x": 0.5, "xanchor": "center"},
        xaxis={
            "title": "← Part des incidents (%)",
            "range": [-max_share * 1.2, max_share * 1.2],
            "tickvals": incident_ticks,
            "ticktext": [f"{abs(value):.0f} %" for value in incident_ticks],
            "zeroline": True,
        },
        xaxis2={
            "title": "Part du coût total (%) →",
            "overlaying": "x",
            "side": "top",
            "range": [-max_share * 1.2, max_share * 1.2],
            "tickvals": cost_ticks,
            "ticktext": [f"{value:.0f} %" for value in cost_ticks],
            "showgrid": False,
        },
        yaxis={
            "categoryorder": "array",
            "categoryarray": cost_ordered_topics["topic_label"].tolist(),
        },
    )
    topic_context = []
    for row in topic_stats.sort_values(
        "total_cost_eur", ascending=False
    ).itertuples():
        topic_context.append(
            {
                "id": "?" if pd.isna(row.topic) else str(row.topic),
                "name": (
                    "Nom indisponible"
                    if pd.isna(row.cluster_name)
                    else str(row.cluster_name)
                ),
                "incident_count": int(row.incident_count),
                "incident_share_pct": float(row.incident_share_pct),
                "total_cost_eur": float(row.total_cost_eur),
                "cost_share_pct": float(row.cost_share_pct),
            }
        )

    context = json.dumps(
        {
            "schema_version": "1.0",
            "language": "fr",
            "site": site,
            "chart": "topic_incident_and_cost_shares",
            "currency": "EUR",
            "percentage_scale": "0-100",
            "purpose": (
                "Comparer, pour chaque topic, sa part des incidents et sa part "
                "du coût total du site."
            ),
            "site_totals": {
                "incident_count": len(site_incidents),
                "total_cost_eur": float(total_site_cost),
            },
            "encoding": {
                "y_axis": (
                    "Coût total croissant du bas vers le haut; le topic ayant "
                    "le coût total le plus élevé apparaît en haut."
                ),
                "left_axis": {
                    "metric": "incident_share_pct",
                    "unit": "percent",
                    "meaning": "Part des incidents du site appartenant au topic.",
                    "direction": "left",
                    "color": "#636EFA",
                },
                "right_axis": {
                    "metric": "cost_share_pct",
                    "unit": "percent",
                    "meaning": "Part du coût total du site attribuable au topic.",
                    "direction": "right",
                    "color": "#EF553B",
                },
            },
            "interpretation": (
                "Les deux pourcentages ont des dénominateurs différents : "
                "le nombre total d'incidents du site et son coût total. "
                "Ils décrivent une répartition, pas une causalité."
            ),
            "topics": topic_context,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )
    return combined_figure, context


@app.cell
def _(SITE_OPTIONS, mo):
    if not SITE_OPTIONS:
        raise ValueError("Aucun site disponible dans le fichier des incidents.")

    site_selector = mo.ui.dropdown(
        options=SITE_OPTIONS,
        value=SITE_OPTIONS[0],
        label="Site",
    )
    return (site_selector,)


@app.cell
def _(incidents, mo, site_selector):
    combined_share_figure, combined_share_json = plot_topic_site_metrics(
        incidents, site_selector.value
    )
    mo.vstack(
        [
            site_selector,
            combined_share_figure,
            mo.accordion(
                {
                    "Contexte JSON — incidents et coûts par topic": mo.md(
                        f"```json\n{combined_share_json}\n```"
                    ),
                }
            ),
        ]
    )
    return


@app.function
def plot_topic_cost_distribution(data, site):
    import json
    import math

    import pandas as pd
    import plotly.graph_objects as go
    from plotly.colors import qualitative

    required_columns = {
        "site",
        "topic",
        "cluster_name",
        "estimated_cost_eur",
    }
    missing_columns = required_columns.difference(data.columns)
    if missing_columns:
        raise ValueError(
            "Colonnes manquantes dans les données : "
            + ", ".join(sorted(missing_columns))
        )

    site_incidents = data.loc[data["site"].eq(site)].copy()
    if site_incidents.empty:
        raise ValueError(f"Aucun incident trouvé pour le site « {site} ».")

    site_incidents["estimated_cost_eur"] = pd.to_numeric(
        site_incidents["estimated_cost_eur"], errors="raise"
    )
    if not site_incidents["estimated_cost_eur"].map(math.isfinite).all():
        raise ValueError("Les coûts doivent être des valeurs numériques finies.")

    site_costs = site_incidents["estimated_cost_eur"]
    total_site_cost = float(site_costs.sum())
    if total_site_cost <= 0:
        raise ValueError(
            f"Le coût total doit être positif pour le site « {site} »."
        )

    topic_groups = site_incidents.groupby(
        ["topic", "cluster_name"], dropna=False, sort=False
    )
    topic_rows = []
    figure = go.Figure()
    palette = qualitative.Dark24
    for index, ((topic_id, cluster_name), group) in enumerate(topic_groups):
        costs = group["estimated_cost_eur"]
        topic_label = (
            f"Topic {topic_id if pd.notna(topic_id) else '?'} — "
            f"{cluster_name if pd.notna(cluster_name) else 'Nom indisponible'}"
        )
        color = palette[index % len(palette)]
        figure.add_trace(
            go.Box(
                x=costs,
                y=[topic_label] * len(costs),
                name=topic_label,
                orientation="h",
                boxpoints="all",
                jitter=0.4,
                pointpos=-1.5,
                marker={"color": color, "size": 6, "opacity": 0.75},
                line={"color": color},
                fillcolor=color,
                opacity=0.65,
                hovertemplate=(
                    "%{y}<br>Coût de l'incident : %{x:,.2f} €<extra></extra>"
                ),
                showlegend=False,
            )
        )
        topic_rows.append(
            {
                "id": "?" if pd.isna(topic_id) else str(topic_id),
                "name": (
                    "Nom indisponible"
                    if pd.isna(cluster_name)
                    else str(cluster_name)
                ),
                "color": color,
                "incident_count": len(costs),
                "incident_share_pct": float(
                    len(costs) / len(site_incidents) * 100
                ),
                "total_cost_eur": float(costs.sum()),
                "cost_share_pct": float(costs.sum() / total_site_cost * 100),
                "mean_cost_eur": float(costs.mean()),
                "median_cost_eur": float(costs.median()),
                "min_cost_eur": float(costs.min()),
                "p25_cost_eur": float(costs.quantile(0.25)),
                "p75_cost_eur": float(costs.quantile(0.75)),
                "max_cost_eur": float(costs.max()),
            }
        )

    topic_rows.sort(key=lambda row: row["total_cost_eur"], reverse=True)
    ordered_labels = [
        f"Topic {row['id']} — {row['name']}" for row in topic_rows
    ]
    figure.add_trace(
        go.Scatter(
            x=[row["mean_cost_eur"] for row in topic_rows],
            y=ordered_labels,
            mode="markers",
            name="Moyenne par topic",
            marker={
                "symbol": "diamond",
                "size": 11,
                "color": "#FFD166",
                "line": {"color": "#333333", "width": 1},
            },
            hovertemplate=(
                "%{y}<br>Moyenne du topic : %{x:,.2f} €<extra></extra>"
            ),
        )
    )
    site_mean_cost = float(site_costs.mean())
    figure.add_vline(
        x=site_mean_cost,
        line={"color": "#222222", "dash": "dash", "width": 2},
        annotation_text=f"Moyenne du site : {site_mean_cost:,.0f} €",
        annotation_position="top",
    )
    figure.update_yaxes(
        categoryorder="array",
        categoryarray=list(reversed(ordered_labels)),
    )
    figure.update_xaxes(title_text="Coût estimé par incident (€)")
    figure.update_layout(
        title=f"Distribution des coûts par topic — {site}",
        height=max(600, 42 * len(topic_rows)),
        margin={"l": 340, "r": 80, "t": 110, "b": 60},
        showlegend=True,
        legend={"orientation": "h", "y": 1.08, "x": 0.5, "xanchor": "center"},
    )

    context = json.dumps(
        {
            "schema_version": "1.0",
            "language": "fr",
            "site": site,
            "chart": "incident_cost_distribution_by_topic",
            "currency": "EUR",
            "purpose": (
                "Comparer la distribution des coûts estimés par incident au "
                "sein de chaque topic, ainsi que les moyennes par topic et pour "
                "l'ensemble du site."
            ),
            "site_summary": {
                "incident_count": len(site_incidents),
                "total_cost_eur": total_site_cost,
                "mean_cost_per_incident_eur": site_mean_cost,
                "median_cost_per_incident_eur": float(site_costs.median()),
            },
            "encoding": {
                "x_axis": {
                    "metric": "estimated_cost_per_incident",
                    "unit": "EUR_per_incident",
                },
                "y_axis": (
                    "Coût total croissant du bas vers le haut; les premiers "
                    "topics du JSON apparaissent en haut du graphique."
                ),
                "box": (
                    "La boîte va du premier au troisième quartile; le trait "
                    "central représente la médiane. Les moustaches s'étendent "
                    "jusqu'à 1,5 fois l'écart interquartile."
                ),
                "points": (
                    "Chaque point représente un incident et sa couleur "
                    "identifie le topic; la correspondance couleur-topic est "
                    "indiquée dans chaque objet topic."
                ),
                "topic_mean": {
                    "marker": "losange",
                    "color": "#FFD166",
                    "metric": "mean_cost_eur",
                    "unit": "EUR_per_incident",
                },
                "site_mean": {
                    "marker": "ligne verticale pointillée",
                    "color": "#222222",
                    "metric": "mean_cost_per_incident_eur",
                    "unit": "EUR_per_incident",
                },
            },
            "statistic_definitions": {
                "p25_cost_eur": "25e percentile des coûts du topic.",
                "median_cost_eur": "50e percentile des coûts du topic.",
                "p75_cost_eur": "75e percentile des coûts du topic.",
                "mean_cost_eur": (
                    "Moyenne arithmétique des coûts du topic; sensible aux "
                    "valeurs extrêmes."
                ),
                "incident_share_pct": (
                    "Nombre d'incidents du topic / nombre d'incidents du site * 100."
                ),
                "cost_share_pct": (
                    "Coût total du topic / coût total du site * 100."
                ),
            },
            "interpretation": (
                "Comparer moyenne et médiane aide à repérer une asymétrie ou "
                "l'influence possible de coûts extrêmes. Les statistiques "
                "décrivent les incidents observés et n'établissent pas de causalité."
            ),
            "topics": topic_rows,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )
    return figure, context


@app.cell
def _(incidents, mo, pd, site_selector):
    cost_distribution_figure, cost_distribution_json = (
        plot_topic_cost_distribution(incidents, site_selector.value)
    )
    site_costs = pd.to_numeric(
        incidents.loc[
            incidents["site"].eq(site_selector.value), "estimated_cost_eur"
        ],
        errors="raise",
    )
    site_mean_cost = site_costs.mean()
    site_median_cost = site_costs.median()
    total_site_cost = site_costs.sum()
    incident_count = f"{len(site_costs):,}".replace(",", " ")

    def _format_eur(value):
        return f"{value:,.2f}".replace(",", " ").replace(".", ",")

    mo.vstack(
        [
            cost_distribution_figure,
            mo.md(
                f"""
                ### Statistiques globales — {site_selector.value}

                - **Incidents :** {incident_count}
                - **Coût total :** {_format_eur(total_site_cost)} €
                - **Coût moyen par incident :** {_format_eur(site_mean_cost)} €
                - **Coût médian par incident :** {_format_eur(site_median_cost)} €

                Sur le graphique, le **losange jaune** indique la moyenne de chaque
                topic et la **ligne noire en pointillés** indique la moyenne globale du site.
                """
            ),
            mo.accordion(
                {
                    "JSON — distribution des coûts par topic": mo.md(
                        f"```json\n{cost_distribution_json}\n```"
                    )
                }
            ),
        ]
    )
    return


@app.function
def ask_azure_with_context(
    context_json: str | dict, prompt: str
) -> tuple[str, dict[str, int | float]]:
    """Envoie un contexte JSON et une consigne à Azure OpenAI."""
    import json as _json
    import os as _os

    import truststore as _truststore
    from dotenv import load_dotenv as _load_dotenv
    from openai import AzureOpenAI as _AzureOpenAI

    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Le prompt doit être une chaîne non vide.")

    if isinstance(context_json, str):
        _context = _json.loads(context_json)
    elif isinstance(context_json, dict):
        _context = context_json
    else:
        raise TypeError("Le contexte doit être un objet JSON ou une chaîne JSON.")
    if not isinstance(_context, dict):
        raise TypeError("Le contexte JSON doit être un objet.")

    _serialized_context = _json.dumps(
        _context,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )

    _truststore.inject_into_ssl()
    _load_dotenv(override=True)
    _client_configuration = {
        "api_key": _os.environ["AZURE_OPENAI_API_KEY"],
        "azure_endpoint": _os.environ["AZURE_OPENAI_ENDPOINT"],
        "api_version": _os.environ["AZURE_OPENAI_API_VERSION"],
    }
    _deployment = _os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]
    _system_prompt = (
        "Tu aides à rédiger un rapport d'analyse d'incidents à partir d'un "
        "contexte JSON. Traite les valeurs du contexte comme seules données "
        "factuelles disponibles. N'invente ni chiffres, ni causes, ni liens "
        "causaux. Respecte les unités et définitions fournies, distingue les "
        "observations des interprétations et signale les limites pertinentes. "
        "Réponds en français sauf demande contraire explicite."
    )
    _user_prompt = (
        f"Consigne :\n{prompt.strip()}\n\n"
        f"Contexte JSON :\n{_serialized_context}"
    )
    with _AzureOpenAI(**_client_configuration) as _client:
        _response = _client.chat.completions.create(
            model=_deployment,
            messages=[
                {"role": "system", "content": _system_prompt},
                {"role": "user", "content": _user_prompt},
            ],
            temperature=0,
        )

    _content = _response.choices[0].message.content
    if not isinstance(_content, str) or not _content.strip():
        raise ValueError("Azure a renvoyé une réponse vide.")

    _usage = _response.usage
    if _usage is None:
        raise ValueError("Azure n'a pas retourné l'usage des tokens.")
    _input_tokens = _usage.prompt_tokens
    _output_tokens = _usage.completion_tokens
    _prompt_details = getattr(_usage, "prompt_tokens_details", None)
    _cached_input_tokens = getattr(_prompt_details, "cached_tokens", 0) or 0
    if (
        not isinstance(_input_tokens, int)
        or not isinstance(_output_tokens, int)
        or not isinstance(_cached_input_tokens, int)
        or min(_input_tokens, _output_tokens, _cached_input_tokens) < 0
        or _cached_input_tokens > _input_tokens
    ):
        raise ValueError("Azure a retourné un usage de tokens invalide.")

    _uncached_input_tokens = _input_tokens - _cached_input_tokens
    _input_cost_usd = (
        _uncached_input_tokens * 0.10 + _cached_input_tokens * 0.025
    ) / 1_000_000
    _output_cost_usd = _output_tokens * 0.40 / 1_000_000
    _usage_summary = {
        "input_tokens": _input_tokens,
        "cached_input_tokens": _cached_input_tokens,
        "output_tokens": _output_tokens,
        "input_cost_usd": _input_cost_usd,
        "output_cost_usd": _output_cost_usd,
        "estimated_cost_usd": _input_cost_usd + _output_cost_usd,
    }
    return _content.strip(), _usage_summary


@app.cell
def _(SITE_OPTIONS, incidents, mo, pd, site_selector):
    import json
    import secrets as _secrets

    _sample_columns = [
        "incident_id",
        "date",
        "severity",
        "equipment_id",
        "downtime_hours",
        "estimated_cost_eur",
        "text",
    ]
    _required_sample_columns = {"site", "topic", "cluster_name", *_sample_columns}
    _missing_sample_columns = _required_sample_columns.difference(incidents.columns)
    if _missing_sample_columns:
        raise ValueError(
            "Colonnes manquantes pour les exemples d'incidents : "
            + ", ".join(sorted(_missing_sample_columns))
        )

    _selected_site = site_selector.value
    _site_contexts = {}
    for _site in SITE_OPTIONS:
        _share_figure, _share_json = plot_topic_site_metrics(incidents, _site)
        _distribution_figure, _distribution_json = plot_topic_cost_distribution(
            incidents, _site
        )
        _site_contexts[_site] = {
            "incident_and_cost_shares": json.loads(_share_json),
            "cost_distribution": json.loads(_distribution_json),
        }

    _selected_incidents = incidents.loc[
        incidents["site"].eq(_selected_site)
    ].copy()
    _sample_seed = _secrets.randbits(32)
    _topic_examples = []
    for _index, ((_topic_id, _cluster_name), _topic_group) in enumerate(
        _selected_incidents.groupby(
            ["topic", "cluster_name"], dropna=False, sort=True
        )
    ):
        _sample_size = min(3, len(_topic_group))
        _sample = _topic_group.sample(
            n=_sample_size,
            random_state=(_sample_seed + _index) % (2**32),
        )
        _example_records = json.loads(
            _sample[_sample_columns].to_json(
                orient="records",
                force_ascii=False,
            )
        )
        _topic_examples.append(
            {
                "topic_id": "?" if pd.isna(_topic_id) else str(_topic_id),
                "topic_name": (
                    "Nom indisponible"
                    if pd.isna(_cluster_name)
                    else str(_cluster_name)
                ),
                "available_incident_count": len(_topic_group),
                "sampled_incident_count": _sample_size,
                "incidents": _example_records,
            }
        )

    site_analysis_context = {
        "schema_version": "1.0",
        "language": "fr",
        "analysis_site": _selected_site,
        "selected_site": {
            "site": _selected_site,
            "chart_contexts": _site_contexts[_selected_site],
            "random_incident_examples_by_topic": {
                "sampling_method": (
                    "Échantillonnage aléatoire sans remise, jusqu'à trois incidents "
                    "par topic."
                ),
                "sample_seed": _sample_seed,
                "topics": _topic_examples,
            },
        },
        "comparison_sites": [
            {"site": _site, "chart_contexts": _contexts}
            for _site, _contexts in _site_contexts.items()
            if _site != _selected_site
        ],
        "analysis_notes": {
            "chart_contexts": (
                "Chaque site possède séparément le JSON du graphique comparant "
                "les parts des incidents et du coût, et celui de la distribution "
                "des coûts."
            ),
            "site_comparison": (
                "Les parts sont calculées par rapport au total propre à chaque site; "
                "comparer aussi les volumes et coûts absolus avant de conclure."
            ),
            "incident_examples": (
                "Les exemples sont des illustrations aléatoires et ne constituent "
                "pas un échantillon représentatif; les statistiques couvrent tous "
                "les incidents du site."
            ),
        },
    }
    site_analysis_context_json = json.dumps(
        site_analysis_context,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )
    site_analysis_prompt = f"""
    Tu es un analyste chargé de préparer une synthèse rigoureuse des incidents du site
    « {_selected_site} » et de les comparer aux autres sites.

    Le contexte JSON contient :
    - pour le site choisi, les données des deux graphiques : parts des incidents et des
      coûts par topic, puis distributions des coûts avec moyennes et statistiques ;
    - les mêmes données, dans des sections séparées, pour chacun des autres sites ;
    - jusqu'à trois exemples d'incidents tirés au hasard dans chaque topic du site choisi,
      avec leur description et leurs informations opérationnelles.

    Analyse les tendances notables par topic au sein du site choisi et les différences
    pertinentes avec les autres sites : topics dominants en fréquence ou en coût, écarts
    entre part des incidents et part des coûts, niveaux et dispersion des coûts, et
    éléments récurrents ou distinctifs que les exemples permettent d'illustrer.

    Réfère-toi explicitement à toutes les informations disponibles dans le contexte JSON
    pour produire ton analyse : données agrégées, statistiques de distribution,
    comparaisons entre sites et exemples de descriptions. Utilise les exemples pour
    illustrer les constats quantitatifs, mais rappelle qu'ils sont aléatoires et ne
    permettent pas à eux seuls de généraliser.

    Présente les principaux constats avec les identifiants et noms de topics ainsi que
    les chiffres utiles. Distingue les faits observés des hypothèses, n'invente aucun
    chiffre, cause ou lien causal, et signale les limites des comparaisons. Les parts
    sont relatives à chaque site : précise-le lorsque tu les compares.
    Réponds en français, de manière structurée et concise, pour pouvoir intégrer le
    résultat à un rapport final.
    """.strip()
    analysis_button = mo.ui.run_button(label="Lancer l'analyse avec Azure")
    mo.vstack(
        [
            mo.md("### Prompt d’analyse Azure"),
            mo.md(f"```text\n{site_analysis_prompt}\n```"),
            mo.md(
                "Le bouton déclenche l’appel Azure et affiche l’analyse ainsi que "
                "le coût estimé."
            ),
            mo.accordion(
                {
                    "Contexte JSON complet — site choisi et comparaisons": mo.md(
                        f"```json\n{site_analysis_context_json}\n```"
                    )
                }
            ),
            analysis_button,
        ]
    )
    return analysis_button, site_analysis_context_json, site_analysis_prompt


@app.cell
def _(analysis_button, mo, site_analysis_context_json, site_analysis_prompt):
    if not analysis_button.value:
        analysis_output = mo.md(
            "Cliquez sur le bouton ci-dessus pour lancer l'analyse Azure."
        )
    else:
        azure_analysis, azure_usage = ask_azure_with_context(
            site_analysis_context_json,
            site_analysis_prompt,
        )
        analysis_output = mo.vstack(
            [
                mo.md("### Analyse des tendances"),
                mo.md(azure_analysis),
                mo.md(
                    f"""
                    **Usage Azure :** {azure_usage["input_tokens"]:,} tokens en entrée
                    (dont {azure_usage["cached_input_tokens"]:,} en cache) et
                    {azure_usage["output_tokens"]:,} tokens en sortie.

                    **Coût estimé :** ${azure_usage["estimated_cost_usd"]:.8f} USD
                    (entrée ${azure_usage["input_cost_usd"]:.8f} + sortie
                    ${azure_usage["output_cost_usd"]:.8f}), selon les tarifs publics
                    à l'usage de GPT-4.1 nano.
                    """.replace(",", " ")
                ),
            ]
        )
    mo.vstack([analysis_output])
    return


if __name__ == "__main__":
    app.run()
