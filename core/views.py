import json
from django.http import JsonResponse
from .redis_service import RedisService
from .services import ChatBotService

def chat_view(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body)
      redis_service = RedisService()
      #A ideia é que junto a requsicão o session_id seja reenviado para manter a conversa
      session_id = request.headers.get('X-Session-ID') or data.get('session_id')
      if not session_id:
          session_id = redis_service.generate_session_id()

      history = redis_service.get_history(session_id)

      service = ChatBotService()
      service.session.history = history

      user_message = data.get('question', '')
      if not user_message:
        return JsonResponse({'error': 'No question provided'}, status=400) 
  
      chatbot_response = service.get_bot_response(user_message)
      redis_service.save_history(session_id, service.session.history)
      return JsonResponse({'resposta': chatbot_response,
                           'session_id': session_id})
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid JSON'}, status=400)
  return JsonResponse({'error': 'Invalid request method'}, status=405)
