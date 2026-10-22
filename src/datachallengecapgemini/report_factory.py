"""Report generation step — fill markdown report templates for solar and wind.

The pipeline ends with two markdown reports, one per asset type. Each report
is produced by filling a template stored in the ``templates/`` folder with:

- **Computed statistics** read from the clusterised incidents CSV (number of
  incidents, sites, total cost, downtime, severity breakdown, top clusters…).
- **Figures** — every ``{{ figure_<plot_name> }}`` placeholder is replaced by
  a markdown image pointing at ``data/plots/<label>/png/<plot_name>.png``
  (relative path, so the report stays portable inside the repository). If the
  PNG is missing but the interactive HTML version exists, a link to the HTML
  page is emitted instead; a figure missing from both folders is replaced by
  a placeholder note and a warning is printed.
- **Figure descriptions** — JSON descriptions from the ``json`` subfolder are
  passed to the prose agents as additional context.
- **Prose** — synopsis, methodology, per-cluster descriptions, recommendations
  and conclusion. These are generated in French by the LLM agents of
  :class:`ReportFactory` (Azure OpenAI, gpt-4.1-nano): each section has its
  own prompt template, the generated text is stored in a
  :class:`ReportProse` object so sections can depend on each other, and the
  total token usage is printed at the end of the step.

Placeholders use the ``{{ variable_name }}`` syntax. Filling is done with a
simple regex substitution (no templating dependency); unknown placeholders
raise an error so typos in templates are caught immediately.

Filled reports are written to ``filled_templates/solar/report.md`` and
``filled_templates/wind/report.md``.

Available as the last step of the top-level ``datachallengecapgemini`` entry
point:

- ``uv run datachallengecapgemini`` — preprocessing (optional) + plotting + reporting
"""

import argparse
import json
import os
import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, ClassVar, TypedDict

import pandas as pd
from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from langgraph.graph import END, START, StateGraph

# Project root: src/datachallengecapgemini/report_factory.py -> 3 levels up
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Placeholder syntax: {{ variable_name }}
PLACEHOLDER_PATTERN = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")

# Prefix of the placeholders that embed a figure: {{ figure_<plot_name> }}
FIGURE_PLACEHOLDER_PREFIX = "figure_"

# Cluster code used for the unclassified / noise incidents
NOISE_CLUSTER_CODE = "C_NOISE"

# Number of clusters detailed in the "cluster_sections" variable
N_DETAILED_CLUSTERS = 5

# Severity levels in increasing order of seriousness
SEVERITY_LEVELS: tuple[str, ...] = ("mineure", "modérée", "sévère")


# ---------------------------------------------------------------------------
# LLM agents — generate the prose sections of the reports
# ---------------------------------------------------------------------------


class ReportState(TypedDict, total=False):
    """State shared by the nodes of the recommendations graph.

    The context fields (``label``, ``statistics``, ``clusters``) are filled
    by the factory before invocation; each node then writes its own output
    field (``cost_drivers``, ``draft_recommendations``, ``recommendations``).
    """

    # Context provided by the factory
    label: str
    statistics: str
    clusters: str
    plot_descriptions: str
    # Outputs of the graph nodes
    cost_drivers: str
    draft_recommendations: str
    recommendations: str


def _new_state_graph() -> StateGraph[ReportState]:  # ty: ignore[invalid-type-arguments]
    """Build an empty ``StateGraph`` over :class:`ReportState`.

    The ``ty: ignore`` comments work around a ``ty`` limitation: it cannot
    match a TypedDict against langgraph's ``StateLike`` protocol bound
    (langgraph's own ``MessagesState`` fails the same check).
    """
    return StateGraph(ReportState)  # ty: ignore[invalid-argument-type]


class TokenUsageCallback(BaseCallbackHandler):
    """Accumulates the token usage of every LLM call made by a factory."""

    def __init__(self) -> None:
        super().__init__()
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.n_calls = 0

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        self.n_calls += 1
        usage = (response.llm_output or {}).get("token_usage") or {}
        self.prompt_tokens += int(usage.get("prompt_tokens") or 0)
        self.completion_tokens += int(usage.get("completion_tokens") or 0)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    def summary(self) -> str:
        return (
            f"{self.total_tokens:,} tokens "
            f"({self.prompt_tokens:,} prompt + {self.completion_tokens:,} "
            f"completion over {self.n_calls} LLM call(s))"
        )


SYNOPSIS_SYSTEM_PROMPT = (
    "Tu es le rédacteur technique d'un rapport d'analyse d'incidents sur "
    "des actifs industriels. Rédige un synopsis exécutif concis (un "
    "paragraphe de 80 à 120 mots) pour le parc {label} : les thèmes "
    "d'incidents dominants et leur poids dans le coût estimé et le temps "
    "d'arrêt. Utilise uniquement les statistiques, le résumé des clusters et "
    "les descriptions des figures "
    "fournis, n'invente aucun chiffre. Rédige en français, avec un ton de "
    "rapport professionnel."
)

