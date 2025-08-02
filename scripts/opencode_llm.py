import subprocess
from typing import Any, Dict, List, Optional
from langchain_core.language_models.llms import BaseLLM
from langchain_core.outputs import Generation, LLMResult

class OpenCodeLLM(BaseLLM):
    """Custom LLM wrapper for OpenCode.ai CLI."""

    model: str  # e.g., 'claude-3.5-sonnet' or 'gpt-4o'

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> LLMResult:
        generations = []
        for prompt in prompts:
            # Run OpenCode CLI non-interactively
            cmd = ['opencode', 'run', prompt, '--model', self.model]
            if kwargs.get('json_output'):  # Optional for structured responses
                cmd.append('--json')
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                output = result.stdout.strip()
            except subprocess.CalledProcessError as e:
                raise ValueError(f"OpenCode error: {e.stderr}")

            # Format as LangChain expects
            generations.append([Generation(text=output)])
        return LLMResult(generations=generations)

    @property
    def _llm_type(self) -> str:
        return "opencode_custom"

    def _identifying_params(self) -> Dict[str, Any]:
        return {"model": self.model}

# Usage example (for later testing):
# claude_llm = OpenCodeLLM(model='claude-3.5-sonnet')
# response = claude_llm.invoke("Test prompt")