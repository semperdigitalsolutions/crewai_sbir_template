from crewai import Task
from agents import (
    researcher,
    secondary_researcher,
    evaluator,
    ideator,
    consensus_agent,
    documenter,
    project_manager,
)

# Task 1: Research the SBIR Topic
research_task = Task(
    description=(
        "Research the provided SBIR topic: {sbir_topic}. "
        "Use your web search or scrape tool to locate and analyze the LIVE DoD/DSIP solicitation page for this topic and any published amendments/updates based on the Topic Number (if present). "
        "Verify dates (release, open, close), eligibility, work percentage minimums, ITAR/EAR restrictions, and template/volume requirements from official sources. "
        "Corroborate with SBIR.gov and Service-specific portals (e.g., afsbirsttr.us) as secondary references. "
        "Focus on key requirements (e.g., eligibility, work minimums), prior art (including DoD-funded projects), and Phase 1 feasibility (unclassified studies, risks). "
        "Include citations to the DSIP/DoD page(s) and amendments. Record retrieval date/time (local). Output a structured report in Markdown, limited to 800-1200 words."
    ),
    expected_output=(
        "A Markdown report with sections: Overview (Problem Significance), Requirements (Eligibility and Key Criteria), Prior Art (Related Work), Feasibility (Gaps and Risks), Live Sources. "
        "The Live Sources section MUST include: (1) the official DSIP/DoD solicitation link, (2) a list of amendments/updates (with titles/dates if available), and (3) Retrieval Timestamp: [LOCAL DATE & TIME]. Include citations from tools."
    ),
    agent=researcher,
)

# Task 1b: Secondary Research Task
secondary_research_task = Task(
    description=(
        "Perform a second, independent research pass on the same SBIR topic: {sbir_topic}, building on the initial report. "
        "Focus on missed details (e.g., 2025 DoD updates, dual-use potential) or alternative perspectives (e.g., industry vs. DoD views). "
        "Use your web search or scrape tool for fresh sources. Output a structured report in Markdown, limited to 600-900 words."
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
        "Based on the consolidated research report and its evaluation, brainstorm 5-6 innovative Phase 1 solutions. "
        "Rank by feasibility/novelty/impact, outline experiments (e.g., with synthetic data, 6-9 month scoping), risks/mitigations, and align with SBIR goals like dual-use and DoD compliance. "
        "Quantify risks numerically (1-5 scale) and include specific, measurable metrics in the proposed experiments. "
        "Use tools if needed for tech trends. Limit to 1000-1500 words."
    ),
    expected_output="Output full, untruncated content. A Markdown list of 5-6 ideas with rankings, outlines (including experiments/risks), and SBIR alignment.",
    context=[synthesis_task, eval_research_task],  # Builds on the consensus report
    agent=ideator,
)

# Task 5: Evaluate the Ideas
eval_ideas_task = Task(
    description=(
        "Critique the ideation output for innovation, feasibility, compliance, and commercialization. "
        "Score each idea 1-10 across criteria, suggest refinements (e.g., Phase 1 scoping adjustments), and note if revisions are needed for SBIR fit."
    ),
    expected_output="A Markdown critique with sections: Idea Scores (by Criterion), Refinements. Limit to 400-600 words per idea and total to 2000-3000 words.",
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
        "Align with Phase 1 constraints (6 months, $150K max) and include dual-use strategy. Keep concise."
        " Within Volume 2, include sample tables for Data Rights (DFARS) and ITAR/EAR compliance."
        " In the Commercialization Strategy section, add a competitive landscape analysis and potential pricing strategies."
        " Instructional Placeholder Rule: When you must include company-specific information (like personnel bios, past projects, or cost figures), you are forbidden from inventing details. Instead, you MUST generate a descriptive, instructional placeholder in brackets. This placeholder should explain what information is needed and why it's important."
        " Examples: "
        " • Instead of inventing a PI name, write: [INSERT Principal Investigator Name and a 3-4 sentence bio. The bio MUST highlight experience directly relevant to AI, simulation, or government contracting to build credibility.] "
        " • Instead of inventing a past project, write: [INSERT a description of a relevant past project. Include the Client (e.g., DoD, commercial), the dollar value, and the outcome. This is needed to prove past performance.] "
        " • Instead of inventing a cost, write: [CALCULATE and INSERT Direct Labor cost based on the SOW hours and the company's blended hourly rate.] "
        " For Volume 3: Cost Volume, generate a 'live' worksheet table of line items that uses bracketed instructional placeholders for values and formulas (no fabricated numbers). "
        " Cost Volume table examples: "
        " • Direct Labor: [SUM OF ALL PERSONNEL HOURS x BLENDED RATE] "
        " • Overhead: [DIRECT LABOR x COMPANY OVERHEAD RATE] "
        " • Total Proposed Cost: [SUM OF ALL ABOVE LINES + FEE] "
        " Also, generate full drafts for the top 3-4 highest-scoring ideas when available. For each selected idea, create a dedicated section starting with '### IDEA: <Idea Title>' that contains a complete set of volumes (## Volume 1 .. ## Volume 7) following the same rules above."
    ),
    expected_output="A Markdown proposal draft containing either a single idea or multiple (top 3-4) idea sections. For multiple, each section must start with '### IDEA: <Idea Title>' and include complete volumes labeled by '## Volume X'. Include placeholders for non-draftable items and a Volume 3 Cost Volume table with bracketed placeholder formulas (no invented values).",
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

