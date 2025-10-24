from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from agents.storyteller import StoryGenerator
from agents.evaluator import Evaluator
from agents.analyzer import Analyzer
import re
from langsmith import traceable
from agents.voice import voice_agent



# --------------------- State Schema --------------------- #
class State(TypedDict):
    prompt: str
    iteration: int
    story_generated: str
    feedback: str
    score: int
    user_name: str
    continue_story: bool
    current_name: str = ""
    current_story_context: list = []


# --------------------- Initialize Agents --------------------- #
story_gen = StoryGenerator()
evaluator = Evaluator()
checkpointer = MemorySaver()
analyzer = Analyzer()


# --------------------- Node Functions --------------------- #
@traceable
def story_gen_fn(state: State) -> State:
    """Generate or continue a story based on user input."""
    prompt = state["prompt"]
    name = state["user_name"]
    continue_story = state["continue_story"]

    
    if continue_story and state["story_generated"]:
        full_prompt = (
            f"{name} wants to continue the previous story. "
            f"Add new elements based on: {prompt}\n\nPrevious story:\n{state['story_generated']}"
        )
    else:
        full_prompt = f"{name} wants a new story based on: {prompt}"

    story = story_gen.generate(full_prompt)
    state["iteration"] += 1
    state["story_generated"] = story
    return state

@traceable
def evaluator_fn(state: State) -> State:
    """Evaluate the generated story."""
    feedback, score = evaluator.evaluate(state["story_generated"])
    state["iteration"] += 1
    state["feedback"] = feedback
    state["score"] = score
    return state

@traceable
def decision_fn(state: State) -> Literal["story_gen", "end"]:
    """Decide whether to refine or end based on score."""
    if state["score"] < 7 and state["iteration"] < 5:
        return "story_gen"
    return "end"

@traceable
def memory_update_fn(state: State) -> State:
    """Analyze input for intent, handle unsafe content, and update memory state."""
    user_input = state["prompt"]
    current_name = state.get("user_name", "")
    context = state.get("current_story_context", [])

   
    analysis = analyzer.analyze(user_input, current_name)

   
    if analysis["intent"] == "unsafe_content":
        state.update({
            "story_generated": "",
            "feedback": analysis["safe_message"],
            "score": 0,
            "user_name": analysis["name"],  
            "continue_story": False,
        })
        
        state["current_story_context"] = []
        return state

  
    intent_type = analysis["intent"]
    new_name = analysis["name"] or current_name
    state["user_name"] = new_name

    if intent_type == "new_story":
       
        state["current_story_context"] = [user_input]
        state["continue_story"] = False
    elif intent_type == "continue":
        context.append(user_input)
        state["current_story_context"] = context
        state["continue_story"] = True

    return state

@traceable
def text_to_speech(state: State) -> State:
    story_text = state.get("story_generated", "")
    if story_text:
        output = voice_agent.text_to_speech(story_text)
        state["audio_path"] = output
    else:
        state["audio_path"] = ""
    return state


# --------------------- Workflow Graph --------------------- #
graph = StateGraph(State)

graph.add_node("story_gen", story_gen_fn)
graph.add_node("evaluator", evaluator_fn)
graph.add_node("decision", decision_fn)
graph.add_node("memory_update", memory_update_fn)
graph.add_node("voice", text_to_speech)


graph.add_edge(START, "story_gen")
graph.add_edge("story_gen", "evaluator")
graph.add_edge("evaluator", "memory_update")
graph.add_edge("memory_update", "voice")
graph.add_conditional_edges(
    "memory_update",
    decision_fn,
    {
        "story_gen": "story_gen",
        "end": "voice",
    },
)
graph.add_edge("voice", END)
compiled_graph = graph.compile(checkpointer=checkpointer)


# --------------------- Runner --------------------- #

session_state = {
        "current_name": "",
        "context": [],
    }

def run_story_workflow(user_input: str, thread_id: str = "default_session"):
    """Main workflow entry point with per-session short-term memory."""
    global session_state

    
    if not session_state.get("current_name"):
        session_state["current_name"] = ""

    
    a = analyzer.analyze(user_input, session_state["current_name"])
    user_name = a.get("name", session_state["current_name"])
    intent_type = a.get("intent", "continue")

    if intent_type == "unsafe_content":
        session_state["context"] = []
        return (
            story_gen.generate(user_input),
            a.get("safe_message", "Let's try a fun, safe story instead!"),
            0,
            0
        )

    
    if intent_type == "new_story":
        session_state["context"] = [user_input]
    elif intent_type == "continue":
        session_state["context"].append(user_input)


    MAX_MEMORY_TURNS = 6
    if len(session_state["context"]) > MAX_MEMORY_TURNS:
        session_state["context"] = session_state["context"][-MAX_MEMORY_TURNS:]

    combined_prompt = " ".join(session_state["context"]) if session_state["context"] else user_input

    initial_state: State = {
        "prompt": combined_prompt,
        "iteration": 0,
        "story_generated": "",
        "feedback": "",
        "score": 0,
        "user_name": user_name or "Unknown",
        "continue_story": (intent_type == "continue"),
        "current_name": session_state.get("current_name", ""),
        "current_story_context": session_state.get("context", []),        
    }

    result = compiled_graph.invoke(
        initial_state,
        config={
            "configurable": {
                "thread_id": initial_state["user_name"] or thread_id,
                "checkpoint_ns": "story_memory",
            }
        },
    )

    return (
        result["story_generated"],
        result["feedback"],
        result["score"],
        result["iteration"],
    )
