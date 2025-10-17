# 🐾 Chatbot Petlove - Assistente de Vendas com IA

Chatbot inteligente desenvolvido como assistente de vendas para e-commerce da Petlove, utilizando múltiplos provedores de IA com estratégia de fallback.

## 🚀 Características Principais

### ✨ Funcionalidades
- 🤖 **Assistente de vendas** especializado em produtos para pets
- 💬 **Conversas contextuais** com persistência de histórico
- 🔄 **Triple Fallback Strategy**: OpenAI → Groq → Grok
- 📊 **Logging completo** de conversas para auditoria
- 🎯 **Session management** via Redis
- 🛡️ **Input sanitization** para segurança
- 📈 **Django Admin** para visualização e análise

### 🏗️ Arquitetura

```
┌─────────────────────────────────────────────┐
│         TRIPLE FALLBACK STRATEGY            │
├─────────────────────────────────────────────┤
│  1️⃣ OpenAI (Primary)                        │
│     ├─ Success → Responde                  │
│     └─ Fail ↓                              │
│  2️⃣ Groq (Secondary) - GRÁTIS! 🆓          │
│     ├─ Success → Responde                  │
│     └─ Fail ↓                              │
│  3️⃣ Grok (Tertiary) - Opcional             │
│     ├─ Success → Responde                  │
│     └─ Fail → Exception                    │
└─────────────────────────────────────────────┘

     ┌──────────────┐
     │   Request    │
     └──────┬───────┘
            │
     ┌──────▼──────────────────────┐
     │  Redis (Cache - 1h TTL)     │  ← Contexto da conversa
     │  + Session Management       │
     └──────┬──────────────────────┘
            │
     ┌──────▼──────────────────────┐
     │  SQLite (Persistent Log)    │  ← Auditoria completa
     │  + Analytics                │
     └─────────────────────────────┘
```

## 📋 Requisitos

- Python 3.8+
- Redis Server
- API Key de pelo menos um provedor de IA (OpenAI ou Groq)

## 🔧 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/roberto-cassio/chatbot.git
cd chatbot/chatbot
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

Edite o `.env` e adicione suas API keys:
```bash
# Opção 1: Usar OpenAI (necessita cartão, mas tem $5 grátis)
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-3.5-turbo

# Opção 2: Usar Groq (100% GRÁTIS - Recomendado para testes!)
GROQ_API_KEY=gsk_xxxxx
GROQ_MODEL=llama-3.1-70b-versatile

# Opcional: Grok/xAI (pago)
XAI_API_KEY=
XAI_API_MODEL=grok-beta
```

**Como conseguir API keys grátis:**
- **Groq (Recomendado)**: https://console.groq.com → 100% grátis
- **OpenAI**: https://platform.openai.com → $5 de crédito inicial

### 5. Instale e inicie o Redis
```bash
# macOS
brew install redis
redis-server

# Linux
sudo apt-get install redis-server
redis-server

# Windows
# Baixe de: https://redis.io/download
```

### 6. Execute as migrations
```bash
python manage.py migrate
```

### 7. (Opcional) Crie um superusuário para o Admin
```bash
python manage.py createsuperuser
```

### 8. Inicie o servidor
```bash
python manage.py runserver
```

## 📡 Como Usar

### Endpoint da API
```
POST http://localhost:8000/api/question-and-answer/
```

### Exemplo de Request
```bash
curl -X POST http://localhost:8000/api/question-and-answer/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Qual a melhor ração para golden retriever?"
  }'
```

### Exemplo de Response
```json
{
  "response": "Para Golden Retriever, recomendo rações premium como Royal Canin Golden Retriever ou Premier Pet Golden...",
  "session_id": "e8f7a2b1-3c4d-5e6f-7a8b-9c0d1e2f3a4b"
}
```

### Mantendo Contexto da Conversa
```bash
# Request 1
curl -X POST http://localhost:8000/api/question-and-answer/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Tenho um golden de 2 anos"}'

# Response retorna session_id: "abc-123..."

# Request 2 (com contexto)
curl -X POST http://localhost:8000/api/question-and-answer/ \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Qual ração você recomenda?",
    "session_id": "abc-123..."
  }'

# Bot vai recomendar considerando que é um golden de 2 anos!
```

## 🎯 Diferenciais Técnicos

### �️ Catálogo de Produtos Integrado
- **Model Product**: Produtos armazenados no banco de dados SQLite
- **Injeção automática**: Catálogo carregado dinamicamente no contexto da IA
- **Pré-prompt + Prompt**: Arquitetura separada para catálogo e instruções
- **Filtragem inteligente**: Apenas produtos disponíveis (`is_available=True` e `stock > 0`)
- **Campos completos**: Nome, categoria, preço, estoque, espécie, raça, idade, descrição
- **Django Admin**: Interface completa para gerenciar produtos (criar, editar, desativar)
- **Recomendações reais**: IA recomenda apenas produtos que existem e estão em estoque

