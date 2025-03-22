from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL категории')
    description = models.TextField(blank=True, verbose_name='Описание категории')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('advertisements:category_detail', args=[self.slug])

class Advertisement(models.Model):
    STATUS_CHOICES = (
        ('active', 'Активно'),
        ('pending', 'На модерации'),
        ('closed', 'Закрыто'),
    )
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique_for_date='created', verbose_name='URL объявления')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisements', verbose_name='Автор')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='advertisements', verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    contact_info = models.CharField(max_length=255, verbose_name='Контактная информация')
    location = models.CharField(max_length=100, verbose_name='Местоположение')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('advertisements:advertisement_detail', args=[self.created.year,
                                                                   self.created.month,
                                                                   self.created.day,
                                                                   self.slug])

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, null=True, verbose_name='О себе')
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'Профиль пользователя {self.user.username}'
