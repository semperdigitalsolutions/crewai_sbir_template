import subprocess
from typing import Callable

def create_opencode_llm(model: str) -> Callable[[str], str]:
    def call(prompt: str) -> str:
        cmd = ['opencode', 'run', prompt, '--model', model]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValueError(f"OpenCode error: {e.stderr}")
        return output
    return call

# Multiple examples for future reference (commented out; uncomment to test):
# claude_call = create_opencode_llm('claude-3.5-sonnet')  # For subscribed Claude via OpenCode
# print(claude_call("Test prompt for Claude"))

# gpt_call = create_opencode_llm('gpt-4o')  # For subscribed GPT via OpenCode
# print(gpt_call("Test prompt for GPT"))

# gemini_call = create_opencode_llm('gemini-1.5-pro')  # For subscribed Gemini via OpenCode
# print(gemini_call("Test prompt for Gemini"))

# free_deepseek_call = create_opencode_llm('openrouter/deepseek/deepseek-chat-v3-0324:free')  # Free OpenRouter model via OpenCode
# print(free_deepseek_call("Test prompt for free DeepSeek"))

# free_qwen_call = create_opencode_llm('openrouter/qwen/qwen3-coder:free')  # Another free OpenRouter model
# print(free_qwen_call("Test prompt for free Qwen Coder"))