from django.db import models
from django.contrib.auth.models import User 


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Status(models.TextChoices):
        PENDING = 'pending'
        PAID = 'paid'
        CANCELLED = 'cancelled'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    def __str__(self):
        return f'Order #{self.id} - {self.user.username}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name} (x{self.quantity})'
    

