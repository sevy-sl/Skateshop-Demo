from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "store"
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_view, name='search'),
    path('<str:brand_type>/', views.brands_view, name='brands'),
    path('<str:brand_type>/<slug:brand_slug>/', views.items_view, name='items'),
    path('<str:brand_type>/<slug:brand_slug>/<slug:item_slug>/', views.detail_view, name='detail'),
    path('<str:brand_type>/<slug:brand_slug>/<slug:item_slug>/favorite/', views.favorite_toggle, name='favorite_toggle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)