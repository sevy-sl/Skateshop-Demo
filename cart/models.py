from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.price for item in self.items.all())
    
class CartItem(models.Model):
	cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)

	skateboard = models.ForeignKey('store.CompleteSkateboard', null=True, blank=True, on_delete=models.CASCADE)
	deck = models.ForeignKey('store.Deck', null=True, blank=True, on_delete=models.CASCADE)
	truck = models.ForeignKey('store.Truck', null=True, blank=True, on_delete=models.CASCADE)

	quantity = models.PositiveIntegerField(default=1)

	@property
	def item(self):
		return self.skateboard or self.deck or self.truck

	@property
	def price(self):
		return self.item.price * self.quantity