METHODOLOGY_SYSTEM_PROMPT = (
    "Tu es le rédacteur technique d'un rapport d'analyse d'incidents sur "
    "des actifs industriels. Décris en un paragraphe (80 à 120 mots) la "
    "méthodologie utilisée pour analyser les incidents du parc {label} : "
    "consolidation des rapports d'incident en un jeu de données unique, "
    "plongement lexical (embedding) et clustering thématique des "
    "descriptions d'incidents, recoupement avec les métadonnées structurées "
    "(site, équipement, sévérité, temps d'arrêt, coût estimé, conditions "
    "météorologiques). Mentionne que les figures sont générées à partir du "
    "jeu de données clusterisé, que les coûts sont exprimés en euros et les "
    "temps d'arrêt en heures. Rédige en français, avec un ton de rapport "
    "professionnel."
)

CLUSTER_DESCRIPTION_SYSTEM_PROMPT = (
    "Tu es ingénieur fiabilité et tu rédiges un rapport d'analyse "
    "d'incidents sur des actifs industriels. Décris le cluster d'incidents "
    "'{cluster_name}' ({cluster_code}) du parc {label} en un paragraphe (60 "
    "à 100 mots) : la signature de défaillance commune, le site le plus "
    "touché, la sévérité dominante, l'exposition en coût et en temps "
    "d'arrêt, et une hypothèse de cause racine. Utilise uniquement les "
    "statistiques du cluster et les descriptions des figures fournies, "
    "n'invente aucun chiffre. Rédige en "
    "français, avec un ton de rapport professionnel."
)

COST_DRIVERS_SYSTEM_PROMPT = (
    "Tu es stratège de maintenance pour un parc d'actifs {label}. À partir "
    "des statistiques, du résumé des clusters et des descriptions des figures "
    "fournis, liste les 3 à 5 "
    "principaux facteurs de coût estimé et de temps d'arrêt, un par ligne, "
    "chacun justifié en une phrase par les données. N'invente aucun "
    "chiffre. Rédige en français."
)

DRAFT_RECOMMENDATIONS_SYSTEM_PROMPT = (
    "Tu es stratège de maintenance pour un parc d'actifs {label}. Pour "
    "chaque facteur de coût et de temps d'arrêt listé ci-dessous, rédige "
    "une recommandation concrète et actionnable. Réponds avec une puce "
    "markdown par facteur, à l'impératif, sans introduction. Rédige en "
    "français."
)

PRIORITISE_RECOMMENDATIONS_SYSTEM_PROMPT = (
    "Tu es directeur de maintenance et tu rédiges la section "
    "recommandations d'un rapport d'analyse d'incidents sur des actifs "
    "industriels pour le parc {label}. Réécris les recommandations "
    "provisoires ci-dessous comme la liste à puces markdown finale et "
    "priorisée du rapport : les plus impactantes en premier, au plus 6 "
    "puces, chacune commençant par '- '. Ne garde que des actions appuyées "
    "par les recommandations provisoires et les statistiques, n'invente pas "
    "de nouvelles actions. Rédige en français."
)

CONCLUSION_SYSTEM_PROMPT = (
    "Tu es le rédacteur technique d'un rapport d'analyse d'incidents sur "
    "des actifs industriels. Rédige la conclusion du rapport du parc "
    "{label} en un paragraphe (60 à 100 mots) : résume les principaux "
    "constats et renvoie vers les recommandations. Utilise le synopsis, "
    "les statistiques, les descriptions des figures et les recommandations "
    "fournis, n'invente aucun "
    "chiffre. Rédige en français, avec un ton de rapport professionnel."
)

SYNTHESE_SYSTEM_PROMPT = """
Tu es un expert en analyse de données et en fiabilité industrielle.

Tu reçois un rapport complet d'analyse des incidents d'un parc
d'actifs industriels, déjà rédigé.

Ta mission est de produire une synthèse générale du rapport en français.

La synthèse doit :
- Identifier les 3 à 5 enseignements les plus importants du rapport.
- Faire ressortir les principaux facteurs de coût et de temps d'arrêt.
- Mettre en évidence les tendances et les problèmes récurrents.
- Hiérarchiser les enjeux et les priorités d'action.
- Relier les constats aux recommandations du rapport.
- Mentionner les limites importantes de l'analyse, si elles sont
  explicitement documentées dans le rapport.

Contraintes :
- Lis le rapport dans son ensemble avant de rédiger.
- Ne répète pas simplement la conclusion existante.
- N'invente aucun chiffre, fait, cause racine ou recommandation.
- Distingue les constats établis des hypothèses.
- Signale les éventuelles contradictions ou limites du rapport.
- Évite les répétitions et les détails secondaires.
- Rédige une synthèse autonome, claire et professionnelle,
  de 200 à 300 mots, avec des paragraphes et des puces Markdown
  si nécessaire.
"""


@dataclass
class ReportProse:
    """Stores the prose sections generated for one report.

    Every section is ``None`` until it has been generated; the ``write_*``
    methods of :class:`ReportFactory` fill the matching attribute, so a
    section can reuse the sections it depends on (e.g. the conclusion
    reuses the synopsis and the recommendations).
    """

    synopsis: str | None = None
    methodology: str | None = None
    cluster_descriptions: list[str] | None = None
    recommendations: str | None = None
    conclusion: str | None = None


