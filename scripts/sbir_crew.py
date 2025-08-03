from crewai import Crew, Process
import re  # For simple score parsing
import os  # For file path handling

from agents import researcher, secondary_researcher, evaluator, ideator, consensus_agent, documenter  # From agents.py
from tasks import research_task, secondary_research_task, synthesis_task, eval_research_task, ideation_task, eval_ideas_task, doc_task, compliance_check_task, final_eval_task  # From tasks.py

# Assemble the Crew with the new parallel research and consensus process
sbir_crew = Crew(
    agents=[researcher, secondary_researcher, consensus_agent, evaluator, ideator, documenter],
    tasks=[research_task, secondary_research_task, synthesis_task, eval_research_task, ideation_task, eval_ideas_task, doc_task, compliance_check_task, final_eval_task],
    process=Process.sequential,  # Runs tasks in order
    verbose=True,  # Detailed logging for debugging
    memory=False  # Enables shared memory for better context retention
)

# Function to run the crew (with evaluation logic)
def run_sbir_crew(sbir_input: str):
    result = sbir_crew.kickoff(inputs={'sbir_topic': sbir_input})
    
    # Create outputs dir if not exists
    os.makedirs('outputs', exist_ok=True)
    
    # Define task labels for better file naming
    task_labels = {
        research_task: "sbir_research_overview.md",
        secondary_research_task: "secondary_sbir_research.md",
        synthesis_task: "consolidated_research.md",
        eval_research_task: "research_critique.md",
        ideation_task: "proposed_ideas_and_ranks.md",
        eval_ideas_task: "ideas_critique.md",
        doc_task: "proposal_draft_sections.md",
        compliance_check_task: "compliance_report.md",
        final_eval_task: "proposal_critique_and_scores.md"
    }
    
    # Save individual task outputs with labeled names
    for task in sbir_crew.tasks:
        task_output = task.output.raw
        default_name = task.description.replace(' ', '_').lower()[:50] + ".md"
        file_name = f"outputs/{task_labels.get(task, default_name)}"
        with open(file_name, 'w') as f:
            f.write(task_output)
        print(f"Saved task output to {file_name}")
        
        if task == doc_task:  # Split draft into volume files for easier template integration
            volumes = task_output.split('## Volume ')  # Assuming Markdown headings
            for i, vol in enumerate(volumes[1:], 1):  # Skip first empty split
                vol_file = f"outputs/volume_{i}.md"
                with open(vol_file, 'w') as f:
                    f.write('## Volume ' + vol)
                print(f"Saved {vol_file}")
    
    # Save the final result
    with open('outputs/final_output.md', 'w') as f:
        f.write(str(result))
    print("Saved final output to outputs/final_output.md")
    
    # Compile writer_handoff.md
    handoff_content = f"# SBIR Writer Handoff for {sbir_input[:50]}\n\n"
    handoff_content += "## Mapping to Template:\n"
    handoff_content += "- Abstract from doc_task -> Volume 1: Technical Abstract\n"
    handoff_content += "- Technical Approach from doc_task -> Volume 2: Phase I Technical Objectives and SOW\n"
    handoff_content += "- Commercial Potential -> Volume 2: Commercialization Strategy\n"
    handoff_content += "- Research from synthesis_task -> Volume 2: Related Work\n\n"
    handoff_content += f"## Draft Sections:\n{doc_task.output.raw}\n\n"
    handoff_content += f"## Ideas and Ranks:\n{ideation_task.output.raw[:1000]}...\n"  # Truncate for preview
    handoff_content += f"## Compliance Notes:\n{compliance_check_task.output.raw}\n"
    with open('outputs/writer_handoff.md', 'w') as f:
        f.write(handoff_content)
    print("Saved writer_handoff.md")
    
    # Compile post_win_approach_overview.md
    post_win_content = f"# Post-Win Approach Overview for {sbir_input[:50]}\n\n"
    post_win_content += "## High-Level Plan:\n" + ideation_task.output.raw[:500] + "...\n\n"
    post_win_content += "## Risks & Mitigations:\n" + eval_ideas_task.output.raw[:500] + "...\n\n"
    post_win_content += "## Resource Needs:\nFrom doc_task (e.g., labor, facilities).\n\n"
    post_win_content += "## Discussion Points:\n- Bandwidth for tasks?\n- IP concerns?\n- Phase II paths?\n"
    with open('outputs/post_win_approach_overview.md', 'w') as f:
        f.write(post_win_content)
    print("Saved post_win_approach_overview.md")
    
    # Basic post-processing: Parse evaluator scores from outputs (assumes Markdown with 'Overall Score: X/10')
    eval_outputs = [task.output.raw for task in sbir_crew.tasks if task.agent == evaluator]
    for i, eval_output in enumerate(eval_outputs, 1):
        score_match = re.search(r'Overall Score:\s*(\d+)/10', eval_output)
        if score_match:
            score = int(score_match.group(1))
            if score < 8:
                print(f"Warning: Low score ({score}/10) detected in eval_output_{i}.md. Consider revisions based on suggestions in output.")
                # Optional: Add auto-rerun logic here later, e.g., re-kickoff specific tasks
    
    return result

if __name__ == "__main__":
    # Load the SBIR topic from the input file (for SBIR 12148)
    input_file = os.path.join('inputs', 'topic.txt')
    with open(input_file, 'r') as f:
        topic = f.read().strip()
    
    print(f"Running crew with SBIR topic from file: {topic[:100]}...")  # Preview first 100 chars
    
    final_result = run_sbir_crew(topic)
    print(final_result)