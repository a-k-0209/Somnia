from langchain_core.prompts import ChatPromptTemplate
from utils.call_model import CallModel
import re

class Evaluator:
    def __init__(self):
        self.llm = CallModel().llm
        with open("prompts/evaluator_prompt.txt") as f:
            system_prompt = f.read()
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{story_generated}")
        ])

    def evaluate(self, state):
        chain = self.prompt_template | self.llm
        result = chain.invoke({"story_generated": state.story_generated})
        state.evaluation = result.content
        match = re.search(r"(\d+(?:\.\d+)?)", state.evaluation)
        if match:
            state.score = int(match.group(1))
        else:
            state.score = 0
        return state
