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

from cart.models import Cart, CartItem


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
			"Confirm your account",
			f"Click the link to activate your account: {link}",
			"noreply@example.com",
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

	context = {
		'favorite_skateboards': request.user.favorite_skateboards.through.objects.filter(user=request.user).order_by('-created_at')[:5],
		'favorite_decks': request.user.favorite_decks.through.objects.filter(user=request.user).order_by('-created_at')[:5],
		'favorite_trucks': request.user.favorite_trucks.through.objects.filter(user=request.user).order_by('-created_at')[:5],
		'cart_items': cart.items.all(),
	}

	return render(request, 'user/index.html', context)


def favorite_skateboards_view(request):
	paginator = Paginator(
		request.user.favorite_skateboards.through.objects.filter(user=request.user).order_by('-created_at'),
		5
	)

	page_obj = paginator.get_page(request.GET.get('page'))

	return render(request, 'user/favorites.html', {'favorites': page_obj})


def favorite_decks_view(request):
	paginator = Paginator(
		request.user.favorite_decks.through.objects.filter(user=request.user).order_by('-created_at'),
		5
	)

	page_obj = paginator.get_page(request.GET.get('page'))

	return render(request, 'user/favorites.html', {'favorites': page_obj})


def favorite_trucks_view(request):
	paginator = Paginator(
		request.user.favorite_trucks.through.objects.filter(user=request.user).order_by('-created_at'),
		5
	)

	page_obj = paginator.get_page(request.GET.get('page'))

	return render(request, 'user/favorites.html', {'favorites': page_obj})