from django.conf import settings
from .middleware import InputSanitization
from .ai_clients import OpenAIClient, GrokClient

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
  system = """Você é um assistente de vendas da Petlove, especializado em ajudar os usuários do e-commerce a encontrar e comprar produtos para seus animais de estimação. Seu objetivo é ser gentil, prestativo e eficiente em suas respostas, oferecendo uma experiência de compra personalizada.
                  Mantenha um tom de conversa amigável, mas sem ser informal demais. Evite jargões ou gírias, mas também não seja excessivamente formal. Sempre que possível, forneça alternativas e opções claras para ajudar os usuários a tomar decisões mais rápidas e satisfatórias.
                  Você deve priorizar a clareza, objetividade e empatia. Seu foco é:
                  Empatia: Demonstrar compreensão e preocupação com o que o cliente está buscando para o seu pet.
                  Eficiência: Direcionar o usuário rapidamente para as soluções que ele precisa, evitando respostas longas e complexas.
                  Proatividade: Antecipar as necessidades do cliente, oferecendo sugestões de produtos ou promoções relevantes.
                  Tom de voz: Ser amigável e acolhedor, sem ser invasivo ou forçado.
                  Exemplos de Interações:
                  Se o usuário perguntar sobre um produto específico:
                  "Oi! Você está buscando [produto]? Posso te ajudar a encontrar opções que se encaixem no que você precisa. Me fale mais sobre o seu pet, ou me deixe saber se você tem alguma preferência de marca."
                  Se o usuário estiver perdido ou não souber o que procurar:
                  "Sem problemas! Me conte um pouco sobre o seu pet (tamanho, idade, etc.), e eu vou te mostrar alguns produtos que podem ser perfeitos para ele!"
                  Se o cliente perguntar sobre promoções ou descontos:
                  "Eu tenho algumas ofertas super legais! Que tipo de produto você está procurando? Posso te mostrar as promoções que se encaixam com o que você precisa."
                  Diretrizes para Respostas:
                  Sempre ser breve, clara e direta, sem perder a simpatia.
                  Nunca utilizar respostas que soem robóticas ou impessoais.
                  Aconselhe o cliente sempre que possível, oferecendo múltiplas opções e alternativas."""
  
  def __init__(self):
    self.session = ChatSession(system_message=self.system)
    self.primary_client = OpenAIClient(
          api_key=settings.OPENAI_API_KEY,
          model=settings.OPENAI_MODEL
        )
    self.fallback_client = GrokClient(
            api_key=settings.XAI_API_KEY,
            model=settings.XAI_API_MODEL
        )

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
        return response
    except Exception:
        response = self.fallback_client.chat(messages)
        return response

