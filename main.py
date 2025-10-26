# import streamlit as st
# from graph.workflow import run_story_workflow

# st.set_page_config(page_title="Somnia Chat", page_icon="🌙")

# st.title("🌙 Somnia Chat")
# st.write("Type a question or story prompt, and Somnia will reply with a bedtime story!")


# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []
# if "last_score" not in st.session_state:
#     st.session_state.last_score = 0
# if "last_iteration" not in st.session_state:
#     st.session_state.last_iteration = 0


# for msg in st.session_state.chat_history:
#     with st.chat_message(msg["role"]):
#         st.markdown(msg["content"])


# user_input = st.chat_input("Your message here...")

# if user_input:
    
#     st.session_state.chat_history.append({"role": "user", "content": user_input})
#     with st.chat_message("user"):
#         st.markdown(user_input)

#     story, feedback, score, iteration = run_story_workflow(user_input)
#     # text_to_speech(story)

    
#     st.session_state.chat_history.append({"role": "assistant", "content": story})
#     with st.chat_message("assistant"):
#         st.markdown(story)

#     print(score, iteration)

# # Display score + iteration in small font below chat
# # st.markdown(
# #     f"<p style='font-size:small;'>Score: {st.session_state.last_score} | Iterations: {st.session_state.last_iteration}</p>",
# #     unsafe_allow_html=True
# # )

import streamlit as st
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from graph.workflow import run_story_workflow
import threading

# -------------------------------
# FASTAPI SETUP
# -------------------------------
app = FastAPI(title="Somnia API", description="Story generation and feedback API")

class StoryRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_story(request: StoryRequest):
    """Generate a story via API."""
    story, feedback, score, iteration = run_story_workflow(request.prompt)
    return {
        "story": story,
        "feedback": feedback,
        "score": score,
        "iteration": iteration,
    }

# -------------------------------
# STREAMLIT FRONTEND
# -------------------------------
def run_streamlit():
    st.set_page_config(page_title="Somnia Chat", page_icon="🌙")

    st.title("🌙 Somnia Chat")
    st.write("Type a question or story prompt, and Somnia will reply with a bedtime story!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Your message here...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        story, feedback, score, iteration = run_story_workflow(user_input)

        st.session_state.chat_history.append({"role": "assistant", "content": story})
        with st.chat_message("assistant"):
            st.markdown(story)

        st.caption(f"Score: {score} | Iteration: {iteration}")

# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        print("🚀 Running FastAPI server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        print("🎨 Running Streamlit app...")
        run_streamlit()
