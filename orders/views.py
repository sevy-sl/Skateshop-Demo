import time
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import Cart

@login_required(login_url='/profile/login')
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()

    if not cart_items:
        return redirect('cart:detail')

    context = {
        'cart': cart,
        'items': cart_items
    }
    return render(request, 'orders/checkout.html', context)

@login_required(login_url='/profile/login/')
def payment(request):
	if request.method != 'POST':
		return redirect('cart:detail')
	
	cart = Cart.objects.get(user=request.user)
	items = cart.items.all()

	if not cart.items.exists():
		return redirect('cart:detail')
      
	if 'pay' in request.POST:
		card_number = request.POST.get('card_number')
		expiry = request.POST.get('expiry')
		cvv = request.POST.get('cvv')

		if len(card_number) < 9 or len(expiry) < 5 or len(cvv) < 3:
			messages.error(request, 'Payment failed')
			return redirect('orders:payment')

		order = Order.objects.create(
			user=request.user,
			total_price=cart.total_price,
			status='paid'
		)

		for item in items:
			OrderItem.objects.create(
				order=order,
				name=item.item.name,
				price=item.price,
				quantity=item.quantity
			)

		items.delete()
		
		messages.success(request, f'Order #{order.id} placed successfully')

		time.sleep(2)

		return redirect('user:index')
	
	context= {
		'cart': cart
	}

	return render(request, 'orders/payment.html', context)