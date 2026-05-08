from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views

app_name = "user"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login, name ='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name ='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('favorites/skateboards/', views.favorite_skateboards_view, name='favorite_skateboards'),
    path('favorites/decks/', views.favorite_decks_view, name='favorite_decks'),
    path('favorites/trucks/', views.favorite_trucks_view, name='favorite_trucks'),
    path('favorites/', RedirectView.as_view(url='/profile/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)