class ReportFactory:
    """Generates the prose sections of an incident report with LLM agents.

    Mirrors :class:`~datachallengecapgemini.plot_factory.PlotFactory`: the
    clusterised incidents dataframe is the main attribute (``df``), completed
    by the asset ``label``. The chat model (Azure OpenAI, gpt-4.1-nano
    deployment) is the ``llm`` attribute, and the context shared by the
    agents (``statistics``, ``clusters``, ``cluster_table`` and the JSON
    ``plot_descriptions``) is precomputed at construction.

    Private ``_*_prompt`` methods only build :class:`ChatPromptTemplate`
    instances. The public ``write_*`` methods handle the execution — a
    simple prompt chain for most sections, a small langgraph ``StateGraph``
    for the multi-step recommendations section — and store the generated
    text in the :class:`ReportProse` object passed as argument, so that
    dependent sections reuse already-generated text when available.
    :meth:`generate_prose` orchestrates the sections requested by the user.

    The token usage of every LLM call is accumulated in ``token_usage`` and
    printed with :meth:`print_token_usage`.
    """

    # Environment variables required to build the default Azure OpenAI LLM
    AZURE_ENV_VARS: ClassVar[tuple[str, ...]] = (
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_CHAT_DEPLOYMENT",
    )

    # Maximum number of clusters rendered in the shared cluster summary
    N_SUMMARISED_CLUSTERS: ClassVar[int] = 10

    # Default prose paragraphs generated by generate_prose, in order
    DEFAULT_PARAGRAPHS: ClassVar[tuple[str, ...]] = (
        "synopsis",
        "methodology",
        "cluster_descriptions",
        "recommendations",
        "conclusion",
    )

    def __init__(
        self,
        df: pd.DataFrame,
        label: str,
        llm: BaseChatModel | None = None,
        plot_descriptions: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.df = df
        self.label = label
        self.plot_descriptions = plot_descriptions or {}
        self.plot_descriptions_context = json.dumps(
            self.plot_descriptions, ensure_ascii=False, indent=2
        )
        self.token_usage = TokenUsageCallback()
        self.llm = llm if llm is not None else self._default_llm()
        # Context elements shared by every agent
        self.statistics = self._render_statistics()
        self.cluster_table = self._compute_cluster_table()
        self.clusters = self._render_clusters()

    @classmethod
    def _default_llm(cls) -> BaseChatModel:
        """Build the default LLM: Azure OpenAI, gpt-4.1-nano chat deployment."""
        load_dotenv()
        missing = [name for name in cls.AZURE_ENV_VARS if not os.environ.get(name)]
        if missing:
            raise RuntimeError(
                f"Missing Azure OpenAI environment variable(s): "
                f"{', '.join(missing)}. Set them in your environment or in "
                "the .env file at the project root."
            )
        return AzureChatOpenAI(
            azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.environ["AZURE_OPENAI_API_VERSION"],
            temperature=0.2,
        )

    # ------------------------------------------------------------------
    # Context rendering — shared by every agent
    # ------------------------------------------------------------------

    def _render_statistics(self) -> str:
        """Render the key fleet statistics as a text block for the agents."""
        df = self.df
        dates = pd.to_datetime(df["date"])
        severity_counts = df["severity"].value_counts()
        total_cost = df["estimated_cost_eur"].sum()
        total_downtime = df["downtime_hours"].sum()
        top_site = df.groupby("site")["estimated_cost_eur"].sum().idxmax()
        top_equipment = df.groupby("equipment_id")["estimated_cost_eur"].sum().idxmax()
        severity_breakdown = ", ".join(
            f"{level}: {int(severity_counts.get(level, 0))}"
            for level in SEVERITY_LEVELS
        )
        lines = [
            f"- Incidents analysés : {len(df)}",
            f"- Sites couverts : {df['site'].nunique()}",
            f"- Équipements surveillés : {df['equipment_id'].nunique()}",
            (
                f"- Période : {dates.min().date().isoformat()} "
                f"à {dates.max().date().isoformat()}"
            ),
            f"- Coût total estimé : {total_cost:,.2f} EUR",
            f"- Temps d'arrêt total : {total_downtime:,.1f} h",
            f"- Coût moyen par incident : {total_cost / len(df):,.2f} EUR",
            f"- Répartition par sévérité : {severity_breakdown}",
            f"- Site le plus coûteux : {top_site}",
            f"- Équipement le plus coûteux : {top_equipment}",
        ]
        return "\n".join(lines)

    def _compute_cluster_table(self) -> pd.DataFrame:
        """Per-cluster aggregates (count, cost, downtime), largest first."""
        return (
            self.df.groupby(["cluster_code", "cluster_name"])
            .agg(
                incident_count=("estimated_cost_eur", "size"),
                total_cost_eur=("estimated_cost_eur", "sum"),
                total_downtime_hours=("downtime_hours", "sum"),
            )
            .reset_index()
            .sort_values("incident_count", ascending=False)
            .reset_index(drop=True)
        )

    def _render_clusters(self) -> str:
        """Render the top thematic clusters as a text block for the agents."""
        n_incidents = len(self.df)
        table = self.cluster_table
        thematic = table[table["cluster_code"] != NOISE_CLUSTER_CODE]
        noise = table[table["cluster_code"] == NOISE_CLUSTER_CODE]

        lines = []
        for _, cluster in thematic.head(self.N_SUMMARISED_CLUSTERS).iterrows():
            cluster_df = self.df[self.df["cluster_code"] == cluster["cluster_code"]]
            top_site = cluster_df.groupby("site")["estimated_cost_eur"].sum().idxmax()
            dominant_severity = cluster_df["severity"].value_counts().idxmax()
            lines.append(
                f"- {cluster['cluster_code']} — {cluster['cluster_name']} : "
                f"{int(cluster['incident_count'])} incidents "
                f"({100 * cluster['incident_count'] / n_incidents:.1f} %), "
                f"{cluster['total_cost_eur']:,.2f} EUR, "
                f"{cluster['total_downtime_hours']:,.1f} h de temps d'arrêt, "
                f"site le plus touché : {top_site}, "
                f"sévérité dominante : {dominant_severity}"
            )
        if not noise.empty:
            count = int(noise.iloc[0]["incident_count"])
            lines.append(
                f"- Incidents non classés (bruit) : {count} "
                f"({100 * count / n_incidents:.1f} %)"
            )
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Prompt templates — one private helper per prose section
    # ------------------------------------------------------------------

    def _synopsis_prompt(self) -> ChatPromptTemplate:
        """Prompt template of the executive synopsis section."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", SYNOPSIS_SYSTEM_PROMPT),
                (
                    "human",
                    (
                        "Type d'actif : {label}\n\n"
                        "Statistiques clés :\n{statistics}\n\n"
                        "Résumé des clusters :\n{clusters}\n\n"
                        "Descriptions des figures :\n{plot_descriptions}\n\n"
                        "Rédige le synopsis du rapport."
                    ),
                ),
            ]
        )

    def _methodology_prompt(self) -> ChatPromptTemplate:
        """Prompt template of the methodology section."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", METHODOLOGY_SYSTEM_PROMPT),
                (
                    "human",
                    (
                        "Type d'actif : {label}\n\n"
                        "Statistiques clés :\n{statistics}\n\n"
                        "Descriptions des figures :\n{plot_descriptions}\n\n"
                        "Rédige la section méthodologie du rapport."
                    ),
                ),
            ]
        )

    def _cluster_description_prompt(self) -> ChatPromptTemplate:
        """Prompt template of the description of a single cluster."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", CLUSTER_DESCRIPTION_SYSTEM_PROMPT),
                (
                    "human",
                    (
                        "Type d'actif : {label}\n\n"
                        "Cluster : {cluster_name} ({cluster_code})\n\n"
                        "Statistiques du cluster :\n{cluster_stats}\n\n"
                        "Descriptions des figures :\n{plot_descriptions}\n\n"
                        "Rédige la description de ce cluster."
                    ),
                ),
            ]
        )

    def _cost_drivers_prompt(self) -> ChatPromptTemplate:
        """Prompt template of the cost/downtime drivers identification."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", COST_DRIVERS_SYSTEM_PROMPT),
                (
                    "human",
                    (
                        "Type d'actif : {label}\n\n"
                        "Statistiques clés :\n{statistics}\n\n"
                        "Résumé des clusters :\n{clusters}\n\n"
                        "Descriptions des figures :\n{plot_descriptions}\n\n"
                        "Liste les principaux facteurs de coût et de temps "
                        "d'arrêt."
                    ),
                ),
            ]
        )

    def _draft_recommendations_prompt(self) -> ChatPromptTemplate:
        """Prompt template of the draft recommendations (one per driver)."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", DRAFT_RECOMMENDATIONS_SYSTEM_PROMPT),
                (
                    "human",
                    (
                        "Type d'actif : {label}\n\n"
                        "Facteurs de coût et de temps d'arrêt :\n"
                        "{cost_drivers}\n\n"
                        "Résumé des clusters :\n{clusters}\n\n"
                        "Descriptions des figures :\n{plot_descriptions}\n\n"
                        "Rédige une recommandation par facteur."
                    ),
                ),
            ]
        )

    def _prioritise_recommendations_prompt(self) -> ChatPromptTemplate:
        """Prompt template of the final prioritised recommendations list."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", PRIORITISE_RECOMMENDATIONS_SYSTEM_PROMPT),
                (
                    "human",
                    (
                        "Type d'actif : {label}\n\n"
                        "Statistiques clés :\n{statistics}\n\n"
                        "Descriptions des figures :\n{plot_descriptions}\n\n"
                        "Recommandations provisoires :\n"
                        "{draft_recommendations}\n\n"
                        "Rédige la liste à puces finale et priorisée."
                    ),
                ),
            ]
        )

    def _conclusion_prompt(self) -> ChatPromptTemplate:
        """Prompt template of the conclusion section."""
        return ChatPromptTemplate.from_messages(
            [
                ("system", CONCLUSION_SYSTEM_PROMPT),
                (
                    "human",
                    (
                        "Type d'actif : {label}\n\n"
                        "Statistiques clés :\n{statistics}\n\n"
                        "Descriptions des figures :\n{plot_descriptions}\n\n"
                        "Synopsis :\n{synopsis}\n\n"
                        "Recommandations :\n{recommendations}\n\n"
                        "Rédige la conclusion du rapport."
                    ),
                ),
            ]
        )

    # ------------------------------------------------------------------
    # Public API — write_* methods run the prompts and return the text
    # ------------------------------------------------------------------

    def write_synthese(self, report: str) -> str:
        """Generate a global synthesis from the complete Markdown report."""

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYNTHESE_SYSTEM_PROMPT),
            (
                "human",
                "Voici le rapport complet à analyser :\n\n{report}\n\n"
                "Rédige la synthèse générale du rapport."
            ),
        ])

        chain = prompt | self.llm | StrOutputParser()

        return chain.invoke(
            {"report": report},
            config={"callbacks": [self.token_usage]},
        )

    def write_synopsis(self, prose: ReportProse | None = None) -> str:
        """Generate the executive synopsis; stored in *prose* if given."""
        chain = self._synopsis_prompt() | self.llm | StrOutputParser()
        text = chain.invoke(
            {
                "label": self.label,
                "statistics": self.statistics,
                "clusters": self.clusters,
                "plot_descriptions": self.plot_descriptions_context,
            },
            config={"callbacks": [self.token_usage]},
        )
        if prose is not None:
            prose.synopsis = text
        return text

    def write_methodology(self, prose: ReportProse | None = None) -> str:
        """Generate the methodology section; stored in *prose* if given."""
        chain = self._methodology_prompt() | self.llm | StrOutputParser()
        text = chain.invoke(
            {
                "label": self.label,
                "statistics": self.statistics,
                "plot_descriptions": self.plot_descriptions_context,
            },
            config={"callbacks": [self.token_usage]},
        )
        if prose is not None:
            prose.methodology = text
        return text

    def write_cluster_description(
        self, cluster_code: str, cluster_name: str, cluster_stats: str
    ) -> str:
        """Generate the description of a single cluster."""
        chain = self._cluster_description_prompt() | self.llm | StrOutputParser()
        return chain.invoke(
            {
                "label": self.label,
                "cluster_code": cluster_code,
                "cluster_name": cluster_name,
                "cluster_stats": cluster_stats,
                "plot_descriptions": self.plot_descriptions_context,
            },
            config={"callbacks": [self.token_usage]},
        )

    def write_cluster_descriptions(
        self,
        n_clusters: int = N_DETAILED_CLUSTERS,
        prose: ReportProse | None = None,
    ) -> list[str]:
        """Generate one description per top thematic cluster (largest first)."""
        n_incidents = len(self.df)
        thematic = self.cluster_table[
            self.cluster_table["cluster_code"] != NOISE_CLUSTER_CODE
        ]
        descriptions = []
        for _, cluster in thematic.head(n_clusters).iterrows():
            code = cluster["cluster_code"]
            cluster_df = self.df[self.df["cluster_code"] == code]
            top_site = cluster_df.groupby("site")["estimated_cost_eur"].sum().idxmax()
            dominant_severity = cluster_df["severity"].value_counts().idxmax()
            cluster_stats = (
                f"{int(cluster['incident_count'])} incidents "
                f"({100 * cluster['incident_count'] / n_incidents:.1f} % de "
                f"tous les incidents), "
                f"{cluster['total_cost_eur']:,.2f} EUR de coût total estimé, "
                f"{cluster['total_downtime_hours']:,.1f} h de temps d'arrêt "
                f"total, site le plus touché : {top_site}, "
                f"sévérité dominante : {dominant_severity}"
            )
            descriptions.append(
                self.write_cluster_description(
                    code, cluster["cluster_name"], cluster_stats
                )
            )
        if prose is not None:
            prose.cluster_descriptions = descriptions
        return descriptions

    def write_recommendations(self, prose: ReportProse | None = None) -> str:
        """Generate the recommendations section; stored in *prose*.

        Recommendations are more complex than the other sections, so this
        writer merges three specialised prompt chains into a single langgraph
        graph:

        1. ``identify_drivers`` — extract the main cost/downtime drivers;
        2. ``draft_recommendations`` — draft one recommendation per driver;
        3. ``prioritise`` — merge, prioritise and format the final list.
        """
        if prose is None:
            prose = ReportProse()
        drivers_chain = self._cost_drivers_prompt() | self.llm | StrOutputParser()
        draft_chain = (
            self._draft_recommendations_prompt() | self.llm | StrOutputParser()
        )
        prioritise_chain = (
            self._prioritise_recommendations_prompt() | self.llm | StrOutputParser()
        )

        def identify_drivers(state: ReportState) -> ReportState:
            return {"cost_drivers": drivers_chain.invoke(dict(state))}

        def draft_recommendations(state: ReportState) -> ReportState:
            return {"draft_recommendations": draft_chain.invoke(dict(state))}

        def prioritise(state: ReportState) -> ReportState:
            return {"recommendations": prioritise_chain.invoke(dict(state))}

        graph = _new_state_graph()
        graph.add_node("identify_drivers", identify_drivers)
        graph.add_node("draft_recommendations", draft_recommendations)
        graph.add_node("prioritise", prioritise)
        graph.add_edge(START, "identify_drivers")
        graph.add_edge("identify_drivers", "draft_recommendations")
        graph.add_edge("draft_recommendations", "prioritise")
        graph.add_edge("prioritise", END)

        state: ReportState = {
            "label": self.label,
            "statistics": self.statistics,
            "clusters": self.clusters,
            "plot_descriptions": self.plot_descriptions_context,
        }
        text = graph.compile().invoke(state, config={"callbacks": [self.token_usage]})[
            "recommendations"
        ]
        prose.recommendations = text
        return text

    def write_conclusion(self, prose: ReportProse | None = None) -> str:
        """Generate the conclusion; stored in *prose*.

        The conclusion depends on the synopsis and the recommendations: if
        *prose* already contains them they are reused, otherwise the
        corresponding ``write_*`` method is called to generate them first.
        """
        if prose is None:
            prose = ReportProse()
        if prose.synopsis is None:
            self.write_synopsis(prose)
        if prose.recommendations is None:
            self.write_recommendations(prose)
        chain = self._conclusion_prompt() | self.llm | StrOutputParser()
        text = chain.invoke(
            {
                "label": self.label,
                "statistics": self.statistics,
                "plot_descriptions": self.plot_descriptions_context,
                "synopsis": prose.synopsis,
                "recommendations": prose.recommendations,
            },
            config={"callbacks": [self.token_usage]},
        )
        prose.conclusion = text
        return text

    def generate_prose(
        self,
        paragraphs: Sequence[str] = DEFAULT_PARAGRAPHS,
        n_clusters: int = N_DETAILED_CLUSTERS,
    ) -> ReportProse:
        """Generate the requested prose paragraphs into a :class:`ReportProse`.

        Each name in *paragraphs* is mapped to the corresponding
        ``write_<name>`` method (e.g. ``"methodology"`` ->
        :meth:`write_methodology`) and called in order with the shared
        :class:`ReportProse` object, so a section can reuse — or generate on
        demand — the sections it depends on. A name without a matching
        method triggers a warning and is skipped.
        """
        print(f"[{self.label}] Generating report prose with LLM agents...")
        prose = ReportProse()
        for name in paragraphs:
            writer = getattr(self, f"write_{name}", None)
            if not callable(writer):
                print(
                    f"[{self.label}] WARNING: no write_{name} method for "
                    f"paragraph '{name}', skipping it."
                )
                continue
            if name == "cluster_descriptions":
                writer(n_clusters=n_clusters, prose=prose)
            else:
                writer(prose=prose)
        return prose

    def print_token_usage(self) -> None:
        """Print the token usage accumulated by this factory's agents."""
        print(f"Token usage ({self.label}): {self.token_usage.summary()}")


