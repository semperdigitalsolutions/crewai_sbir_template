from crewai import Crew, Process
import re  # For simple score parsing

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
    
    # Basic post-processing: Parse evaluator scores from outputs (assumes Markdown with 'Overall Score: X/10')
    eval_outputs = [task.output.raw_output for task in sbir_crew.tasks if task.agent == evaluator]
    for eval_output in eval_outputs:
        score_match = re.search(r'Overall Score:\s*(\d+)/10', eval_output)
        if score_match:
            score = int(score_match.group(1))
            if score < 8:
                print(f"Warning: Low score ({score}/10) detected. Consider revisions based on suggestions in output.")
                # Optional: Add auto-rerun logic here later, e.g., re-kickoff specific tasks
    
    return result

# Example usage (comment out for now; we'll test later)
# if __name__ == "__main__":
#     topic = "Develop AI tools for climate monitoring."  # Or load from file
#     final_result = run_sbir_crew(topic)
#     print(final_result)

if __name__ == "__main__":
    topic = "Test SBIR Topic: AI for testing."  # Dummy input
    print(f"Simulating crew kickoff with input: {topic}")
    # final_result = run_sbir_crew(topic)  # Comment this out to avoid real run
    # print(final_result)
    print("Crew structure loaded successfully—no errors in agents/tasks.")