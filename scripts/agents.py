from crewai import Agent
# from crewai_tools import SerperDevTool  # For web search; requires SERPER_API_KEY env var (set later if using)
from opencode_llm import OpenCodeLLM  # Your custom wrapper

# Initialize tools (e.g., web search; optional for now)
# search_tool = SerperDevTool()  # Free tier available; sign up at serper.dev for API key

# Define LLMs (using your subscriptions via OpenCode)
claude_llm = OpenCodeLLM(model='claude-3.5-sonnet')  # Creative tasks
gpt_llm = OpenCodeLLM(model='gpt-4o')  # Analytical tasks
gemini_llm = OpenCodeLLM(model='gemini-1.5-pro')  # Synthesis/ideation

# Agent 1: Researcher
researcher = Agent(
    role='SBIR Researcher',
    goal='Gather and summarize information on SBIR topics, solicitations, prior art, and feasibility.',
    backstory=(
        "You are an expert in SBIR research, skilled at analyzing solicitations and identifying key requirements. "
        "Use tools like web search for up-to-date info. Output a structured report with sections: Overview, Key Requirements, Prior Art, Feasibility Gaps."
    ),
    llm=claude_llm,
    # tools=[search_tool],
    tools=[],
    verbose=True,
    allow_delegation=False  # No delegation for now
)

# Agent 2: Evaluator
evaluator = Agent(
    role='SBIR Evaluator',
    goal='Critique outputs for accuracy, completeness, bias, and SBIR compliance on a 1-10 scale.',
    backstory=(
        "You are a rigorous evaluator with SBIR expertise. Score each criterion (accuracy, completeness, innovation, feasibility) "
        "and suggest improvements. If score <8 overall, recommend revisions."
    ),
    llm=gpt_llm,
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
    llm=gemini_llm,
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
    llm=claude_llm,  # Or use a local Ollama if extending
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
    llm=gpt_llm,
    verbose=True,
    allow_delegation=False
)