# CrewAI SBIR Template

Reusable multi-LLM workflow for SBIR Phase 1 (research, evaluation, ideation, documentation) using CrewAI.

## Setup
- Clone for a new project: `git clone git@github.com:semperdigitalsolutions/crewai_sbir_template.git sbir-project-[SBIR-NUMBER]`
- cd into the new dir.
- Update `inputs/topic.txt` with your solicitation/topic details.
- Build/Run in Docker: `docker-compose build` then `docker-compose up -d`
- Shell in: `docker-compose exec crewai-env bash`
- Run the crew: `python scripts/sbir_crew.py` (outputs to console; extend for files).
- Stop: `docker-compose down`.

## Customization
- Agents/Tasks in `scripts/agents.py` and `tasks.py`.
- LLMs in `agents.py` (defaults to free OpenRouter models; swap to subscribed like Claude by changing model strings).
- For full runs, ensure OpenCode is configured (auth for OpenRouter if using free models).
- Tools like search (SerperDevTool): Uncomment in agents.py, set SERPER_API_KEY env var (sign up at serper.dev).

## Troubleshooting
- LLM Errors: Ensure OpenCode is installed/authenticated; test with `opencode run "test" --model openrouter/deepseek/deepseek-chat-v3-0324:free`.
- Docker Issues: Rebuild with `docker-compose build --no-cache` if changes don't apply.
- Memory=True: Set if needed, but requires OPENAI_API_KEY for embeddings.
- Rate Limits: Free models have quotas; switch to subscribed for production.

## Enhancements
- Add file outputs to `outputs/` in sbir_crew.py.
- Enable tools/search for research agent.
- For Phase 2, add developer agent for code gen.

Notes: Requires OpenCode.ai global. Tools may need API keys.