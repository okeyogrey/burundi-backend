from django.contrib import admin
from django.urls import path, include
from product_app.views import landing_page

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # REMOVED the old path('', landing_page, name='landing_page'),
    # Instead, we rely on product_app/urls.py for /product/landing/.

    path('', landing_page, name='home'),

    path('product/', include(('product_app.urls', 'product_app'), namespace='product_app')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('orders/', include('orders.urls')),
    path('paypal/', include(('paypal.standard.ipn.urls', 'paypal'), namespace='paypal')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
