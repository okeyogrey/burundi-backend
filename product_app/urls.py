from django.urls import path
from . import views

app_name = 'product_app'  # Add this to fix URL redirection issues

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('json/', views.product_list_json, name='product_list_json'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]
