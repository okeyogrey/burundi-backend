from django.urls import path
from . import views
from .views import MyLogoutView

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
]