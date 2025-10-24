# import re
from utils.call_model import CallModel
from langsmith import traceable
import re

class Evaluator:
    def __init__(self):
        self.llm = CallModel()
        with open("prompts/evaluator_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    @traceable
    def evaluate(self, story_generated: str):
        """
        Evaluate a story and extract feedback and score from model output.
        Expected model output format:
        Feedback: <feedback text>
        Overall Score: <integer>
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": story_generated},
        ]
        try:
            response = self.llm.invoke(messages)
        except Exception as e:
            raise RuntimeError(f"Evaluation failed: {e}")

        content = str(response).strip()

        feedback_match = re.search(r"Feedback:\s*(.*)", content)
        score_match = re.search(r"Overall Score:\s*(\d+)", content)

        feedback = feedback_match.group(1).strip() if feedback_match else "No feedback provided."
        score = int(score_match.group(1)) if score_match else 0

        return feedback, score
