from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from orders.models import Order
from django.contrib.auth.views import LogoutView


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('accounts:login')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['orders'] = Order.objects.filter(user=self.request.user).order_by('-created')
        return ctx
    
class MyLogoutView(LogoutView):
    # these are the default, but you can redefine if yours are different
    http_method_names = ['get', 'post', 'head', 'options', 'trace']