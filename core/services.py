import logging
from django.conf import settings

from .models import AIConfig
from .middleware import InputSanitization
from .ai_clients import OpenAIClient, GroqClient, GrokClient

logger = logging.getLogger('chatbot_logger')

class ChatSession:
  def __init__(self, system_message):
    self.system_message = system_message
    self.history = []

  def add_user(self, message):
    self.history.append({'role': 'user', 'content': message})
  def add_bot(self, message):
    self.history.append({'role': 'assistant', 'content': message})

  def get_past_messages(self):
      return [{'role': 'system', 'content': self.system_message}] + self.history


class ChatBotService:
  DEFAULT_SYSTEM_PROMPT = """Você é um assistente de vendas da Petlove, especializado em ajudar os usuários do e-commerce a encontrar e comprar produtos para seus animais de estimação. Seu objetivo é ser gentil, prestativo e eficiente em suas respostas, oferecendo uma experiência de compra personalizada."""
  
  def __init__(self):
    system_config = AIConfig.objects.filter(is_active=True).first()
    system_message = system_config.system if system_config else self.DEFAULT_SYSTEM_PROMPT
    
    self.session = ChatSession(system_message=system_message)
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

  def get_bot_response(self, user_message):
    user_message = InputSanitization.sanitize_input(user_message)
    self.session.add_user(user_message)
    messages = self.session.get_past_messages()
    bot_response = self._fallback_strategy(messages)

    self.session.add_bot(bot_response)
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

