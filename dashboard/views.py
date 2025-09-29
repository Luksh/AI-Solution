from django.shortcuts import render

# Create your views here.
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomAdminLoginView(LoginView):
    template_name = 'dashboard/login.html'
    form_class = AdminAuthenticationForm
    
    def get_success_url(self):
        # Check if there's a next parameter
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('admin:index')
