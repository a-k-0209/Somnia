from langchain_core.prompts import ChatPromptTemplate
from utils.call_model import CallModel

class StoryGenerator:
    def __init__(self):
        self.llm = CallModel().llm
        with open("prompts/storyteller_prompt.txt") as f:
            system_prompt = f.read()
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{initial_prompt}\n\nPrevious feedback (if any): {feedback}")
        ])

    def generate(self, state):
        chain = self.prompt_template | self.llm
        result = chain.invoke({
            "initial_prompt": state.initial_prompt,
            "feedback": getattr(state, "feedback", "No feedback yet.")
        })
        state.story_generated = result.content
        return state


# class StoryGenerator:
#     def __init__(self):
#         self.llm = CallModel().llm
#         with open("prompts/storyteller_prompt.txt") as f:
#             system_prompt = f.read()
#         self.prompt_template = ChatPromptTemplate.from_messages([
#             ("system", system_prompt),
#             ("human", "{initial_prompt}")
#         ])

#     def generate(self, state):
#         chain = self.prompt_template | self.llm
#         result = chain.invoke({"initial_prompt": state.initial_prompt})
#         state.story_generated = result.content
#         return state
