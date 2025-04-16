from django.db import models

# Create your models here.


class ChatRoom(models.Model):
    retailer = models.ForeignKey(
        'retailers.Retailer', on_delete=models.CASCADE)
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'products.Product', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat between {self.customer.username} and {self.retailer.username}"


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=10, choices=[(
        'customer', 'Customer'), ('retailer', 'Retailer')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class ChatbotSession(models.Model):
    customer = models.ForeignKey(
        'customers.Customer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chatbot session for {self.customer.username} ({self.created_at})"


class ChatbotMessage(models.Model):
    session = models.ForeignKey(
        ChatbotSession, on_delete=models.CASCADE, related_name='messages')
    # False for customer, True for bot
    is_bot = models.BooleanField(default=False)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        sender = "Bot" if self.is_bot else "Customer"
        return f"{sender}: {self.content[:30]}..."


class BotResponse(models.Model):
    """Predefined responses for common queries"""
    CATEGORY_CHOICES = [
        ('greeting', 'Greeting'),
        ('product', 'Product Inquiry'),
        ('order', 'Order Status'),
        ('delivery', 'Delivery'),
        ('payment', 'Payment'),
        ('custom', 'Custom Bouquet'),
        ('complaint', 'Complaint'),
        ('farewell', 'Farewell'),
        ('fallback', 'Fallback'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    keywords = models.TextField(
        help_text="Comma-separated keywords that trigger this response")
    response_text = models.TextField()
    priority = models.PositiveSmallIntegerField(
        default=1, help_text="Higher number means higher priority")

    def __str__(self):
        return f"{self.category}: {self.response_text[:30]}..."


class ChatSession(models.Model):
    session_id = models.CharField(max_length=100)
    user = models.ForeignKey('customers.Customer',
                             on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.session_id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender = "Bot" if self.is_bot else "User"
        return f"{sender}: {self.message[:30]}"
