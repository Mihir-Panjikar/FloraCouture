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
