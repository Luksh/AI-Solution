from django.urls import path
from . import views
from django.shortcuts import redirect
from .views import CustomAdminLoginView

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('solutions/', views.solutions, name='solutions'),
    path('solutions/<slug:slug>/', views.solution_detail, name='solution_detail'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('case-studies/<int:id>/', views.case_study_detail, name='case_study_detail'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('events/', views.events, name='events'),
    path('contact/', views.contact, name='contact'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('test-logo/', views.test_logo, name='test_logo'),
    path('login/', lambda request: redirect('admin:login'), name='login'),
    path('events/', views.events, name='events'),
     path('login/', CustomAdminLoginView.as_view(), name='login'),
     path('chat/', views.chat, name='chat'),
     path('event-register/', views.event_register, name='event_register'),
     # Add this new URL pattern to your urlpatterns list
     path('events/<int:event_id>/', views.event_detail, name='event_detail'),
     # Add this new URL pattern to your urlpatterns list
     path('events/<int:event_id>/', views.event_detail, name='event_detail'),
]
