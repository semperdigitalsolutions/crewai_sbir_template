from crewai import Crew, Process
import re  # For simple score parsing
import os  # For file path handling

from agents import researcher, evaluator, ideator, synthesizer, documenter  # From agents.py
from tasks import research_task, eval_research_task, ideation_task, eval_ideas_task, synthesis_task, doc_task, final_eval_task  # From tasks.py

# Assemble the Crew
sbir_crew = Crew(
    agents=[researcher, evaluator, ideator, synthesizer, documenter],
    tasks=[research_task, eval_research_task, ideation_task, eval_ideas_task, synthesis_task, doc_task, final_eval_task],
    process=Process.sequential,  # Runs tasks in order
    verbose=True,  # Detailed logging for debugging
    memory=False  # Enables shared memory for better context retention
)

# Function to run the crew (with evaluation logic)
def run_sbir_crew(sbir_input: str):
    result = sbir_crew.kickoff(inputs={'sbir_topic': sbir_input})
    
    # Create outputs dir if not exists
    os.makedirs('outputs', exist_ok=True)
    
    # Save individual task outputs
    for task in sbir_crew.tasks:
        task_output = task.output.raw
        file_name = f"outputs/{task.description.replace(' ', '_').lower()[:50]}.md"  # e.g., research_task.md, truncate for safety
        with open(file_name, 'w') as f:
            f.write(task_output)
        print(f"Saved task output to {file_name}")
    
    # Save the final result
    with open('outputs/final_output.md', 'w') as f:
        f.write(str(result))
    print("Saved final output to outputs/final_output.md")
    
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