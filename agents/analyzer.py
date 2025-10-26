import json
from utils.call_model import CallModel
from langsmith import traceable

class Analyzer:
    @traceable
    def analyze(self, user_input: str, prev_name: str = None):
        """
        Analyzes user input for story intent, name changes, and unsafe content.
        Keeps previous name if no new one is specified.
        """
        system_prompt = (
            "You are Somnia’s Story Analyzer — an AI safety and intent detector for a children’s storytelling app.\n\n"
            "Your job is to read the user’s input and output a JSON object describing what to do next.\n"
            "You must carefully detect the following:\n"
            "1. If the user is asking for a new story (e.g., 'I want a story about a cat'),\n"
            "   or to continue an existing story (e.g., 'add a dragon').\n"
            "2. Extract the user's name if mentioned.\n"
            "3. Detect unsafe, violent, scary, or adult content — words like kill, death, blood, murder, die, ghost, gun, fight, poison, or any similar idea.\n"
            "4. If such content is detected, set intent to 'unsafe_content' and include a calm, kind message in 'safe_message', like:\n"
            "   'I'm sorry, I can’t include that, but I can make something magical instead!'\n"
            "5. Always return your answer as a valid JSON object only, nothing else.\n\n"
            "Return format:\n"
            "{\n"
            '  "intent": "new_story" | "continue" | "unsafe_content",\n'
            '  "name": string,\n'
            '  "reason": string,\n'
            '  "safe_message": string (only if intent == "unsafe_content")\n'
            "}"
        )



        full_prompt = f"{system_prompt}\n\nUser input: {user_input}\nPrevious name: {prev_name or 'None'}"

        llm = CallModel()
        response = llm.invoke(full_prompt)

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError:
            parsed = {
                "intent": "continue",
                "name": prev_name or "Unknown",
                "reason": "Parsing error",
                "safe_message": ""
            }

        if (not parsed.get("name") or parsed["name"].lower() in ["unknown", "none", "null"]) and prev_name:
            parsed["name"] = prev_name

        return parsed
