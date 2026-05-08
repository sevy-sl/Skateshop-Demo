from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "store"
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_view, name='search'),
    path('<str:brand_type>/', views.brands_view, name='brands'),
    path('<str:brand_type>/<str:brand_name>/', views.items_view, name='items'),
    path('<str:brand_type>/<str:brand_name>/<str:item_name>/', views.detail_view, name='detail'),
    path('<str:brand_type>/<str:brand_name>/<str:item_name>/<int:item_id>/favorite/', views.favorite_toggle, name='favorite_toggle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)