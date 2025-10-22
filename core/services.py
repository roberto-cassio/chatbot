import logging
from django.conf import settings
from langchain.memory import ConversationBufferWindowMemory

from .models import AIConfig
from .middleware import InputSanitization
from .ai_clients import OpenAIClient, GroqClient, GrokClient
from langchain.schema import HumanMessage, AIMessage


logger = logging.getLogger('chatbot_logger')


class ChatBotService:
  DEFAULT_SYSTEM_PROMPT = """Você é um assistente de vendas da Petlove, especializado em ajudar os usuários do e-commerce a encontrar e comprar produtos para seus animais de estimação. Seu objetivo é ser gentil, prestativo e eficiente em suas respostas, oferecendo uma experiência de compra personalizada."""
  
  def __init__(self):
    system_config = AIConfig.objects.filter(is_active=True).first()
    self.system_message = system_config.system if system_config else self.DEFAULT_SYSTEM_PROMPT
    
    self.memory = ConversationBufferWindowMemory(k=5, return_messages=True)
    self.primary_client = OpenAIClient(
          api_key=settings.OPENAI_API_KEY,
          model=settings.OPENAI_MODEL
        )
    self.secondary_client = GroqClient(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL
        )
    self.tertiary_client = GrokClient(
            api_key=settings.XAI_API_KEY,
            model=settings.XAI_API_MODEL
        ) if settings.XAI_API_KEY else None
    self.last_provider = None

  def _build_messages(self):
    messages = [{'role': 'system', 'content': self.system_message}]
    chat_history = self.memory.load_memory_variables({})
    if 'history' in chat_history:
      for msg in chat_history['history']:
        if hasattr(msg, 'type'):
          role = 'user' if msg.type == 'human' else 'assistant'
          messages.append({'role': role, 'content': msg.content})
    return messages

  def get_bot_response(self, user_message):
    user_message = InputSanitization.sanitize_input(user_message)
    
    self.memory.save_context({'input': user_message}, {'output': ''})
    messages = self._build_messages()
    bot_response = self._fallback_strategy(messages)
    
    chat_history = self.memory.load_memory_variables({})
    if 'history' in chat_history and len(chat_history['history']) > 0:
      last_msg = chat_history['history'][-1]
      if hasattr(last_msg, 'type') and last_msg.type == 'ai':
        chat_history['history'][-1].content = bot_response
    
    return bot_response

  def _fallback_strategy(self, messages):
    try:
        response = self.primary_client.chat(messages)
        self.last_provider = 'openai'
        return response
    except Exception as e:
        print(f"[ChatBot] OpenAI failed: {e}")
        try:
            response = self.secondary_client.chat(messages)
            self.last_provider = 'groq'
            return response
        except Exception as e:
            print(f"[ChatBot] Groq failed: {e}")
            if self.tertiary_client:
                try:
                    response = self.tertiary_client.chat(messages)
                    self.last_provider = 'grok'
                    return response
                except Exception as e:
                    print(f"[ChatBot] Grok failed: {e}")
                    raise Exception("All AI providers failed")
            else:
                raise Exception("Primary and secondary providers failed, no tertiary configured")

  def serialize_history(self, history):
    serialized = []
    for msg in history:
        if hasattr(msg, "type"):
            role = "user" if msg.type == "human" else "assistant"
            serialized.append({"role": role, "content": msg.content})
    return serialized
  
  def deserialize_history(self, history):
    deserialized = []
    for msg in history:
        if msg["role"] == "user":
            deserialized.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            deserialized.append(AIMessage(content=msg["content"]))
    return deserialized