import threading
from .models import ChatSession, ChatMessage


class ChatLogger:
    """
    Serviço para logging de conversas do chatbot.
    Suporta logging síncrono e assíncrono.
    """
    
    @staticmethod
    def log_message(session_id, role, content, ai_provider=None):
        """
        Loga uma mensagem do chat de forma síncrona.
        
        Args:
            session_id: UUID da sessão
            role: 'user', 'assistant' ou 'system'
            content: Conteúdo da mensagem
            ai_provider: 'openai' ou 'grok' (opcional)
        """
        try:
            session, _ = ChatSession.objects.get_or_create(
                session_id=session_id
            )
            ChatMessage.objects.create(
                session=session,
                role=role,
                content=content,
                ai_provider=ai_provider
            )
        except Exception as e:
            print(f"[ChatLogger] Erro ao logar mensagem: {e}")
    
    @staticmethod
    def log_message_async(session_id, role, content, ai_provider=None):
        """
        Loga uma mensagem do chat de forma assíncrona (background thread).
        Não bloqueia a resposta HTTP.
        
        Args:
            session_id: UUID da sessão
            role: 'user', 'assistant' ou 'system'
            content: Conteúdo da mensagem
            ai_provider: 'openai' ou 'grok' (opcional)
        """
        thread = threading.Thread(
            target=ChatLogger.log_message,
            args=(session_id, role, content, ai_provider),
            daemon=True
        )
        thread.start()
    
    @staticmethod
    def log_conversation(session_id, user_message, bot_response, ai_provider=None):
        """
        Loga uma troca completa (user + bot) de forma assíncrona.
        
        Args:
            session_id: UUID da sessão
            user_message: Mensagem do usuário
            bot_response: Resposta do bot
            ai_provider: 'openai' ou 'grok' (opcional)
        """
        def _log_both():
            try:
                session, _ = ChatSession.objects.get_or_create(
                    session_id=session_id
                )
                
                # Cria ambas as mensagens em uma transação
                ChatMessage.objects.create(
                    session=session,
                    role='user',
                    content=user_message
                )
                ChatMessage.objects.create(
                    session=session,
                    role='assistant',
                    content=bot_response,
                    ai_provider=ai_provider
                )
            except Exception as e:
                print(f"[ChatLogger] Erro ao logar conversa: {e}")
        
        thread = threading.Thread(target=_log_both, daemon=True)
        thread.start()
