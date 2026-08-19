from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from itertools import chain


from cart.models import Cart, CartItem
from store.models import FavoriteItem

def register(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']

		user = User.objects.create_user(
			username=username,
			email=email,
			password=password,
			is_active=False
		)

		token = default_token_generator.make_token(user)
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		link = request.build_absolute_uri(reverse('user:activate', args=[uid, token]))

		send_mail(
			'Confirm your account',
			f'Click the link to activate your account: {link}',
			'noreply@example.com',
			[email],
		)

		return render(request, 'user/check_mail.html')

	return render(request, 'user/register.html')


def Login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('user:index')
		else:
			messages.info(request, 'Account does not exist')

	return render(request, 'user/login.html', {'title': 'Login here'})


def logout_view(request):
	logout(request)
	return redirect('user:login')


def activate(request, uidb64, token):
	User = get_user_model()
	uid = urlsafe_base64_decode(uidb64).decode()
	user = get_object_or_404(User, pk=uid)

	if default_token_generator.check_token(user, token):
		user.is_active = True
		user.save()
		return redirect('user:login')

	return render(request, 'user/activation_failed.html')


@login_required(login_url='/profile/login/')
def index(request):
	cart, _ = Cart.objects.get_or_create(user=request.user)

	favorites = FavoriteItem.objects.filter(user=request.user).select_related(
'original_item', 'original_item__parent_brand').order_by('-created_at')[:8]

	context = {
		'cart_items': cart.items.all(),
		'favorites': favorites
	}

	return render(request, 'user/index.html', context)
