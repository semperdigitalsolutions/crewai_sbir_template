from crewai import Task
from agents import researcher, evaluator, ideator, synthesizer, documenter  # Import from agents.py

# Task 1: Research the SBIR Topic
research_task = Task(
    description=(
        "Research the provided SBIR topic: {sbir_topic}. "
        "Analyze the solicitation, key requirements, prior art, and feasibility. "
        "Use tools if needed. Output a structured report in Markdown."
    ),
    expected_output='A Markdown report with sections: Overview, Requirements, Prior Art, Feasibility.',
    agent=researcher
)

# Task 2: Evaluate the Research
eval_research_task = Task(
    description=(
        "Critique the research report for accuracy, completeness, bias, and SBIR fit. "
        "Score each on 1-10, provide overall score, and suggest improvements. "
        "If overall <8, note revisions needed."
    ),
    expected_output='A critique report with scores and suggestions in Markdown.',
    context=[research_task],  # Depends on research_task output
    agent=evaluator
)

# Task 3: Ideate Solutions
ideation_task = Task(
    description=(
        "Based on the research report and evaluation, brainstorm 3-5 innovative Phase 1 solutions. "
        "Rank by feasibility/novelty, outline experiments, and align with SBIR goals."
    ),
    expected_output='A list of 3-5 ideas with rankings and outlines in Markdown.',
    context=[research_task, eval_research_task],  # Builds on prior
    agent=ideator
)

# Task 4: Evaluate the Ideas
eval_ideas_task = Task(
    description=(
        "Critique the ideation output for innovation, feasibility, and compliance. "
        "Score each idea 1-10, suggest refinements."
    ),
    expected_output='Critique with scores and refinements in Markdown.',
    context=[ideation_task],
    agent=evaluator
)

# Task 5: Synthesize the Best Solution
synthesis_task = Task(
    description=(
        "Combine research, evaluations, and top ideas into a cohesive Phase 1 solution outline. "
        "Resolve conflicts and prioritize based on feedback."
    ),
    expected_output='A unified solution outline in Markdown.',
    context=[research_task, eval_research_task, ideation_task, eval_ideas_task],
    agent=synthesizer
)

# Task 6: Draft Documentation
doc_task = Task(
    description=(
        "Draft SBIR Phase 1 proposal sections based on the synthesized outline. "
        "Include abstract, technical approach, and basic budget/commercial plan. Keep concise."
    ),
    expected_output='Proposal draft in Markdown with sections.',
    context=[synthesis_task],
    agent=documenter
)

# Task 7: Final Evaluation
final_eval_task = Task(
    description=(
        "Perform a final critique of the full output for overall quality and SBIR readiness. "
        "Score 1-10 and suggest any last fixes."
    ),
    expected_output='Final critique and score in Markdown.',
    context=[doc_task],
    agent=evaluator
)