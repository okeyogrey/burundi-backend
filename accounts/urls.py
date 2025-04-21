from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import custom_logout

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path(
      'login/',
      auth_views.LoginView.as_view(template_name='registration/login.html'),
      name='login'
    ),
    path('logout/', custom_logout, name='logout'),
]