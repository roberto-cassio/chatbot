from openai import OpenAI

class BaseAIClient:
    def chat(self, messages):
        raise NotImplementedError()

class OpenAIClient(BaseAIClient):
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def chat(self, messages, temperature=0.7):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content

class GroqClient(BaseAIClient):
    def __init__(self, api_key, model):
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )

    def chat(self, messages, temperature=0.7):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content

class GrokClient(BaseAIClient):
    def __init__(self, api_key, model):
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.x.ai/v1"
        )

    def chat(self, messages, temperature=0.7):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message.content