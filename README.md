# CrewAI SBIR Template

Reusable, multi‑LLM workflow for SBIR Phase I (research → evaluation → ideation → documentation → SOP planning) using CrewAI.

## Features
- Multi‑idea ideation (5–6 ideas), drafting top 3–4 ideas with per‑idea output folders
- Live research with web search and scraping tools (SerperDevTool, ScrapeWebsiteTool)
- Placeholder‑driven drafting (no fabricated company data) and Cost Volume worksheet templates
- Post‑win SOP template generation with review and revision loop
- Robust error handling for LLM init and file I/O
- CLI input for topic file and basic post‑processing score checks
- Pytest unit tests for score parsing and multi‑idea splitting

## Prerequisites
- Python 3.10+
- Docker + docker‑compose (optional, recommended)
- Accounts/API keys (if using tools/models):
  - OPENROUTER_API_KEY (https://openrouter.ai)
  - SERPER_API_KEY (https://serper.dev)

## Setup
1) Clone for a new project
- `git clone git@github.com:semperdigitalsolutions/crewai_sbir_template.git sbir-project-[SBIR-NUMBER]`
- `cd sbir-project-[SBIR-NUMBER]`

2) Create environment file `.env`
- Add required keys:
  - `OPENROUTER_API_KEY=...`
  - `SERPER_API_KEY=...`

3a) Run in Docker
- `docker-compose build`
- `docker-compose up -d`
- Shell in: `docker-compose exec crewai-env bash`

3b) Or run locally (no Docker)
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -U pip`
- Install deps used here: `pip install crewai crewai-tools pytest`

## Provide the Topic Input
- Edit `inputs/topic.txt` with your solicitation/topic details, or prepare another file.

## Run the Pipeline
- Docker shell or local shell:
- `python scripts/sbir_crew.py --topic inputs/topic.txt`
  - You can pass any file: `python scripts/sbir_crew.py -t path/to/your_topic.txt`

## Outputs
- All artifacts go to `outputs/`:
  - `sbir_research_overview.md`
  - `secondary_sbir_research.md`
  - `consolidated_research.md`
  - `research_critique.md`
  - `proposed_ideas_and_ranks.md`
  - `ideas_critique.md`
  - `proposal_draft_sections.md`
  - `compliance_report.md`
  - `proposal_critique_and_scores.md`
  - `project_plan_template.md`
  - `project_plan_critique.md`
  - `final_project_plan.md`
  - `writer_handoff.md`
  - `post_win_approach_overview.md`
  - `final_output.md`

- Multi‑idea drafts also create per‑idea directories:
  - `outputs/idea_1_template/`
    - `proposal_draft_sections.md`
    - `volume_1.md`, `volume_2.md`, …
  - `outputs/idea_2_template/` …

## Important drafting rules (built‑in)
- Phase I constraints standardized to: **6 months, $150K max**
- Do not fabricate company‑specific info (bios, past performance, costs). Use bracketed instructional placeholders, e.g.:
  - `[INSERT Principal Investigator Name and 3–4 sentence bio …]`
  - `[CALCULATE Direct Labor based on SOW hours x blended rate]`
- Cost Volume (Volume 3) uses placeholder formulas (no invented numbers)
- Compliance content:
  - Include sample Markdown tables for certifications (ITAR, FOCI, Section 889)
  - Include Data Rights (DFARS) and ITAR/EAR compliance tables within Volume 2
- Commercialization content:
  - Add competitive landscape analysis and potential pricing strategies
- Ideation content:
  - Quantify risks (1–5 scale) and include specific, measurable experiment metrics

## Tools
- Research agents use:
  - `SerperDevTool` (web search) — requires `SERPER_API_KEY`
  - `ScrapeWebsiteTool` (scraping)
- Configure tools in `scripts/agents.py` and ensure API keys are set via environment or `.env`.

## Tests
- Pytest tests live in `tests/`.
- Run from repo root:
```bash
pytest -q
```
- Covered:
  - Decimal‑friendly score parsing (`parse_overall_score`)
  - Multi‑idea splitting (`split_multi_idea_blocks`)

## Troubleshooting
- Missing/invalid API keys
  - Ensure `.env` contains `OPENROUTER_API_KEY` and (for search) `SERPER_API_KEY`.
  - In Docker, rebuild if env changed: `docker-compose build --no-cache && docker-compose up -d`.
- File I/O errors
  - Outputs directory is created automatically; errors are logged and do not crash the run.
- Rate limits or model availability
  - Consider switching to subscribed models in `scripts/agents.py`.

## Customization
- Agents: `scripts/agents.py`
- Tasks/prompts: `scripts/tasks.py`
- Orchestrator / CLI / utilities: `scripts/sbir_crew.py`

---

If you need help tailoring prompts, outputs, or adding new tasks/agents, open an issue or ping the maintainer.
