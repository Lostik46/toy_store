from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    
    # URLs для категорий
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_edit, name='category_add'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    # URLs для продуктов
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
] 