# Task 8: Generate Post-Win Execution Template (SOP)
generate_project_plan_task = Task(
    description=(
        "Create a detailed, reusable Phase I execution plan template (Standard Operating Procedure). "
        "This MUST be a generic template: do not invent dates, names, organizations, or dollar amounts. "
        "Use bracketed instructional placeholders for all specifics, e.g., [Week X], [Start Date], [End Date], [PI Name], [Project Manager Name], [Government TPOC], [Task 1 Budget $], [Deliverable Name], [Milestone Acceptance Criteria]. "
        "Include the following sections in Markdown: "
        " 1) Overview & Assumptions (Phase I duration as [N Weeks], total budget as [TOTAL BUDGET $], period of performance as [POP Start]–[POP End]). "
        " 2) Governance & RACI (roles: [PI], [PM], [Tech Lead], [Contracts], [Gov TPOC], with a RACI table using placeholders). "
        " 3) Milestones & Deliverables (milestones with [Target Week], [Owner], [Acceptance Criteria]; deliverables with [Due Week], [Format], [Recipient]). "
        " 4) Week-by-Week Plan (Weeks 1–[N]: for each week include Objectives, Tasks, Dependencies, Exit Criteria, Artifacts, and a [Planned vs. Actual] status line). "
        " 5) Risk Register & Mitigations (ID, Description, Impact, Probability, Mitigation, Owner, Trigger; all values as placeholders). "
        " 6) Communications Cadence (Weekly Standup [Day/Time], Biweekly Gov Sync [Day/Time], Email templates, Decision logs). "
        " 7) Budget Tracking Template (line items: [Direct Labor Hours/Rate], [Overhead %], [Materials $], [Travel $], [Fee %]; formulas as bracketed placeholders, no numbers). "
        " 8) Compliance & Documentation (ITAR/EAR checks, data rights assertions, reports schedule) as placeholders. "
        " 9) Closeout Checklist (Final Report, Invention Disclosure, Property, Invoices, Lessons Learned) with placeholder owners/dates. "
        "Instructional Placeholder Rule applies: never fabricate; always use descriptive placeholders explaining what is needed and why."
    ),
    expected_output=(
        "A Markdown SOP template with the sections above. It must be fully generic and reusable, using bracketed placeholders for all dates, names, organizations, and budget values. "
        "Include a Week-by-Week Plan scaffold labeled [Week 1] through [Week N], and a Budget Tracking table with placeholder formulas (e.g., [SUM OF ALL PERSONNEL HOURS x BLENDED RATE])."
    ),
    agent=project_manager,
)

# Task 9: Evaluate the Project Plan
evaluate_project_plan_task = Task(
    description=(
        "Critically review the project plan template produced by the Project Manager. "
        "Assess for realism, completeness, and practicality for a standard SBIR Phase I project. "
        "Provide a score (1-10) and actionable, concrete suggestions for improvement."
    ),
    expected_output=(
        "A Markdown critique including: Overall Score (1-10), Strengths, Gaps/Concerns, and Actionable Suggestions grouped by section (e.g., Governance, Milestones, Week-by-Week, Budget Tracking). Limit to 400-700 words."
    ),
    context=[generate_project_plan_task],
    agent=evaluator,
)

# Task 10: Revise the Project Plan
revise_project_plan_task = Task(
    description=(
        "Take the original project plan template and the evaluator's critique, and produce a final, improved version. "
        "Address each actionable suggestion while preserving the generic, placeholder-driven nature (no real names/dates/budgets). "
        "Ensure the template is robust, realistic, and ready for reuse across Phase I projects."
    ),
    expected_output=(
        "A refined Markdown SOP template that incorporates the evaluator's feedback. Maintain instructional placeholders (e.g., [Week X], [Owner], [TOTAL BUDGET $]) and keep all formulas as bracketed placeholders."
    ),
    context=[generate_project_plan_task, evaluate_project_plan_task],
    agent=project_manager,
)