from crewai import Agent
from crewai.llm import LLM
import os  # For env var

# from crewai_tools import SerperDevTool  # Commented for now; revisit later

# Define LLMs using OpenRouter API (set OPENROUTER_API_KEY in .env)
deepseek_v3_llm = LLM(
    model="deepseek/deepseek-chat-v3-0324",  # Cheap reasoning for research/evaluation
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    custom_llm_provider="openrouter"
)

kimi_k2_llm = LLM(
    model="moonshotai/kimi-k2",  # For innovation, reasoning, code (paid upgrade)
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    custom_llm_provider="openrouter"
)

gemini_25_flash_llm = LLM(
    model="google/gemini-2.5-flash",  # For synthesis, long context
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    custom_llm_provider="openrouter"
)

# Agent 1: Researcher
researcher = Agent(
    role='SBIR Researcher',
    goal='Gather and summarize information on SBIR topics, solicitations, prior art, and feasibility.',
    backstory=(
        "You are an expert in SBIR research, skilled at analyzing solicitations and identifying key requirements. "
        "Use tools like web search for up-to-date info. Output a structured report with sections: Overview, Key Requirements, Prior Art, Feasibility Gaps."
    ),
    llm=deepseek_v3_llm,  # Assigned: deepseek-chat-v3-0324 for cost-effective reasoning/tool use
    tools=[],  # Commented search_tool; revisit later
    verbose=True,
    allow_delegation=False  # No delegation for now
)

# Agent 2: Evaluator
evaluator = Agent(
    role='SBIR Evaluator',
    goal='Critique outputs for accuracy, completeness, bias, and SBIR compliance on a 1-10 scale.',
    backstory=(
        "You are a rigorous evaluator with SBIR expertise. Score each criterion (accuracy, completeness, innovation, feasibility) "
        "and provide overall score. If overall <8, note revisions needed."
    ),
    llm=deepseek_v3_llm,  # Assigned: deepseek-chat-v3-0324 for cost-effective reasoning/tool use
    verbose=True,
    allow_delegation=False
)

# Agent 3: Ideator
ideator = Agent(
    role='SBIR Ideator',
    goal='Brainstorm innovative solutions and technical approaches based on research.',
    backstory=(
        "You are a creative innovator specializing in SBIR Phase 1 ideas. Generate 3-5 concepts, rank them by feasibility and novelty, "
        "and outline experiments. Ensure alignment with solicitation goals."
    ),
    llm=kimi_k2_llm,  # Assigned: kimi-k2 for innovation/reasoning
    verbose=True,
    allow_delegation=False
)

# Agent 4: Synthesizer
synthesizer = Agent(
    role='SBIR Synthesizer',
    goal='Combine research, ideas, and evaluations into a cohesive solution outline.',
    backstory=(
        "You integrate diverse inputs, resolve conflicts, and produce a unified outline. "
        "Prioritize the best ideas and incorporate evaluator feedback."
    ),
    llm=gemini_25_flash_llm,  # Assigned: gemini-2.5-flash for reasoning/synthesis
    verbose=True,
    allow_delegation=False
)

# Agent 5: Documenter
documenter = Agent(
    role='SBIR Documenter',
    goal='Draft Phase 1 proposal sections like abstract, technical plan, and budget justification.',
    backstory=(
        "You are a professional SBIR writer. Use templates for Phase 1 (e.g., 15-page limit). "
        "Output in Markdown format with sections: Abstract, Approach, Commercial Potential."
    ),
    llm=kimi_k2_llm,  # Assigned: kimi-k2 for innovation/reasoning
    verbose=True,
    allow_delegation=False
)