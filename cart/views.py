from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Cart, CartItem
from store.models import CompleteSkateboard, Deck, Truck


@login_required(login_url='/profile/login/')
def cart_add(request):
	if request.method == 'POST':
		item_id = request.POST.get('item_id')
		item_type = request.POST.get('item_type')
		item_quantity = int(request.POST.get('item_quantity', 1))

		cart, _ = Cart.objects.get_or_create(user=request.user)

		if item_type == 'skateboard':
			item = CompleteSkateboard.objects.get(id=item_id)
			filter_kwargs = {'skateboard': item}

		elif item_type == 'deck':
			item = Deck.objects.get(id=item_id)
			filter_kwargs = {'deck': item}

		elif item_type == 'truck':
			item = Truck.objects.get(id=item_id)
			filter_kwargs = {'truck': item}

		else:
			return redirect('cart:detail')

		cart_item, created = CartItem.objects.get_or_create(
			cart=cart,
			defaults={'quantity': item_quantity},
			**filter_kwargs
		)

		if not created:
			cart_item.quantity += item_quantity
			cart_item.save()

	return redirect("cart:detail")


@login_required(login_url='/profile/login/')
def cart_detail(request):
	cart, _ = Cart.objects.get_or_create(user=request.user)

	if request.method == 'POST':
		if 'clear_cart' in request.POST:
			cart.items.all().delete()
			return redirect('cart:detail')
		elif 'clear_item' in request.POST:
			cart.items.filter(id=request.POST.get('item_id')).delete()
			return redirect('cart:detail')
		
	context = {
		'cart': cart,
		'items': cart.items.all(),
	}

	return render(request, 'cart/detail.html', context)
