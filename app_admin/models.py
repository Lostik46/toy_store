from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_russian_mobile(value):
    try:
        phone = phonenumbers.parse(value, "RU")
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError("Номер телефона недействителен.")
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("Неверный формат номера телефона.")

cyrillic_validator = RegexValidator(
    regex=r'^[а-яА-ЯёЁ\s]+$', 
)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Псевдоним')
    first_name = models.CharField(max_length=250, validators=[cyrillic_validator], verbose_name='Имя')
    last_name = models.CharField(max_length=250, validators=[cyrillic_validator], verbose_name='Фамилия')
    mobile = models.CharField(max_length=11, null=False, validators=[validate_russian_mobile], verbose_name='Мобильный телефон')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='Электронная почта')
    address = models.CharField(max_length=40, null=True, blank=True, verbose_name='Адрес')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, default='profile_images/default.jpg', verbose_name='Фото профиля')

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
    
    def get_name(self):
        return f"{self.first_name} {self.last_name}"

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='Название категории')
    short_description = models.CharField(max_length=200, verbose_name='Краткое описание')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    short_description = models.TextField(verbose_name='Краткое описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', 
                            null=True, blank=True, default='products/default.jpg')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_on_sale = models.BooleanField(default=False, verbose_name='По акции')
    discount = models.IntegerField(null=True, blank=True, verbose_name='Скидка (%)')
    discount_start_date = models.DateField(null=True, blank=True, verbose_name='Дата начала акции')
    discount_end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания акции')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']  # Сортировка по умолчанию - сначала новые товары

    @property
    def sale_price(self):
        if self.is_on_sale:
            discount_amount = (self.price * self.discount) / 100
            return round(self.price - discount_amount, 2)
        return self.price
