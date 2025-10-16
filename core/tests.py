import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from core.services import ChatBotService, ChatSession
from core.middleware import InputSanitization
from core.models import ChatSession as ChatSessionModel, ChatMessage


class InputSanitizationTestCase(TestCase):
    
    def test_remove_html_tags(self):
        dirty = "<script>alert('xss')</script>Hello"
        clean = InputSanitization.sanitize_input(dirty)
        self.assertNotIn("<script>", clean)
        self.assertNotIn("</script>", clean)
    
    def test_truncate_long_text(self):
        long_text = "a" * 2000
        clean = InputSanitization.sanitize_input(long_text)
        self.assertEqual(len(clean), 1000)
    
    def test_remove_control_chars(self):
        dirty = "Hello\x00\x01World"
        clean = InputSanitization.sanitize_input(dirty)
        self.assertEqual(clean, "HelloWorld")


class ChatSessionTestCase(TestCase):
    
    def setUp(self):
        self.session = ChatSession(system_message="Test system")
    
    def test_add_user_message(self):
        self.session.add_user("Hello")
        self.assertEqual(len(self.session.history), 1)
        self.assertEqual(self.session.history[0]['role'], 'user')
        self.assertEqual(self.session.history[0]['content'], 'Hello')
    
    def test_add_bot_message(self):
        self.session.add_bot("Hi there!")
        self.assertEqual(len(self.session.history), 1)
        self.assertEqual(self.session.history[0]['role'], 'assistant')
    
    def test_get_past_messages_includes_system(self):
        self.session.add_user("Test")
        messages = self.session.get_past_messages()
        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[0]['content'], 'Test system')
        self.assertEqual(len(messages), 2)


class ChatBotServiceTestCase(TestCase):
    
    @patch('core.services.OpenAIClient')
    @patch('core.services.GroqClient')
    def test_fallback_strategy_primary_success(self, mock_groq, mock_openai):
        mock_openai_instance = MagicMock()
        mock_openai_instance.chat.return_value = "OpenAI response"
        mock_openai.return_value = mock_openai_instance
        
        service = ChatBotService()
        service.primary_client = mock_openai_instance
        
        response = service._fallback_strategy([{"role": "user", "content": "test"}])
        
        self.assertEqual(response, "OpenAI response")
        self.assertEqual(service.last_provider, 'openai')
        mock_openai_instance.chat.assert_called_once()
    
    @patch('core.services.OpenAIClient')
    @patch('core.services.GroqClient')
    def test_fallback_strategy_uses_groq_on_openai_failure(self, mock_groq, mock_openai):
        mock_openai_instance = MagicMock()
        mock_openai_instance.chat.side_effect = Exception("OpenAI down")
        
        mock_groq_instance = MagicMock()
        mock_groq_instance.chat.return_value = "Groq response"
        
        service = ChatBotService()
        service.primary_client = mock_openai_instance
        service.secondary_client = mock_groq_instance
        service.tertiary_client = None
        
        response = service._fallback_strategy([{"role": "user", "content": "test"}])
        
        self.assertEqual(response, "Groq response")
        self.assertEqual(service.last_provider, 'groq')
        mock_groq_instance.chat.assert_called_once()


class ChatViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('chat')
    
    def test_post_without_question_returns_400(self):
        response = self.client.post(
            self.url,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())
    
    def test_get_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
    
    def test_invalid_json_returns_400(self):
        response = self.client.post(
            self.url,
            data="invalid json",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    @patch('core.views.ChatBotService')
    @patch('core.views.RedisService')
    @patch('core.views.ChatLogger')
    def test_successful_request_returns_response_and_session_id(self, mock_logger, mock_redis, mock_service):
        mock_redis_instance = MagicMock()
        mock_redis_instance.generate_session_id.return_value = "test-session-123"
        mock_redis_instance.get_history.return_value = []
        mock_redis.return_value = mock_redis_instance
        
        mock_service_instance = MagicMock()
        mock_service_instance.get_bot_response.return_value = "Bot response"
        mock_service_instance.session.history = []
        mock_service_instance.last_provider = 'openai'
        mock_service.return_value = mock_service_instance
        
        response = self.client.post(
            self.url,
            data=json.dumps({"question": "Test question"}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        self.assertIn('session_id', data)
        self.assertEqual(data['response'], 'Bot response')


class ChatLogModelTestCase(TestCase):
    
    def test_create_chat_session(self):
        session = ChatSessionModel.objects.create(session_id="test-123")
        self.assertEqual(session.session_id, "test-123")
        self.assertIsNotNone(session.created_at)
        self.assertIsNotNone(session.last_interaction)
    
    def test_create_chat_message(self):
        session = ChatSessionModel.objects.create(session_id="test-456")
        message = ChatMessage.objects.create(
            session=session,
            role='user',
            content='Test message',
            ai_provider='openai'
        )
        self.assertEqual(message.role, 'user')
        self.assertEqual(message.content, 'Test message')
        self.assertEqual(message.ai_provider, 'openai')
    
    def test_chat_message_ordering(self):
        session = ChatSessionModel.objects.create(session_id="test-789")
        msg1 = ChatMessage.objects.create(session=session, role='user', content='First')
        msg2 = ChatMessage.objects.create(session=session, role='assistant', content='Second')
        
        messages = session.messages.all()
        self.assertEqual(messages[0].content, 'First')
        self.assertEqual(messages[1].content, 'Second')
