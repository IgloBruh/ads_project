from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils.text import slugify
from .forms import UserRegistrationForm, UserProfileForm, LoginForm, AdvertisementForm, AdvertisementSearchForm
from .models import UserProfile, Advertisement, Category
import random
import string

def index(request):
    advertisements = Advertisement.objects.filter(status='active').order_by('-created')[:10]
    categories = Category.objects.all()
    
    form = AdvertisementSearchForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        location = form.cleaned_data.get('location')
        
        if query:
            advertisements = advertisements.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        if category:
            advertisements = advertisements.filter(category=category)
        if min_price:
            advertisements = advertisements.filter(price__gte=min_price)
        if max_price:
            advertisements = advertisements.filter(price__lte=max_price)
        if location:
            advertisements = advertisements.filter(location__icontains=location)
    
    return render(request, 'advertisements/index.html', {
        'title': 'Доска объявлений',
        'advertisements': advertisements,
        'categories': categories,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('advertisements:profile')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'advertisements/register.html', {
        'form': form,
        'title': 'Регистрация'
    })

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему!')
                return redirect('advertisements:index')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()
    
    return render(request, 'advertisements/login.html', {
        'form': form,
        'title': 'Вход'
    })

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('advertisements:index')

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('advertisements:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    user_advertisements = Advertisement.objects.filter(author=request.user).order_by('-created')
    
    return render(request, 'advertisements/profile.html', {
        'form': form,
        'profile': profile,
        'title': 'Профиль пользователя',
        'user_advertisements': user_advertisements
    })

def generate_unique_slug(title, model_class):
    """Генерирует уникальный slug для объявления"""
    slug = slugify(title)
    if not slug:
        # Если slugify не смог создать slug из заголовка, генерируем случайный
        slug = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    
    unique_slug = slug
    num = 1
    while model_class.objects.filter(slug=unique_slug).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    
    return unique_slug

@login_required
def advertisement_create(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.author = request.user
            advertisement.slug = generate_unique_slug(advertisement.title, Advertisement)
            advertisement.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('advertisements:advertisement_detail', advertisement.id)
    else:
        form = AdvertisementForm()
    
    return render(request, 'advertisements/advertisement_form.html', {
        'form': form,
        'title': 'Создание объявления'
    })

@login_required
def advertisement_edit(request, pk):
    advertisement = get_object_or_404(Advertisement, id=pk, author=request.user)
    
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('advertisements:advertisement_detail', pk)
    else:
        form = AdvertisementForm(instance=advertisement)
    
    return render(request, 'advertisements/advertisement_form.html', {
        'form': form,
        'title': 'Редактирование объявления',
        'advertisement': advertisement
    })

def advertisement_detail(request, pk):
    advertisement = get_object_or_404(Advertisement, id=pk)
    return render(request, 'advertisements/advertisement_detail.html', {
        'advertisement': advertisement,
        'title': advertisement.title
    })

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'advertisements/category_list.html', {
        'categories': categories,
        'title': 'Категории объявлений'
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    advertisements = Advertisement.objects.filter(category=category, status='active').order_by('-created')
    
    return render(request, 'advertisements/category_detail.html', {
        'category': category,
        'advertisements': advertisements,
        'title': category.name
    })

def search_advertisements(request):
    form = AdvertisementSearchForm(request.GET)
    advertisements = Advertisement.objects.filter(status='active')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        location = form.cleaned_data.get('location')
        
        if query:
            advertisements = advertisements.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        if category:
            advertisements = advertisements.filter(category=category)
        if min_price:
            advertisements = advertisements.filter(price__gte=min_price)
        if max_price:
            advertisements = advertisements.filter(price__lte=max_price)
        if location:
            advertisements = advertisements.filter(location__icontains=location)
    
    return render(request, 'advertisements/search_results.html', {
        'advertisements': advertisements,
        'form': form,
        'title': 'Результаты поиска'
    })
