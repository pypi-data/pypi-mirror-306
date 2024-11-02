import os
from mistralai import Mistral


class Apache:
    model_map = {
        "apachelm-v3": "ag:332133fc:20241102:apachelm-v3:de8afc4d",
        "apachelm-v4": "ag:332133fc:20241102:apachelm-v4:18ea79ed",
        "apachelm-v3.5": "ag:332133fc:20241102:apachelm-v3-5:1722c5ec",
    }

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("APACHE_API_KEY")
        self.client = Mistral(api_key=self.api_key)

    def messages(self):
        return MessageBuilder(self.client)


class MessageBuilder:

    def __init__(self, client):
        self.client = client

    def create(self, model, max_tokens, messages):
        agent_id = Apache.model_map.get(model)
        if not agent_id:
            raise ValueError(f"Model '{model}' not found in model_map.")

        chat_response = self.client.agents.complete(
            agent_id=agent_id,
            messages=messages,
        )
        return Message(chat_response.choices[0].message.content)


class Message:

    def __init__(self, content):
        self.content = content
