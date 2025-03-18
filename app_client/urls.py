from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('signup/', views.client_signup_view, name='client_signup'),
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.custom_logout, name='logout'),
] 