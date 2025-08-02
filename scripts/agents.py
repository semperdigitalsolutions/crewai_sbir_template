from crewai import Agent
# from crewai_tools import SerperDevTool  # Commented for now; revisit later

from opencode_llm import create_opencode_llm  # Updated import

# Define LLMs as callables (using free OpenRouter models via OpenCode for testing)
deepseek_v3_llm = create_opencode_llm('openrouter/deepseek/deepseek-chat-v3-0324:free')  # Good for creative/research tasks (235B params)
qwen_coder_llm = create_opencode_llm('openrouter/qwen/qwen3-coder:free')  # Analytical/coding-focused (131B params)
deepseek_r1_llm = create_opencode_llm('openrouter/deepseek/r1:free')  # Balanced for synthesis/ideation (37B params)

# Agent 1: Researcher
researcher = Agent(
    role='SBIR Researcher',
    goal='Gather and summarize information on SBIR topics, solicitations, prior art, and feasibility.',
    backstory=(
        "You are an expert in SBIR research, skilled at analyzing solicitations and identifying key requirements. "
        "Use tools like web search for up-to-date info. Output a structured report with sections: Overview, Key Requirements, Prior Art, Feasibility Gaps."
    ),
    llm=deepseek_v3_llm,  # Free model for research
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
    llm=qwen_coder_llm,  # Free model for analytical critiques
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
    llm=deepseek_r1_llm,  # Free model for ideation
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
    llm=deepseek_v3_llm,  # Free model for synthesis
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
    llm=qwen_coder_llm,  # Free model for structured drafting
    verbose=True,
    allow_delegation=False
)