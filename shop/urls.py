from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/shop/', permanent=False)),
    path('shop/', include(('store.urls', 'store'), namespace='store')),
    path('profile/', include(('user.urls', 'user'), namespace='user')),
    path('profile/cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('profile/cart/checkout/', include(('orders.urls', 'orders'), namespace='orders')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
