
from xai_sdk import Client
from xai_sdk.chat import user, system

class BaseAIClient:
  def chat(self, messages):
    raise NotImplementedError()

class OpenAIClient(BaseAIClient):
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key

    def chat(self, messages, temperature=0.7):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
        )
        return response.choices[0].message['content']       

class GrokClient(BaseAIClient):
      def __init__(self, api_key, model):
        self.model = model
        self.api_key = api_key
        self.client = Client(api_key=self.api_key)


      def chat(self, messages):
        chat = self.client.chat.create(model=self.model)
        for msg in messages:
            chat.append(msg)
        response_data = chat.get_response()
        return response_data