class SolarReportFactory(ReportFactory):
    """Generates report prose for the solar fleet (label ``solar``)."""

    def __init__(
        self,
        df: pd.DataFrame,
        llm: BaseChatModel | None = None,
        plot_descriptions: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(df, "solar", llm=llm, plot_descriptions=plot_descriptions)

    @classmethod
    def from_csv(
        cls,
        csv_path: Path,
        llm: BaseChatModel | None = None,
        plot_descriptions: dict[str, dict[str, Any]] | None = None,
    ) -> "SolarReportFactory":
        return cls(pd.read_csv(csv_path), llm=llm, plot_descriptions=plot_descriptions)


class WindReportFactory(ReportFactory):
    """Generates report prose for the wind fleet (label ``wind``)."""

    def __init__(
        self,
        df: pd.DataFrame,
        llm: BaseChatModel | None = None,
        plot_descriptions: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(df, "wind", llm=llm, plot_descriptions=plot_descriptions)

    @classmethod
    def from_csv(
        cls,
        csv_path: Path,
        llm: BaseChatModel | None = None,
        plot_descriptions: dict[str, dict[str, Any]] | None = None,
    ) -> "WindReportFactory":
        return cls(pd.read_csv(csv_path), llm=llm, plot_descriptions=plot_descriptions)


def fill_template(template: str, context: dict[str, str]) -> str:
    """Replace every ``{{ variable_name }}`` placeholder in *template*.

    Raises
    ------
    ValueError
        If a placeholder has no matching key in *context*.
    """
    unknown: list[str] = []

    def _replace(match: re.Match) -> str:
        name = match.group(1)
        if name not in context:
            unknown.append(name)
            return match.group(0)
        return context[name]

    filled = PLACEHOLDER_PATTERN.sub(_replace, template)
    if unknown:
        raise ValueError(
            f"Unknown template placeholder(s): {', '.join(sorted(set(unknown)))}. "
            f"Available variables: {', '.join(sorted(context))}"
        )
    return filled


def _figure_markdown(plot_name: str, plots_dir: Path, report_dir: Path) -> str:
    """Markdown for one figure: a PNG image, or a link to the HTML version."""
    png_path = plots_dir / "png" / f"{plot_name}.png"
    if png_path.exists():
        relative = os.path.relpath(png_path, report_dir).replace(os.sep, "/")
        return f"![{plot_name}]({relative})"
    html_path = plots_dir / "html" / f"{plot_name}.html"
    if html_path.exists():
        relative = os.path.relpath(html_path, report_dir).replace(os.sep, "/")
        return f"[Interactive figure: {plot_name}]({relative})"
    raise FileNotFoundError(
        f"No figure found for plot '{plot_name}' in {plots_dir / 'png'} "
        f"or {plots_dir / 'html'} — run the plotting step first."
    )


def _load_plot_descriptions(plots_dir: Path) -> dict[str, dict[str, Any]]:
    """Load each plot's JSON description from *plots_dir/json*."""
    descriptions: dict[str, dict[str, Any]] = {}
    for path in sorted((plots_dir / "json").glob("plot_*.json")):
        description = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(description, dict):
            raise TypeError(f"Plot description must be a JSON object: {path}")
        descriptions[path.stem] = description
    return descriptions


def build_report_context(
    df: pd.DataFrame,
    label: str,
    plots_dir: Path,
    report_dir: Path,
    prose: ReportProse,
) -> dict[str, str]:
    """Build every template variable for one report.

    Real statistics come from *df* (the clusterised incidents dataframe);
    figures are resolved from *plots_dir* (``png`` and ``html`` subfolders) as
    ``figure_<plot_name>`` variables pointing relatively to *report_dir*.
    Prose blocks come from the :class:`ReportProse` object generated by
    :meth:`ReportFactory.generate_prose`.
    """
    if (
        prose.synopsis is None
        or prose.methodology is None
        or prose.cluster_descriptions is None
        or prose.recommendations is None
        or prose.conclusion is None
    ):
        raise ValueError(
            "Missing prose section(s) in the ReportProse object — generate "
            "every section with ReportFactory.generate_prose before "
            "building the report context."
        )
    cluster_descriptions = prose.cluster_descriptions
    if not isinstance(cluster_descriptions, list):
        raise TypeError("The 'cluster_descriptions' prose value must be a list.")

    n_incidents = len(df)
    severity_counts = df["severity"].value_counts()
    total_cost = df["estimated_cost_eur"].sum()
    total_downtime = df["downtime_hours"].sum()
    dates = pd.to_datetime(df["date"])
    top_site = df.groupby("site")["estimated_cost_eur"].sum().idxmax()
    top_equipment = df.groupby("equipment_id")["estimated_cost_eur"].sum().idxmax()

    # Clusters, largest first; the noise cluster is reported separately
    cluster_counts = (
        df.groupby(["cluster_code", "cluster_name"])
        .size()
        .to_frame("incident_count")
        .reset_index()
        .sort_values("incident_count", ascending=False)
    )
    thematic_counts = cluster_counts[
        cluster_counts["cluster_code"] != NOISE_CLUSTER_CODE
    ]

    rows = ["| Cluster | Incidents | Share |", "| --- | ---: | ---: |"]
    for _, cluster in cluster_counts.iterrows():
        code = cluster["cluster_code"]
        name = cluster["cluster_name"]
        count = cluster["incident_count"]
        cell = (
            f"{name} (unclassified)"
            if code == NOISE_CLUSTER_CODE
            else f"{code} — {name}"
        )
        rows.append(f"| {cell} | {count} | {100 * count / n_incidents:.1f}% |")
    top_clusters_table = "\n".join(rows)

    sections = []
    detailed_clusters = thematic_counts.head(N_DETAILED_CLUSTERS)
    if len(cluster_descriptions) != len(detailed_clusters):
        raise ValueError(
            "The generated cluster descriptions must match the number of "
            f"reported clusters ({len(detailed_clusters)}); received "
            f"{len(cluster_descriptions)}."
        )
    for (_, cluster), description in zip(
        detailed_clusters.iterrows(), cluster_descriptions
    ):
        code = cluster["cluster_code"]
        name = cluster["cluster_name"]
        count = cluster["incident_count"]
        cluster_df = df[df["cluster_code"] == code]
        cluster_top_site = (
            cluster_df.groupby("site")["estimated_cost_eur"].sum().idxmax()
        )
        dominant_severity = cluster_df["severity"].value_counts().idxmax()
        sections.append(
            f"### {code} — {name}\n\n"
            f"- **Incidents:** {count} ({100 * count / n_incidents:.1f}% of all incidents)\n"
            f"- **Most affected site:** {cluster_top_site}\n"
            f"- **Dominant severity:** {dominant_severity}\n\n"
            f"{description}"
        )
    cluster_sections = "\n\n".join(sections)

    context: dict[str, str] = {
        "report_title": f"{label.capitalize()} Asset Incident Analysis Report",
        "asset_label": label.capitalize(),
        "asset_label_lower": label,
        "generation_date": date.today().isoformat(),
        "n_incidents": str(n_incidents),
        "n_sites": str(df["site"].nunique()),
        "n_equipment": str(df["equipment_id"].nunique()),
        "period_start": dates.min().date().isoformat(),
        "period_end": dates.max().date().isoformat(),
        "total_cost_eur": f"{total_cost:,.2f}",
        "total_downtime_hours": f"{total_downtime:,.1f}",
        "avg_cost_per_incident": f"{total_cost / n_incidents:,.2f}",
        "n_minor": str(int(severity_counts.get("mineure", 0))),
        "n_moderate": str(int(severity_counts.get("modérée", 0))),
        "n_severe": str(int(severity_counts.get("sévère", 0))),
        "top_site_by_cost": str(top_site),
        "top_equipment_by_cost": str(top_equipment),
        "n_clusters": str(len(thematic_counts)),
        "top_clusters_table": top_clusters_table,
        "synopsis": prose.synopsis,
        "methodology": prose.methodology,
        "cluster_sections": cluster_sections,
        "recommendations": prose.recommendations,
        "conclusion": prose.conclusion,
    }

    # One figure_<plot_name> variable per available plot (PNG preferred,
    # interactive HTML as fallback)
    png_dir = plots_dir / "png"
    html_dir = plots_dir / "html"
    if not png_dir.is_dir() and not html_dir.is_dir():
        raise FileNotFoundError(
            f"No plots found in {plots_dir} — run the plotting step first "
            "(uv run datachallengecapgemini)."
        )
    plot_names = sorted(
        {path.stem for path in png_dir.glob("plot_*.png")}
        | {path.stem for path in html_dir.glob("plot_*.html")}
    )
    for plot_name in plot_names:
        context[f"{FIGURE_PLACEHOLDER_PREFIX}{plot_name}"] = _figure_markdown(
            plot_name, plots_dir, report_dir
        )

    return context


def render_report(template: str, context: dict[str, str], plots_dir: Path) -> str:
    """Fill *template* with *context*, warning about missing figures.

    A ``figure_<plot_name>`` placeholder without a matching plot is replaced
    by a placeholder note and a warning is printed, so the rest of the
    report is still filled.
    """
    context = dict(context)
    missing_figures = sorted(
        {
            match.group(1)
            for match in PLACEHOLDER_PATTERN.finditer(template)
            if match.group(1).startswith(FIGURE_PLACEHOLDER_PREFIX)
            and match.group(1) not in context
        }
    )
    for name in missing_figures:
        plot_name = name[len(FIGURE_PLACEHOLDER_PREFIX) :]
        print(
            f"WARNING: figure '{plot_name}' is mentioned in the template "
            f"but missing from {plots_dir / 'png'} and "
            f"{plots_dir / 'html'} — run the plotting step first."
        )
        context[name] = f"*(Figure manquante : {plot_name})*"
    return fill_template(template, context)


def run_reporting(
    solar_csv_path: Path,
    wind_csv_path: Path,
    plots_output_dir: Path,
    templates_dir: Path,
    reports_output_dir: Path,
) -> None:
    """Fill the solar and wind markdown templates and save the reports.

    Reads ``<templates_dir>/<label>_report.md`` for each label, fills it with
    statistics from the clusterised CSV and figures from
    ``<plots_output_dir>/<label>/{png,html,json}``, and writes the result to
    ``<reports_output_dir>/<label>/report.md``.

    Prose is generated by the LLM agents of :class:`ReportFactory` (Azure
    OpenAI, gpt-4.1-nano), and token usage is printed per report.
    """
    for label, factory_type, csv_path in (
        ("solar", SolarReportFactory, solar_csv_path),
        ("wind", WindReportFactory, wind_csv_path),
    ):
        template_path = templates_dir / f"{label}_report.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Report template not found: {template_path}")

        df = pd.read_csv(csv_path)
        plots_dir = plots_output_dir / label
        report_dir = reports_output_dir / label
        report_dir.mkdir(parents=True, exist_ok=True)

        plot_descriptions = _load_plot_descriptions(plots_dir)
        factory = factory_type(df, plot_descriptions=plot_descriptions)
        prose = factory.generate_prose()

        template = template_path.read_text(encoding="utf-8")
        context = build_report_context(df, label, plots_dir, report_dir, prose=prose)
        # 1. Generate the complete report from the template
        report = render_report(template, context, plots_dir)

        # 2. Ask the synthesis agent to read the complete report
        synthese = factory.write_synthese(report)

        # 3. Append the synthesis to the final report
        report = (
            report.rstrip()
            + "\n\n## Synthèse générale\n\n"
            + synthese.strip()
            + "\n"
        )

        # 4. Save the enriched report
        report_path = report_dir / "report.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"Saved {report_path}")

        factory.print_token_usage()
       

    print(f"Done. Filled reports are in {reports_output_dir}")


def add_report_arguments(parser: argparse.ArgumentParser) -> None:
    """Add report-generation-specific arguments to *parser*."""
    parser.add_argument(
        "--templates-dir",
        type=Path,
        default=PROJECT_ROOT / "templates",
        help="Directory containing the markdown report templates (<label>_report.md).",
    )
    parser.add_argument(
        "--reports-output-dir",
        type=Path,
        default=PROJECT_ROOT / "filled_templates",
        help="Directory where filled reports are saved (<label>/report.md subfolders are created inside).",
    )
