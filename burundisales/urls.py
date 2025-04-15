# burundisales/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# REMOVE this import if you no longer use it at the root:
# from product_app.views import landing_page

urlpatterns = [
    path('admin/', admin.site.urls),

    # REMOVED the old path('', landing_page, name='landing_page'),
    # Instead, we rely on product_app/urls.py for /product/landing/.

    path('product/', include('product_app.urls')),  # The correct mapping
    path('orders/', include('orders.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
