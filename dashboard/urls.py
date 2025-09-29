from django.urls import path
from .views import CustomAdminLoginView
app_name = 'dashboard'

urlpatterns = [
    path('login/', CustomAdminLoginView.as_view(), name='login'),
]