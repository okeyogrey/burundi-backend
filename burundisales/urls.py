from django.contrib import admin
from django.urls import path, include
from product_app.views import landing_page

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='home'),
    path('product/', include(('product_app.urls', 'product_app'), namespace='product_app')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('orders/', include('orders.urls')),
    path('paypal/', include(('paypal.standard.ipn.urls', 'paypal'), namespace='paypal')),
]

if settings.DEBUG:
    # Only serve MEDIA files locally when DEBUG=True
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
