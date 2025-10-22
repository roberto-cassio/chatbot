from django.contrib import admin
from .models import AIConfig, ChatSession, ChatMessage, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'target_species', 'target_age', 'in_stock', 'is_available']
    list_filter = ['category', 'target_species', 'target_age', 'is_available', 'created_at']
    search_fields = ['name', 'description', 'target_breed']
    list_editable = ['price', 'stock', 'is_available']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'category', 'description')
        }),
        ('Precificação e Estoque', {
            'fields': ('price', 'stock', 'is_available')
        }),
        ('Segmentação', {
            'fields': ('target_species', 'target_breed', 'target_age')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def in_stock(self, obj):
        return obj.in_stock
    in_stock.boolean = True
    in_stock.short_description = 'Em Estoque'


@admin.register(AIConfig)
class AIConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_active', 'system_preview', 'created_at']
    list_filter = ['is_active']
    search_fields = ['system']
    
    def system_preview(self, obj):
        return obj.system[:100] + '...' if obj.system and len(obj.system) > 100 else obj.system
    system_preview.short_description = 'Prompt do Sistema'
    
    def created_at(self, obj):
        return 'Configurado'
    created_at.short_description = 'Status'


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
