from crewai import Agent
from crewai.llm import LLM
import os  # For env var

from crewai_tools import SerperDevTool, ScrapeWebsiteTool  # Uncommented and assuming it's installed; for web_search and scraping

# Possible Models
# x-ai/grok-4
# anthropic/claude-opus-4
# google/gemini-2.5-pro
# google/gemini-2.5-flash
# deepseek/deepseek-chat-v3-0324
# moonshotai/kimi-k2


# Define LLMs using OpenRouter API (set OPENROUTER_API_KEY in .env)
try:
    deepseek_llm = LLM(
        model="deepseek/deepseek-chat-v3-0324",  # Reasoning for research/evaluation
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )
except Exception as e:
    print(f"Warning initializing LLM deepseek/deepseek-chat-v3-0324: {e}")
    deepseek_llm = LLM(
        model="google/gemini-2.5-flash",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )

try:
    kimi_k2_llm = LLM(
        model="moonshotai/kimi-k2",  # For innovation, reasoning, code (paid upgrade)
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )
except Exception as e:
    print(f"Warning initializing LLM moonshotai/kimi-k2: {e}")
    kimi_k2_llm = LLM(
        model="google/gemini-2.5-flash",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )

try:
    gemini_2_5_flash_llm = LLM(
        model="google/gemini-2.5-flash",  # For synthesis, long context
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )
except Exception as e:
    print(f"Warning initializing LLM google/gemini-2.5-flash: {e}")
    gemini_2_5_flash_llm = LLM(
        model="x-ai/grok-4",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )

try:
    grok_4_llm = LLM(
        model="x-ai/grok-4",  # Reasoning for research/evaluation
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )
except Exception as e:
    print(f"Warning initializing LLM x-ai/grok-4: {e}")
    grok_4_llm = LLM(
        model="google/gemini-2.5-flash",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )

try:
    claude_opus_4_llm = LLM(
        model="anthropic/claude-opus-4.1",  # Reasoning for research/evaluation
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )
except Exception as e:
    print(f"Warning initializing LLM anthropic/claude-opus-4.1: {e}")
    claude_opus_4_llm = LLM(
        model="google/gemini-2.5-flash",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )

try:
    gemini_2_5_pro_llm = LLM(
        model="google/gemini-2.5-pro",  # Reasoning for research/evaluation
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )
except Exception as e:
    print(f"Warning initializing LLM google/gemini-2.5-pro: {e}")
    gemini_2_5_pro_llm = LLM(
        model="google/gemini-2.5-flash",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )

try:
    claude_sonnet_4_llm = LLM(
        model="anthropic/claude-sonnet-4",  # Reasoning for research/evaluation
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )
except Exception as e:
    print(f"Warning initializing LLM anthropic/claude-sonnet-4: {e}")
    claude_sonnet_4_llm = LLM(
        model="google/gemini-2.5-flash",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        custom_llm_provider="openrouter",
    )

# Configure search and scrape tools (requires SERPER_API_KEY in environment for search)
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# Agent 1: Researcher
researcher = Agent(
    role="SBIR Researcher",
    goal="Gather and summarize information on SBIR topics, solicitations, prior art, and feasibility.",
    backstory=(
        "You are an expert in SBIR research, skilled at analyzing 2025 solicitations and identifying key requirements (e.g., eligibility, data rights). "
        "Use tools like web_search or browse_page for up-to-date info on DSIP/BAAs. Output a structured report with sections: Overview, Key Requirements, Prior Art, Feasibility Gaps, including citations and limited to 800-1200 words."
    ),
    llm=grok_4_llm,  # Assigned Grok-4 for strong reasoning and tool integration in primary research
    tools=[search_tool, scrape_tool],
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
    llm=claude_opus_4_llm,  # Assigned Claude-Opus-4 for rigorous, detailed critique and analysis
    tools=[],
    verbose=True,
    allow_delegation=False,
)

# Agent 3: Ideator
ideator = Agent(
    role="SBIR Ideator",
    goal="Brainstorm innovative solutions and technical approaches based on research.",
    backstory=(
        "You are a creative innovator specializing in SBIR Phase 1 ideas. Generate 5-6 concepts, rank them by feasibility, novelty, and dual-use impact, "
        "and outline experiments with risks/mitigations. Ensure alignment with solicitation goals and 2025 DoD priorities; limit to 1000-1500 words."
    ),
    llm=grok_4_llm,  # Assigned Grok-4 for creative brainstorming and innovative concept generation
    tools=[],
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
    llm=gemini_2_5_pro_llm,  # Assigned Gemini-2.5-Pro for long-context handling and diverse viewpoints in secondary research
    tools=[search_tool, scrape_tool],
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
    llm=claude_opus_4_llm,  # Assigned Claude-Opus-4 for superior synthesis and cohesive merging of reports
    tools=[],
    verbose=True,
    allow_delegation=False,
)

# Agent 5: Documenter
documenter = Agent(
    role="SBIR Documenter",
    goal="Draft comprehensive Phase 1 proposal sections aligned with DoD SBIR templates, including all required volumes.",
    backstory=(
        "You are a professional SBIR writer specializing in DoD/USAF proposals. Use the 2025 DoD template structure (e.g., Volume 1: Cover Sheet with abstract/benefits; Volume 2: Technical Volume with SOW, related work; Volume 3: Cost Volume; etc.). "
        "Draft sections based on ideation/evaluation, ensuring compliance with elements like foreign nationals, data rights, and DSIP requirements. Include placeholders for certifications/supporting docs. "
        "You must include required certifications (e.g., ITAR, FOCI, Section 889) as sample Markdown tables in the proposal draft. "
        "Output in Markdown with clear volume/section headings; limit to 3000-5000 words total."
    ),
    llm=gemini_2_5_pro_llm,  # Assigned Gemini-2.5-Pro for detailed drafting and long-context structured outputs
    tools=[],
    verbose=True,
    allow_delegation=False,
)

# Agent 6: Project Manager
project_manager = Agent(
    role="SBIR Project Manager",
    goal="Produce reusable, placeholder-driven Phase I post-award execution plans and SOPs.",
    backstory=(
        "You are an experienced DoD SBIR project manager. You create clear, week-by-week execution templates that cover kickoff, RACI/governance, tasking, milestones, deliverables, risks, communications, budget tracking, and closeout. "
        "All specifics (dates, names, orgs, budgets) must remain as instructional placeholders to keep the template reusable across projects."
    ),
    llm=claude_sonnet_4_llm,
    tools=[],
    verbose=True,
    allow_delegation=False,
)
