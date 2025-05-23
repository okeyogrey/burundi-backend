from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove/', views.remove_from_cart, name='remove_from_cart'),
    path('update/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/<int:pk>/', views.order_success, name='order_success'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('payment-verify/', views.payment_verify, name='payment_verify'),
    path('history/', views.OrderHistoryView.as_view(), name='order_history'),
]
