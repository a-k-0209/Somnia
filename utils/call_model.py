

import os
from langchain_groq import ChatGroq
from langsmith import traceable




class CallModel:
    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.model_name = model_name
        

        self.llm = ChatGroq(
            model=self.model_name,
            api_key=self.api_key,
            max_tokens=3000, 
        )


    @traceable
    def invoke(self, messages):
        """
        messages: list of dicts like [{"role": "system", "content": ...}, {"role": "user", "content": ...}]
        Returns: the model's string response.
        """
        response = self.llm.invoke(messages)
        return response.content 


