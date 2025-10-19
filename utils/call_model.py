from langchain_groq import ChatGroq
from pydantic import SecretStr
import os

class CallModel():
    def __init__(self, model_name="llama-3.3-70b-versatile", temperature=0.7):
        # Get API key from environment variable
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.llm = ChatGroq(
            model=model_name, 
            temperature=temperature,
            api_key=SecretStr(api_key)
        )
