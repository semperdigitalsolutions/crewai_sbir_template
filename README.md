# CrewAI SBIR Template

Reusable multi-LLM workflow for SBIR Phase 1 (research, evaluation, ideation, documentation).

## Setup
- Clone for a new project: `git clone <repo-url> sbir-project-[topic]`
- cd into the new dir.
- Update `inputs/sample_sbir_topic.txt` with your solicitation/topic.
- Build/Run in Docker: `docker-compose up -d`
- Exec in: `docker-compose exec crewai-env bash`
- Run the crew: `python scripts/sbir_crew.py` (update to load input from file if needed).
- Outputs in `/outputs`.

## Customization
- Agents/Tasks in `scripts/agents.py` and `tasks.py`.
- For full runs, uncomment kickoff in `sbir_crew.py`.

## Notes
- Requires OpenCode.ai global.
- Tools like search need API keys (e.g., SERPER_API_KEY).