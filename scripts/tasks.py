from crewai import Task
from agents import (
    researcher,
    secondary_researcher,
    evaluator,
    ideator,
    consensus_agent,
    documenter,
)

# Task 1: Research the SBIR Topic
research_task = Task(
    description=(
        "Research the provided SBIR topic: {sbir_topic}. "
        "Analyze the 2025 solicitation via official sources (use web_search or browse_page for DSIP/BAAs). Focus on key requirements (e.g., eligibility, work minimums), prior art (including DoD-funded projects), and Phase 1 feasibility (e.g., unclassified studies, risks). "
        "Use tools for accurate, current info. Output a structured report in Markdown, limited to 800-1200 words."
    ),
    expected_output="A Markdown report with sections: Overview (Problem Significance), Requirements (Eligibility and Key Criteria), Prior Art (Related Work), Feasibility (Gaps and Risks). Include citations from tools.",
    agent=researcher,
)

# Task 1b: Secondary Research Task
secondary_research_task = Task(
    description=(
        "Perform a second, independent research pass on the same SBIR topic: {sbir_topic}, building on the initial report. "
        "Focus on missed details (e.g., 2025 DoD updates, dual-use potential) or alternative perspectives (e.g., industry vs. DoD views). "
        "Use tools like web_search for fresh sources. Output a structured report in Markdown, limited to 600-900 words."
    ),
    expected_output="A complementary Markdown report with sections: Overview (Alternative Angles), Requirements (Additional Criteria), Prior Art (Overlooked Work), Feasibility (New Gaps/Risks). Include citations.",
    context=[research_task],  # Add this for reference without copying
    agent=secondary_researcher,
)

# Task 2: Create Consensus from Research
synthesis_task = Task(
    description=(
        "Take the two research reports and merge them into a single, cohesive, and superior summary. "
        "Identify the most critical points from each (e.g., key requirements, prior art gaps), resolve discrepancies using SBIR priorities like feasibility and compliance. "
        "Incorporate 2025 DoD updates and tool-cited sources. Produce a unified, comprehensive report limited to 1000-1500 words. "
        "This will be the single source of truth for all subsequent tasks."
    ),
    expected_output="A single, unified Markdown report with sections: Overview, Requirements, Prior Art, Feasibility, Resolved Discrepancies. Include citations.",
    context=[research_task, secondary_research_task],
    agent=consensus_agent,
)

# Task 3: Evaluate the Consolidated Research
eval_research_task = Task(
    description=(
        "Critique the consolidated research report for accuracy, completeness, bias, SBIR fit, innovation, and commercialization potential. "
        "Score each on 1-10, provide overall score, and suggest targeted improvements (e.g., for Phase 1 feasibility). "
        "If overall <8, note specific revisions needed, prioritizing DoD compliance."
    ),
    expected_output="A critique report in Markdown with sections: Scores (by Criterion), Overall Score, Suggestions. Limit to 400-600 words.",
    context=[synthesis_task],  # Depends on the new consensus report
    agent=evaluator,
)

# Task 4: Ideate Solutions
ideation_task = Task(
    description=(
        "Based on the consolidated research report and its evaluation, brainstorm 3-5 innovative Phase 1 solutions. "
        "Rank by feasibility/novelty/impact, outline experiments (e.g., with synthetic data, 6-9 month scoping), risks/mitigations, and align with SBIR goals like dual-use and DoD compliance. "
        "Use tools if needed for tech trends. Limit to 800-1200 words."
    ),
    expected_output="Output full, untruncated content. A Markdown list of 3-5 ideas with rankings, outlines (including experiments/risks), and SBIR alignment.",
    context=[synthesis_task, eval_research_task],  # Builds on the consensus report
    agent=ideator,
)

# Task 5: Evaluate the Ideas
eval_ideas_task = Task(
    description=(
        "Critique the ideation output for innovation, feasibility, compliance, and commercialization. "
        "Score each idea 1-10 across criteria, suggest refinements (e.g., Phase 1 scoping adjustments), and note if revisions are needed for SBIR fit."
    ),
    expected_output="A Markdown critique with sections: Idea Scores (by Criterion), Refinements. Limit to 300-500 words per idea.",
    context=[ideation_task],
    agent=evaluator,
)

# Task 6: Draft Documentation
doc_task = Task(
    description=(
        "Draft SBIR Phase 1 proposal sections based on the ideation output, evaluation, and DoD template structure. "
        "Choose the best idea (highest-scored), and draft: Volume 1 (Cover Sheet with abstract <3000 chars, benefits); "
        "Volume 2 (Technical Volume: Problem Identification, Objectives, SOW with tasks/milestones/deliverables, Related Work, Future R&D Relationship, Commercialization Strategy, Key Personnel, Foreign Citizens table, Facilities/Equipment, Subcontractors); "
        "Volume 3 (Cost Volume: Justified budget, travel, labor hours); Volume 4-7 (placeholders for CCR, Supporting Docs, FWA Training, Foreign Affiliations). "
        "Align with Phase 1 constraints (3 months, $75K max) and include dual-use strategy. Keep concise."
    ),
    expected_output="A Markdown proposal draft with sections labeled by Volume (e.g., ## Volume 1: Cover Sheet), including placeholders for non-draftable items like forms.",
    context=[ideation_task, eval_ideas_task],  # Depends on the generated ideas
    agent=documenter,
)

# New Task: Compliance Check (add after doc_task; use evaluator)
compliance_check_task = Task(
    description=(
        "Review the proposal draft for compliance with SBIR template elements (e.g., foreign citizens disclosure, data rights assertions, joint venture eligibility, ITAR/EAR restrictions). "
        "Flag issues, suggest fixes (e.g., insert table for assertions), and ensure alignment with DSIP requirements like Q&A deadlines."
    ),
    expected_output="A Markdown compliance report with sections: Flagged Issues, Suggested Fixes, Overall Compliance Score (1-10). Limit to 300-500 words.",
    context=[doc_task],
    agent=evaluator,
)

# Task 7: Final Evaluation
final_eval_task = Task(
    description=(
        "Perform a final critique of the full proposal draft for overall quality, SBIR readiness, and criteria like accuracy, innovation, feasibility, commercialization. "
        "Score 1-10 overall and per criterion, suggest last fixes (e.g., budget inconsistencies, template alignment with volumes like SOW or data rights). "
        "Reference 2025 DoD guidelines and the provided template structure."
    ),
    expected_output="A Markdown final critique with sections: Scores (by Criterion), Overall Score, Last Fixes. Limit to 500-800 words.",
    context=[doc_task, compliance_check_task],
    agent=evaluator,
)