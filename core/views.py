import json
from django.http import JsonResponse
from core.services import ChatBotService

def chat_view(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body)

      user_message = data.get('question', '')
      if not user_message:
        return JsonResponse({'error': 'No question provided'}, status=400) 

      service = ChatBotService()
      chatbot_response = service.get_bot_response(user_message)
      return JsonResponse({'answer': chatbot_response})
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid JSON'}, status=400)
  return JsonResponse({'error': 'Invalid request method'}, status=405)
