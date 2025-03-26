from django.urls import path
from . import views

app_name = 'product_app'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('json/', views.product_list_json, name='product_list_json'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),

    # Landing page if you want /product/landing/
    path('landing/', views.landing_page, name='landing_page'),
]
