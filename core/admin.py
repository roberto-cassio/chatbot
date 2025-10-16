from django.contrib import admin
from .models import ChatSession, ChatMessage


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'last_interaction', 'message_count']
    list_filter = ['created_at', 'last_interaction']
    search_fields = ['session_id']
    readonly_fields = ['session_id', 'created_at', 'last_interaction']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Mensagens'


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'content_preview', 'ai_provider', 'timestamp']
    list_filter = ['role', 'ai_provider', 'timestamp']
    search_fields = ['content', 'session__session_id']
    readonly_fields = ['session', 'role', 'content', 'timestamp', 'ai_provider']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Conteúdo'
