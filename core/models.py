from django.db import models

class AIConfig(models.Model):
  id = models.AutoField(primary_key=True)
  system = models.TextField(null=True, blank=True)
  is_active = models.BooleanField(default=False)

class ChatSession(models.Model):
  session_id = models.CharField(max_length=64, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  last_interaction = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Sessão: {self.session_id}"
  
class ChatMessage(models.Model):
  ROLE_CHOICES = [
    ('user', 'Usuário'),
    ('assistant', 'Assistente'),
    ('system', 'Sistema'),
  ]
  session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
  role = models.CharField(max_length=10, choices=ROLE_CHOICES)
  content = models.TextField()
  timestamp = models.DateTimeField(auto_now_add=True)
  ai_provider = models.CharField(max_length=20, blank=True, null=True)

  class Meta:
    ordering = ['timestamp']

  def __str__(self):
    return f"[{self.role}] {self.content[:50]}..."