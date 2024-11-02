# apachelabs/client.py

import os
from mistralai import Mistral
from .config import MODEL_AGENT_MAP

class Apache:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Provide it as an argument or set MISTRAL_API_KEY in environment.")
        self.client = Mistral(api_key=self.api_key)
    
    def messages(self, model, max_tokens=1024, messages=None):
        if model not in MODEL_AGENT_MAP:
            raise ValueError(f"Unknown model: {model}")
        agent_id = MODEL_AGENT_MAP[model]
        
        response = self.client.agents.complete(
            agent_id=agent_id,
            messages=messages or [],
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
