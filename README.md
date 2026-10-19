# DataChallengeCapGemini

Starter kit for the **Cap-Gemini DataChallenge for Mines Paris 2026** — incident analysis for PV (solar) and wind assets.

The goal is to build an agentic pipeline that, starting from incident reports in
`data/incidents_students.csv` and pdf reports in `data/pdf_scan` and `data/pdf_digital`, performs:

- **Topic modeling** (grouping incidents by theme),
- **Root-cause analysis**,
- **Global statistics** (by site, severity, seasonality, downtime, cost, etc.),
- **Remediation proposals** (maintenance actions, technical improvements).

The first building block — topic modeling — was already provided as a notebook, that was converted by us as a [marimo](https://marimo.io) notebook.

## Project structure

to run the project, it is important to include the `.env` file and the `data` folder to the cloned repository. In the end, you should have the following structure :

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

Install uv if you don't have it (here is the command for linux installation):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Scanned-PDF preprocessing uses Surya OCR with a llama.cpp server. Install
[llama.cpp](https://github.com/ggml-org/llama.cpp/blob/master/docs/install.md),
including the `llama` command with the `serve` subcommand:

```bash
curl -LsSf https://llama.app/install.sh | sh
```

Start the server in a separate terminal. The `-hf` option downloads Surya's
GGUF model and its multimodal projector automatically the first time:

```bash
llama serve -hf datalab-to/surya-ocr-2-gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --alias datalab-to/surya-ocr-2 \
  --ctx-size 16384 \
  --parallel 1
```

Keep that server running while preprocessing. In another terminal, point Surya
to it and run the preprocessing command:

```bash
export SURYA_INFERENCE_URL=http://127.0.0.1:8080/v1
uv run datachallengecapgemini-preprocess
```

Preprocessing does not start the server or download the model. It stops with
an error if `SURYA_INFERENCE_URL` is missing, or if the configured server is
unavailable or serving a different model.

The final pipeline step converts the markdown reports to PDF with
[pandoc](https://pandoc.org/). For the latest release, use the installer for
your platform from the [pandoc GitHub releases](https://github.com/jgm/pandoc/releases/latest)
(for example, the `.msi` on Windows, `.pkg` on macOS, or `.deb` on Debian/Ubuntu).
See Pandoc's [installation guide](https://pandoc.org/installing.html) for other
platforms and installation options. Make sure the `pandoc` command is on your
`PATH`.

PDF export also requires `xelatex`, the PDF engine used by this project. It is
available in [TeX Live](https://www.tug.org/texlive/) and other TeX
distributions; choose the installation for your operating system:

- **Debian/Ubuntu:** install XeLaTeX and commonly needed LaTeX packages:
  `sudo apt install texlive-xetex texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended`.
- **macOS:** install [MacTeX](https://tug.org/mactex/) for the more complete
  setup. [BasicTeX](https://tug.org/mactex/morepackages.html) is a smaller
  alternative, but may need additional TeX packages installed with `tlmgr`.
- **Windows:** install [MiKTeX](https://miktex.org/download) and allow it to
  install missing packages when prompted.

Check that both commands are available before running the pipeline:

```bash
pandoc --version
xelatex --version
```

Without pandoc, the pipeline stops with an error at the last step; you can
skip that step with `uv run dc --skip-pdf`.

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

## Running the pipeline

The full pipeline can be runned using:

```bash
uv run dc
```

`dc` is a short alias for the `datachallengecapgemini` command.

By default, plotting skips preprocessing and reads the pre-existing
`data/incidents_clusterised_solar.csv` and
`data/incidents_clusterised_wind.csv` files. Override their locations with
`--solar-csv` and `--wind-csv`. Solar and wind plots are written separately
under `data/plots/solar` and `data/plots/wind`.

The pipeline ends with a report-generation step: it fills the markdown
templates in `templates/` (`solar_report.md`, `wind_report.md`) with
statistics computed from the clusterised CSVs, the figures from
`data/plots/<label>/png`, and placeholder prose, then writes the filled
reports to `filled_templates/solar/report.md` and
`filled_templates/wind/report.md`. Templates use `{{ variable_name }}`
placeholders, including `{{ figure_<plot_name> }}` for figures. Override the
template and output locations with `--templates-dir` and
`--reports-output-dir`.

As a final step, each filled markdown report is converted to PDF with
pandoc, producing `filled_templates/solar/report.pdf` and
`filled_templates/wind/report.pdf` next to the markdown files. This step
requires `pandoc` and a PDF engine (see [Prerequisites](#prerequisites));
skip it with `--skip-pdf`.

You can also start the preprocessing only using:

```bash
uv run datachallengecapgemini-preprocess
```

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
| `uv sync --dev` | Install including dev dependencies (marimo,ruff,ty) |
| `uv add <package>` | Add a new dependency |
| `uv run marimo edit notebooks/starterkit_students.py` | Edit the notebook |
| `uv run marimo run notebooks/starterkit_students.py` | Run the notebook (read-only app mode) |
| `uv run python -m datachallengecapgemini` | Run the package entry point |

## Tech stack

- **marimo** — reactive notebook environment
- **BERTopic** — topic modeling
- **UMAP / HDBSCAN** — dimensionality reduction and clustering
- **Azure OpenAI** — embeddings (`text-embedding-3-small`) and chat (`gpt-4.1-nano`)
- **pandas / numpy / matplotlib / plotly** — data manipulation and visualization
- **uv** — dependency and environment management
