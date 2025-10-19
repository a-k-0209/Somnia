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


    # def call_model(self, max_tokens=3000, temperature=0.1):
    #     api_key = "AIzaSyCUPjby__GDwPYklqWc1wei3FbAXZsOwGA"  # Or use os.getenv("GOOGLE_API_KEY")
    #     llm = ChatGoogleGenerativeAI(
    #         model="gemini-2.5-flash",
    #         google_api_key=api_key,
    #         temperature=temperature,
    #         max_output_tokens=max_tokens,
    #     )
    #     # resp = llm.invoke(prompt)
    #     return llm
    # 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