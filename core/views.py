import json
from django.http import JsonResponse
from django.shortcuts import render
from core.services import ChatBotService
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt # Para teste, remover
def ChatView(request):
  if request.method == "POST":
    try:
      data = json.loads(request.body)

      user_message = data.get('question', '')
      if not user_message:
        return JsonResponse({'error': 'No question provided'}, status=400) 

      chatbot_response = ChatBotService.get_bot_response(user_message)
      return JsonResponse({'answer': chatbot_response})
    except json.JSONDecodeError:
      return JsonResponse({'error': 'Invalid JSON'}, status=400)
  return JsonResponse({'error': 'Invalid request method'}, status=405)
