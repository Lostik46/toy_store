from django import forms
from django.contrib.auth.models import User
from app_admin.models import Client

class ClientUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    
    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': 'Имя пользователя'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'mobile', 'email', 'address', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7XXXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
