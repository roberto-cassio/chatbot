import logging
import threading
from .models import ChatSession, ChatMessage


class ChatLogger:

    logger = logging.getLogger('chatbot_logger')
    
    @staticmethod
    def log_message(session_id, role, content, ai_provider=None):
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
            ChatLogger.logger.error(f"Erro ao logar mensagem: {e}")

    @staticmethod
    def log_message_async(session_id, role, content, ai_provider=None):
        thread = threading.Thread(
            target=ChatLogger.log_message,
            args=(session_id, role, content, ai_provider),
            daemon=True
        )
        thread.start()
    
    @staticmethod
    def log_conversation(session_id, user_message, bot_response, ai_provider=None):
        def _log_both():
            try:
                session, _ = ChatSession.objects.get_or_create(
                    session_id=session_id
                )
                
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
                ChatLogger.logger.error(f"Erro ao logar conversa: {e}")

        thread = threading.Thread(target=_log_both, daemon=True)
        thread.start()
