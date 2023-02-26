from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='authors-register'),
    #path('register/create/', views.register_create, name='authors-register-create'),
    path('login/', views.login_view, name='authors-login'),
    path('login/create/', views.login_create, name='authors-login-create'),
    path('logout/', views.logout_view, name='authors-logout'),
    path('dashboard/', views.dashboard, name='authors-dashboard'),
    path('dashboard/recipe/<int:id>/edit', views.cbv.DashboardRecipeView.as_view(), name='authors-dashboard-recipe-edit'),
    path('dashboard/recipe/<int:id>/delete', views.cbv.DashboardRecipeDelete.as_view(), name='authors-dashboard-recipe-delete'),
    path('dashboard/recipe/create', views.cbv.DashboardRecipeView.as_view(), name='authors-dashboard-recipe-create'),
    
]