### 🔄 Resiliência
- **Triple Fallback**: Se OpenAI falhar, tenta Groq. Se Groq falhar, tenta Grok.
- **Rastreamento**: Sabe qual provedor respondeu (`last_provider`)
- **Logs**: Imprime falhas no console para debugging

### 💾 Dual Persistence
- **Redis**: Cache rápido para contexto (TTL: 1 hora)
- **SQLite**: Log permanente para auditoria e analytics

### 🛡️ Segurança
- **Input Sanitization**: Remove HTML, caracteres de controle
- **Truncamento**: Limita input em 1000 caracteres (proteção DoS)
- **HTML Escape**: Previne XSS

### 📊 Observabilidade
- **Django Admin**: Visualize todas as conversas
- **Filtros**: Por data, provedor de IA, role
- **Busca**: Por conteúdo ou session_id
- **Métricas**: Contador de mensagens por sessão
- **Logging Estruturado**: Logs em console e arquivos rotativos
  - `logs/chatbot.log`: Warnings e acima (max 5MB, 5 backups)
  - `logs/errors.log`: Apenas errors (max 5MB, 5 backups)

## 🔍 Acessando o Admin

```
URL: http://localhost:8000/admin/
Login: (use o superuser criado)
```

Você poderá:
- Ver todas as sessões de chat
- Analisar conversas completas
- Filtrar por provedor de IA (openai, groq, grok)
- Buscar por conteúdo específico

## 🧪 Testes Automatizados

### Executar os testes
```bash
python manage.py test core
```

### Cobertura de Testes
- ✅ **Input Sanitization**: Remoção de HTML, caracteres de controle, truncamento
- ✅ **ChatSession**: Gerenciamento de histórico
- ✅ **ChatBotService**: Estratégia de fallback (OpenAI → Groq)
- ✅ **API Endpoint**: Validações, erros HTTP, session management
- ✅ **Models**: Criação e ordenação de mensagens
- ✅ **AIConfig**: Prompts customizáveis via banco de dados

```bash
# Output esperado:
# Creating test database...
# ..................
# ----------------------------------------------------------------------
# Ran 19 tests in 0.XXXs
# 
# OK
```

## 🧪 Testando Manualmente

### Teste Básico
```bash
curl -X POST http://localhost:8000/api/question-and-answer/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Olá!"}'
```

### Teste com Contexto
```python
import requests

# Primeira mensagem
r1 = requests.post(
    'http://localhost:8000/api/question-and-answer/',
    json={'question': 'Meu nome é João e tenho um gato'}
)
session_id = r1.json()['session_id']

# Segunda mensagem (com contexto)
r2 = requests.post(
    'http://localhost:8000/api/question-and-answer/',
    json={
        'question': 'Qual é o meu nome e qual pet eu tenho?',
        'session_id': session_id
    }
)
print(r2.json()['response'])
# Output: "Seu nome é João e você tem um gato!"
```

## 📁 Estrutura do Projeto

```
chatbot/
├── core/
│   ├── ai_clients.py       # Clientes OpenAI, Groq, Grok
│   ├── services.py         # ChatBotService com fallback
│   ├── views.py            # Endpoint da API
│   ├── models.py           # ChatSession, ChatMessage
│   ├── logger_service.py   # Logging assíncrono
│   ├── redis_service.py    # Session management
│   ├── middleware.py       # Input sanitization
│   ├── admin.py            # Config do Django Admin
│   └── urls.py
├── chatbot/
│   ├── settings.py         # Configurações
│   └── urls.py
├── populate_products.py    # Script para popular produtos
├── requirements.txt
├── .env.example
├── .gitignore
└── manage.py
```

## 🚀 Próximos Passos
-  **RAG (Retrieval-Augmented Generation)**: Indexar produtos com embeddings vetoriais, buscar apenas produtos relevantes por query (ex: "ração golden" → só rações para raças grandes) tornando as respostas mais precisas e com menor custo de tokens.
-  **Rate Limiting via Redis**: Proteção contra abuso de API usando Redis para controle de requisições por IP/usuário
-  **Circuit Breaker**: Adicionar padrão de resiliência para evitar sobrecarga em falhas consecutivas
-  **Celery para Processamento Assíncrono**: Substituir threading manual por Celery com RabbitMQ/Redis para logging e tarefas pesadas
-  **Proxy para Gerenciamento de IAs**: Criação de Proxy para fazer o gerenciamento dos modelos de IA possibilitando:
      - 🔐 **Segurança**: API keys isoladas em um serviço separado
      - 📊 **Monitoramento**: Logs centralizados de todas as chamadas
      - 🚦 **Rate Limiting**: Controle granular por IP/usuário
      - 💰 **Controle de Custo**: Métricas de uso por cliente
      - 🔄 **Load Balancing**: Distribuição inteligente entre prov logging e identificação das tentativas de acesso via IP além de dar mais uma camada de segurança para as API Keys.


## 👤 Autor

Roberto Cássio
- GitHub: [@roberto-cassio](https://github.com/roberto-cassio)

