from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Создаем профиль пользователя
            UserProfile.objects.create(user=user)
            
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'avatar', 'bio')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from .models import Advertisement, Category

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('title', 'category', 'description', 'price', 'contact_info', 'location')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap для стилизации формы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class AdvertisementSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Поиск')
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Категория',
        empty_label='Все категории'
    )
    min_price = forms.DecimalField(required=False, label='Цена от')
    max_price = forms.DecimalField(required=False, label='Цена до')
    location = forms.CharField(required=False, label='Местоположение')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap для стилизации формы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
