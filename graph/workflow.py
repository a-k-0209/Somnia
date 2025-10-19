from langgraph.graph import StateGraph, END
from agents.storyteller import StoryGenerator
from agents.evaluator import Evaluator
from pydantic import BaseModel

class StoryState(BaseModel):
    initial_prompt: str
    story_generated: str = ""
    evaluation: str = ""
    feedback: str = ""
    score: int = 0
    iteration: int = 0  #loop





story_gen = StoryGenerator()
evaluator = Evaluator()

def story_node(state: StoryState):
    return story_gen.generate(state)

# def evaluation_node(state: StoryState):
#     return evaluator.evaluate(state)
def evaluation_node(state: StoryState):
    state = evaluator.evaluate(state)
    lines = state.evaluation.splitlines()
    for line in lines:
        if line.startswith("Feedback:"):
            state.feedback = line.replace("Feedback:", "").strip()
            break
    return state


from langgraph.graph import StateGraph, END

def build_graph():
    graph = StateGraph(StoryState)

    graph.add_node("generate_story", story_node)
    graph.add_node("evaluate_story", evaluation_node)

    graph.add_edge("generate_story", "evaluate_story")

    def continue_or_end(state: StoryState):
        state.iteration += 1
        print(f"\n🔁 Iteration {state.iteration}: Score = {state.score}")
        if state.iteration < 5 and state.score < 7:
            print("🧠 Re-generating story with feedback...\n")
            return "generate_story"
        else:
            print(f"✅ Finished after {state.iteration} iterations (Score: {state.score})\n")
            return END

    graph.add_conditional_edges(
        "evaluate_story",
        continue_or_end,
        {
            "generate_story": "generate_story",
            END: END
        }
    )

    graph.set_entry_point("generate_story")
    return graph.compile()


