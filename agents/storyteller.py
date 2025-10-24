# 
from utils.call_model import CallModel
from langsmith import traceable

class StoryGenerator:
    def __init__(self):
        self.llm = CallModel()
        with open("prompts/storyteller_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    @traceable
    def generate(self, user_prompt: str) -> str:
        """
        Generate a story based on the user prompt.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        try:
            story = self.llm.invoke(messages)
        except Exception as e:
            raise RuntimeError(f"Story generation failed: {e}")
        return story
