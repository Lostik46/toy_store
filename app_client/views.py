from django.shortcuts import get_object_or_404, render, redirect
from . import forms
from django.contrib import messages
from django.db.models import Q
from app_admin.models import Product, ProductCategory, Client
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

def custom_logout(request):
    logout(request)
    return redirect('home')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'registration/login.html')

def client_signup_view(request):
    userForm = forms.ClientUserForm()
    clientForm = forms.ClientForm()
    mydict = {'userForm': userForm, 'ClientForm': clientForm}
    if request.method == 'POST':
        userForm = forms.ClientUserForm(request.POST)
        clientForm = forms.ClientForm(request.POST, request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = clientForm.save(commit=False)
            customer.user = user
            customer.save()
            messages.success(request, "Регистрация прошла успешно! Теперь вы можете войти.")
            return redirect('login') 
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    return render(request, 'app_client/sign_up.html', context=mydict)

@login_required
def profile_view(request):
    if request.user.is_superuser:
        return redirect('admin_home')
        
    try:
        client = request.user.client
    except Client.DoesNotExist:
        client = None

    if request.method == 'POST':
        form = forms.ClientForm(request.POST, request.FILES, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.user = request.user
            client.save()
            messages.success(request, 'Профиль успешно обновлен')
            return redirect('profile')
    else:
        form = forms.ClientForm(instance=client)

    return render(request, 'app_client/profile.html', {
        'form': form,
        'client': client
    })

def home(request):
    # Получаем товары со скидкой
    sale_products = Product.objects.filter(
        is_active=True,
        is_on_sale=True,
        discount__isnull=False,
        discount_start_date__lte=timezone.now(),
        discount_end_date__gte=timezone.now()
    )[:6]

    # Получаем новые товары (за последние 7 дней)
    new_products = Product.objects.filter(
        is_active=True,
        created_at__gte=timezone.now() - timezone.timedelta(days=7)
    )[:6]

    return render(request, 'app_client/home.html', {
        'sale_products': sale_products,
        'new_products': new_products
    })

def catalog(request):
    products = Product.objects.filter(is_active=True)
    categories = ProductCategory.objects.all()
    
    # Фильтрация по категории
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Поиск по названию
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    return render(request, 'app_client/catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query
    })

def product_detail(request, pk):
    product = Product.objects.get(pk=pk, is_active=True)
    return render(request, 'app_client/product_detail.html', {
        'product': product
    })