
from xai_sdk import Client
from xai_sdk.chat import user, system

class BaseAIClient:
  def chat(self, system_message, user_message):
    raise NotImplementedError()

class OpenAIClient(BaseAIClient):
    def __init__(self, api_key, model):
        self.api_key = settings.OPENAI_API_KEY
        self.model = model

    def chat(self, system_message,user_message, temperature=0.7):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature,
        )
        return response.choices[0].message['content']       

class GrokClient(BaseAIClient):
      def __init__(self, api_key, model):
        self.model = model
        self.api_key = settings.XAI_API_KEY

      def chat(self, system_message, user_message):
        client = Client(api_key=self.api_key)
        chat = client.chat.create(model=self.api_key)
        chat.append({"role": "system", "content": system_message})
        chat.append({"role": "user", "content": user_message})
        response_data = chat.get_response()
        return response_data