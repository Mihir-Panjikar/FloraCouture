from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "chat"

    def ready(self):
        # Register models with the admin site
        from django.contrib import admin
        from . import models

        @admin.register(models.ChatbotSession)
        class ChatbotSessionAdmin(admin.ModelAdmin):
            list_display = ('customer', 'created_at',
                            'last_activity', 'is_active')
            list_filter = ('is_active', 'created_at')
            search_fields = ('customer__username',)

        @admin.register(models.ChatbotMessage)
        class ChatbotMessageAdmin(admin.ModelAdmin):
            list_display = ('get_customer', 'is_bot',
                            'content_preview', 'timestamp')
            list_filter = ('is_bot', 'timestamp')
            search_fields = ('content', 'session__customer__username')

            def get_customer(self, obj):
                return obj.session.customer.username
            get_customer.short_description = 'Customer'

            def content_preview(self, obj):
                return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
            content_preview.short_description = 'Content'

        @admin.register(models.BotResponse)
        class BotResponseAdmin(admin.ModelAdmin):
            list_display = ('category', 'keywords_preview',
                            'response_preview', 'priority')
            list_filter = ('category', 'priority')
            search_fields = ('keywords', 'response_text')

            def keywords_preview(self, obj):
                return obj.keywords[:30] + '...' if len(obj.keywords) > 30 else obj.keywords
            keywords_preview.short_description = 'Keywords'

            def response_preview(self, obj):
                return obj.response_text[:50] + '...' if len(obj.response_text) > 50 else obj.response_text
            response_preview.short_description = 'Response'
