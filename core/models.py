from django.db import models

class AIConfig(models.Model):
  id = models.AutoField(primary_key=True)
  system = models.TextField(null=True, blank=True)
  is_active = models.BooleanField(default=False)

class Product(models.Model):
  CATEGORY_CHOICES = [
    ('racao', 'Ração'),
    ('petisco', 'Petisco'),
    ('brinquedo', 'Brinquedo'),
    ('acessorio', 'Acessório'),
    ('higiene', 'Higiene'),
    ('saude', 'Saúde'),
  ]
  
  SPECIES_CHOICES = [
    ('cachorro', 'Cachorro'),
    ('gato', 'Gato'),
    ('passaro', 'Pássaro'),
    ('peixe', 'Peixe'),
    ('roedor', 'Roedor'),
    ('todos', 'Todos'),
  ]
  
  AGE_CHOICES = [
    ('filhote', 'Filhote'),
    ('adulto', 'Adulto'),
    ('idoso', 'Idoso'),
    ('todos', 'Todos'),
  ]
  
  name = models.CharField(max_length=200, verbose_name='Nome do Produto')
  category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Categoria')
  price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
  stock = models.IntegerField(default=0, verbose_name='Estoque')
  description = models.TextField(verbose_name='Descrição')
  target_species = models.CharField(max_length=20, choices=SPECIES_CHOICES, verbose_name='Espécie')
  target_breed = models.CharField(max_length=100, blank=True, verbose_name='Raça Específica')
  target_age = models.CharField(max_length=20, choices=AGE_CHOICES, default='todos', verbose_name='Idade')
  is_available = models.BooleanField(default=True, verbose_name='Disponível')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['-created_at']
    verbose_name = 'Produto'
    verbose_name_plural = 'Produtos'

  def __str__(self):
    return f"{self.name} - R$ {self.price}"
  
  @property
  def in_stock(self):
    return self.stock > 0 and self.is_available

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