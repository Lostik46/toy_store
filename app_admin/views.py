from django.shortcuts import redirect, get_object_or_404, render
from . import forms
from django.contrib.auth import  login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ProductCategory, Product
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView

def login_view(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home') 
            return redirect('home') 
    else:
        form = forms.LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def admin_home(request):
    if not request.user.is_superuser:
        return redirect('home')
        
    context = {
        'categories_count': ProductCategory.objects.count(),
        'products_count': Product.objects.count(),
        'active_sales': Product.objects.filter(
            is_active=True,
            is_on_sale=True,
            discount_start_date__lte=timezone.now(),
            discount_end_date__gte=timezone.now()
        ).count()
    }
    return render(request, 'app_admin/admin_home.html', context)

@login_required
def category_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    categories = ProductCategory.objects.all()
    return render(request, 'app_admin/category_list.html', {'categories': categories})

@login_required
def category_edit(request, pk=None):
    if not request.user.is_superuser:
        return redirect('home')
    
    if pk:
        category = get_object_or_404(ProductCategory, pk=pk)
    else:
        category = None

    if request.method == 'POST':
        form = forms.ProductCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Категория успешно сохранена')
            return redirect('category_list')
    else:
        form = forms.ProductCategoryForm(instance=category)

    return render(request, 'app_admin/category_form.html', {
        'form': form,
        'category': category
    })

@login_required
def category_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    
    category = get_object_or_404(ProductCategory, pk=pk)
    category.delete()
    messages.success(request, 'Категория успешно удалена')
    return redirect('category_list')

@login_required
def product_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    products = Product.objects.all()
    return render(request, 'app_admin/product_list.html', {'products': products})

class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = forms.ProductForm
    template_name = 'app_admin/product_form.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        # Если товар не по акции, очищаем поля скидки
        if not form.cleaned_data['is_on_sale']:
            form.instance.discount = None
            form.instance.discount_start_date = None
            form.instance.discount_end_date = None
        response = super().form_valid(form)
        messages.success(self.request, 'Товар успешно создан!')
        return response

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = forms.ProductForm
    template_name = 'app_admin/product_form.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        # Если товар не по акции, очищаем поля скидки
        if not form.cleaned_data['is_on_sale']:
            form.instance.discount = None
            form.instance.discount_start_date = None
            form.instance.discount_end_date = None
        response = super().form_valid(form)
        messages.success(self.request, 'Товар успешно обновлен!')
        return response

@login_required
def product_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Товар успешно удален')
    return redirect('product_list')