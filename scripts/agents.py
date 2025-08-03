from crewai import Agent
from crewai.llm import LLM
import os  # For env var

# from crewai_tools import SerperDevTool  # Commented for now; revisit later

# Possible Models
# x-ai/grok-4
# anthropic/claude-opus-4
# google/gemini-2.5-pro
# google/gemini-2.5-flash
# deepseek/deepseek-chat-v3-0324
# moonshotai/kimi-k2


# Define LLMs using OpenRouter API (set OPENROUTER_API_KEY in .env)
deepseek_llm = LLM(
    model="deepseek/deepseek-chat-v3-0324",  # Reasoning for research/evaluation
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    custom_llm_provider="openrouter",
)

kimi_k2_llm = LLM(
    model="moonshotai/kimi-k2",  # For innovation, reasoning, code (paid upgrade)
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    custom_llm_provider="openrouter",
)

gemini_2_5_flash_llm = LLM(
    model="google/gemini-2.5-flash",  # For synthesis, long context
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    custom_llm_provider="openrouter",
)

# Agent 1: Researcher
researcher = Agent(
    role="SBIR Researcher",
    goal="Gather and summarize information on SBIR topics, solicitations, prior art, and feasibility.",
    backstory=(
        "You are an expert in SBIR research, skilled at analyzing 2025 solicitations and identifying key requirements (e.g., eligibility, data rights). "
        "Use tools like web_search or browse_page for up-to-date info on DSIP/BAAs. Output a structured report with sections: Overview, Key Requirements, Prior Art, Feasibility Gaps, including citations and limited to 800-1200 words."
    ),
    llm=kimi_k2_llm,  # Keep for reasoning/tool use
    tools=[],
    # tools=[web_search, browse_page],  # Enable for real-time sources
    verbose=True,
    allow_delegation=False,
)

# Agent 2: Evaluator
evaluator = Agent(
    role="SBIR Evaluator",
    goal="Critique outputs for accuracy, completeness, bias, and SBIR compliance on a 1-10 scale.",
    backstory=(
        "You are a rigorous evaluator with SBIR expertise. Score each criterion (accuracy, completeness, innovation, feasibility, commercialization) "
        "and provide overall score. If overall <8, note Phase 1-specific revisions needed, referencing DoD templates."
    ),
    llm=gemini_2_5_flash_llm,  # Keep for evaluation strength
    tools=[],
    # tools=[web_search],  # Optional for verifying facts
    verbose=True,
    allow_delegation=False,
)

# Agent 3: Ideator
ideator = Agent(
    role="SBIR Ideator",
    goal="Brainstorm innovative solutions and technical approaches based on research.",
    backstory=(
        "You are a creative innovator specializing in SBIR Phase 1 ideas. Generate 3-5 concepts, rank them by feasibility, novelty, and dual-use impact, "
        "and outline experiments with risks/mitigations. Ensure alignment with solicitation goals and 2025 DoD priorities; limit to 800-1200 words."
    ),
    llm=kimi_k2_llm,  # Keep for innovation
    tools=[],
    # tools=[web_search, x_keyword_search],  # For trends/inspiration
    verbose=True,
    allow_delegation=False,
)

# Agent 2b: Secondary Researcher (for consensus)
secondary_researcher = Agent(
    role="Secondary SBIR Researcher",
    goal="Provide an alternative and diverse perspective on the SBIR topic research.",
    backstory=(
        "You are an expert in SBIR research with a knack for finding information others might miss, like 2025 updates or dual-use angles. "
        "Provide a second, independent analysis to ensure comprehensive coverage, including citations; limit to 600-900 words."
    ),
    llm=deepseek_llm,  # Keep for different viewpoint
    tools=[],
    # tools=[web_search, browse_page],  # Enable for fresh sources
    verbose=True,
    allow_delegation=False,
)

# Agent 4: Consensus Agent (formerly Synthesizer)
consensus_agent = Agent(
    role="SBIR Consensus Agent",
    goal="Merge multiple research reports into a single, cohesive, and superior summary.",
    backstory=(
        "You specialize in synthesizing diverse information. Take reports from researchers, identify critical points, resolve discrepancies with SBIR focus (e.g., Phase 1 feasibility), "
        "and produce a unified report with citations; limit to 1000-1500 words."
    ),
    llm=gemini_2_5_flash_llm,  # Keep for synthesis
    tools=[],
    # tools=[web_search],  # For resolving conflicts
    verbose=True,
    allow_delegation=False,
)

# Agent 5: Documenter
documenter = Agent(
    role="SBIR Documenter",
    goal="Draft Phase 1 proposal sections like abstract, technical plan, and budget justification.",
    backstory=(
        "You are a professional SBIR writer. Use 2025 DoD templates (e.g., 10-15 page equiv.), draft abstract (<3000 chars), approach (with milestones), budget (justified rates), and commercial potential (dual-use). "
        "Output in Markdown; limit to 2000-3000 words."
    ),
    llm=gemini_2_5_flash_llm,  # Swap for better drafting
    tools=[],
    # tools=[web_search],  # For market data
    verbose=True,
    allow_delegation=False,
)
