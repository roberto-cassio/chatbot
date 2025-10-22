import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .redis_service import RedisService
from .services import ChatBotService
from .logger_service import ChatLogger

@csrf_exempt
def chat_view(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body)
      redis_service = RedisService()
      
      session_id = request.headers.get('X-Session-ID') or data.get('session_id')
      if not session_id:
          session_id = redis_service.generate_session_id()

      history = redis_service.get_history(session_id)

      service = ChatBotService()
      service.memory.chat_memory.messages = service.deserialize_history(history)

      user_message = data.get('question', '')
      if not user_message:
        return JsonResponse({'error': 'No question provided'}, status=400)

      chatbot_response = service.get_bot_response(user_message)

      updated_history = service.memory.chat_memory.messages
      serialized_history = service.serialize_history(updated_history)
      redis_service.save_history(session_id, serialized_history)

      ChatLogger.log_conversation(
          session_id=session_id,
          user_message=user_message,
          bot_response=chatbot_response,
          ai_provider=service.last_provider
      )

      return JsonResponse({
          'response': chatbot_response,
          'session_id': session_id
      })
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid JSON'}, status=400)
  return JsonResponse({'error': 'Invalid request method'}, status=405)
