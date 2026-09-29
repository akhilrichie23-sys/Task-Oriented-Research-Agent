# Task-Oriented Research Agent

A cost-optimized, auditable, autonomous research pipeline built with **LangGraph**, **Google Gemini model routing**, **live web search (Tavily / DuckDuckGo)**, and **semantic caching**.

Built for the **Techvruk Agentic AI Challenge** under the *Task-Oriented Research Agents* track.

---

## Key Capabilities & Technical Highlights

- **Dynamic Task Deconstruction & Tiered Routing**: Automatically breaks complex research briefs into targeted search queries, routing lighter planning tasks to fast/cost-effective models and synthesizing final briefs with high-capacity models.
- **Semantic Caching**: In-memory and persistent disk cache keyed by prompt signature and model tier, achieving 100% token savings on repeated runs.
- **Real-Time Web Intelligence**: Multi-query search execution with resilient fallback engines and citation attribution.
- **Auditable Telemetry & FinOps**: Deterministic step-by-step audit logs in JSON format along with real-time USD token cost accounting.
- **Multi-Format Publication**: Generates structured Markdown reports and PDF briefs ready for decision-makers.

---

## Project Structure

```
├── main.py                     # Agent execution entry point
├── requirements.txt            # Python dependencies
├── SUBMISSION.md               # Challenge submission brief & architecture write-up
├── src/
│   ├── agent/                  # LangGraph state machine, router, and state schemas
│   ├── cache/                  # Semantic caching engine
│   ├── tools/                  # Live search & PDF generation tools
│   └── utils/                  # Audit logger and cost tracking telemetry
├── tests/                      # Automated unit test suite
└── outputs/                    # Generated research reports, PDFs, and audit logs
```

---

## Setup & Quickstart

### 1. Virtual Environment & Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `.env.example` to `.env` and set your API keys:
```bash
cp .env.example .env
```
Key configuration parameters:
- `GEMINI_API_KEY`: API key for Google Gemini models.
- `TAVILY_API_KEY` (Optional): For enhanced web search (falls back to DuckDuckGo if unset).

### 3. Running the Agent
```bash
python main.py
```

### 4. Running the Test Suite
```bash
python -m unittest discover tests
```
