# DataChallengeCapGemini

Starter kit for the **Hackathon Mines Paris 2026** — incident analysis for PV (solar) and wind assets.

The goal is to build an agentic pipeline that, starting from incident reports in
`data/incidents_students.csv`, performs:

- **Topic modeling** (grouping incidents by theme),
- **Root-cause analysis**,
- **Global statistics** (by site, severity, seasonality, downtime, cost, etc.),
- **Remediation proposals** (maintenance actions, technical improvements).

This repository ships the first building block — topic modeling — as a [marimo](https://marimo.io) notebook.

## Project structure

```
├── data/                          # Incident data (CSV + PDFs, gitignored)
│   ├── incidents_students.csv     # Main dataset (1800 reports)
│   ├── pdf_digital/               # Digital PDFs (extractable text)
│   └── pdf_scan/                  # Scanned PDFs (require OCR)
├── notebooks/
│   └── starterkit_students.py     # marimo notebook — topic modeling pipeline
├── src/
│   └── datachallengecapgemini/    # Python package
├── pyproject.toml                 # Project metadata and dependencies (uv)
├── uv.lock                        # Locked dependency versions
├── .python-version                # Python version pin (3.13)
└── .env                           # Azure OpenAI credentials (gitignored, never commit)
```

## Prerequisites

- **Python 3.13** (pinned in `.python-version`)
- **[uv](https://docs.astral.sh/uv/)** — fast Python package and environment manager

Install uv if you don't have it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Setup

### 1. Clone and enter the project

```bash
git clone <repo-url>
cd DataChallengeCapGemini
```

### 2. Install dependencies

`uv` reads `pyproject.toml` and creates a virtual environment in `.venv/` automatically:

```bash
uv sync
```

This installs all runtime dependencies (BERTopic, HDBSCAN, UMAP, pandas, OpenAI SDK, etc.)
and the dev dependencies (marimo).

### 3. Configure environment variables

The notebook calls Azure OpenAI for embeddings and chat completions. Create a `.env` file
in the project root:

```bash
cp .env.example .env   # if an example is provided, otherwise create it manually
```

Fill in your Azure OpenAI credentials:

```dotenv
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://<your-resource>.cognitiveservices.azure.com/
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_CHAT_DEPLOYMENT=<your-chat-deployment-name>
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<your-embedding-deployment-name>
```

> **Note:** `.env` is listed in `.gitignore` — never commit your API keys.
> The endpoint must be the Azure OpenAI **resource** endpoint, not a `/api/projects/...` URL.

### 4. Data

The dataset (`data/incidents_students.csv` and the PDF folders) is gitignored. If you are
participating in the hackathon, the data is provided on-site. Place it in the `data/`
directory at the project root.

The CSV contains 1800 incident reports with columns such as `incident_id`, `site`,
`asset_type`, `date`, `severity`, `downtime_hours`, `estimated_cost_eur`,
`weather_condition`, `text`, `document_format`, and `document_path`.

Three document formats are present:

| Format        | Description                                   | Location            |
|---------------|-----------------------------------------------|---------------------|
| `text`        | Text already available in the CSV             | `text` column       |
| `pdf_digital` | Digital PDF (extractable text)                | `data/pdf_digital/` |
| `pdf_scan`    | Scanned PDF (image, requires OCR)             | `data/pdf_scan/`    |

The starter kit only uses the `text` subset (~600 reports) to get you started quickly.

## Running the notebook

The notebook is a **marimo** notebook (not Jupyter). Start the marimo server:

```bash
uv run marimo run notebooks/starterkit_students.py
```

Then open the URL shown in the terminal (default: <http://localhost:2718>).

To run the notebook as a script (non-interactive, executes all cells top to bottom):

```bash
uv run marimo run notebooks/starterkit_students.py --no-token
```

Or export it to other formats:

```bash
# Export to HTML
uv run marimo export html notebooks/starterkit_students.py -o notebook.html

# Export to a Jupyter notebook (.ipynb)
uv run marimo export ipynb notebooks/starterkit_students.py -o notebook.ipynb

# Export to a plain Python script
uv run marimo export script notebooks/starterkit_students.py -o notebook_script.py
```

## Editing the notebook

To edit the notebook interactively, start marimo in **edit mode**:

```bash
uv run marimo edit notebooks/starterkit_students.py
```

This opens the marimo editor in your browser where you can:

- Add, remove, and reorder cells,
- Edit code and Markdown cells,
- Run cells individually or run all (`Ctrl+Enter` / `Shift+Enter`),
- See outputs inline.

marimo notebooks are stored as plain Python files (`.py`), making them easy to version
control with git — no JSON `.ipynb` merge conflicts.

### Notebook workflow

The starter kit notebook (`notebooks/starterkit_students.py`) follows this pipeline:

1. **Configuration** — loads `.env`, sets up SSL (truststore), reads Azure OpenAI settings.
2. **Load data** — reads `data/incidents_students.csv`, filters to `document_format == "text"`.
3. **Compute embeddings** — calls Azure OpenAI embeddings in batches, with retry on rate limits
   and local caching (`embeddings_students.npy`) to avoid recomputation.
4. **Topic modeling** — BERTopic with UMAP (dimensionality reduction) + HDBSCAN (clustering)
   + CountVectorizer (French stopwords). It exhaustively tests integer `min_cluster_size` values
   from 2 to 20% of the wind incident count, then refits only values where the cluster count
   changes for downstream comparison.
5. **Select cluster size** — compares the retained `min_cluster_size` values and sends the observed
   fusions, incident texts, and severities to Azure OpenAI on button click. Azure prioritizes
   preserving diagnostically distinct clusters and reports remaining redundant topic groups.
6. **Explore results** — topic info, bar charts, hierarchy visualization, example documents.
7. **Name clusters** — prepares an ordered harness containing every topic name and all of its
   texts, then sends it to the configured Azure OpenAI chat deployment on button click. The
   response maps each existing topic ID and name to a concise, distinctive French name; topic
   `-1` remains labeled as unclassified noise.
8. **Next steps** — suggestions for extending the pipeline (PDF processing, agent-based
   remediation, cross-referencing with metadata, etc.).

The two Azure chat requests print their actual input/output token usage and an **estimated**
USD cost after completion. The estimate assumes public pay-as-you-go GPT-4.1 nano rates
($0.10/1M uncached input tokens, $0.025/1M cached input tokens, $0.40/1M output tokens);
actual charges can differ with the deployed model, region, pricing agreement, or billing mode.
See [Azure OpenAI pricing](https://azure.microsoft.com/en-us/pricing/details/azure-openai/).

## Useful commands

| Command | Description |
|---------|-------------|
| `uv sync` | Install / update all dependencies |
| `uv sync --dev` | Install including dev dependencies (marimo) |
| `uv add <package>` | Add a new dependency |
| `uv run marimo edit notebooks/starterkit_students.py` | Edit the notebook |
| `uv run marimo run notebooks/starterkit_students.py` | Run the notebook (read-only app mode) |
| `uv run python -m datachallengecapgemini` | Run the package entry point |

## Tech stack

- **marimo** — reactive notebook environment
- **BERTopic** — topic modeling
- **UMAP / HDBSCAN** — dimensionality reduction and clustering
- **Azure OpenAI** — embeddings (`text-embedding-3-small`) and chat (`gpt-4.1-nano`)
- **pandas / numpy / matplotlib** — data manipulation and visualization
- **uv** — dependency and environment management
