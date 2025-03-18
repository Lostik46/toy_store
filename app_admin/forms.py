from django import forms
from django.contrib.auth import authenticate
from .models import Product, ProductCategory

class LoginForm(forms.Form):
    username = forms.CharField(label='Псевдоним')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError('Неверный псевдоним или пароль')
        return cleaned_data

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ['category_name', 'short_description']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'short_description', 'price', 'image', 
                 'is_on_sale', 'discount', 'discount_start_date', 'discount_end_date']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля скидки необязательными
        self.fields['discount'].required = False
        self.fields['discount_start_date'].required = False
        self.fields['discount_end_date'].required = False
        
        # Добавляем классы Bootstrap для стилизации
        for field in self.fields:
            if isinstance(self.fields[field], forms.BooleanField):
                self.fields[field].widget.attrs['class'] = 'form-check-input'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'
        
        # Специальные настройки для полей
        self.fields['description'].widget = forms.Textarea(attrs={'rows': 4})
        self.fields['short_description'].widget = forms.Textarea(attrs={'rows': 2})
        self.fields['discount_start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['discount_end_date'].widget = forms.DateInput(attrs={'type': 'date'})

    def clean(self):
        cleaned_data = super().clean()
        is_on_sale = cleaned_data.get('is_on_sale')
        
        if is_on_sale:
            # Проверяем обязательные поля только если товар по акции
            discount = cleaned_data.get('discount')
            discount_start_date = cleaned_data.get('discount_start_date')
            discount_end_date = cleaned_data.get('discount_end_date')
            
            if not discount:
                self.add_error('discount', 'Это поле обязательно для товаров по акции')
            if not discount_start_date:
                self.add_error('discount_start_date', 'Это поле обязательно для товаров по акции')
            if not discount_end_date:
                self.add_error('discount_end_date', 'Это поле обязательно для товаров по акции')
            
            # Проверка корректности дат
            if discount_start_date and discount_end_date and discount_start_date > discount_end_date:
                self.add_error('discount_end_date', 'Дата окончания акции должна быть позже даты начала')
        
        return cleaned_data
