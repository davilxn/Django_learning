from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='authors-register'),
    path('register/create/', views.register_create, name='authors-register-create'),
    path('login/', views.login_view, name='authors-login'),
    path('login/create/', views.login_create, name='authors-login-create'),
    path('logout/', views.logout_view, name='authors-logout'),
    path('dashboard/', views.dashboard, name='authors-dashboard'),
]