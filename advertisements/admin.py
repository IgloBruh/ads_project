from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Category, Advertisement, UserProfile

# Настройка заголовка и названия админ-панели
admin.site.site_header = 'Администрирование сайта объявлений'
admin.site.site_title = 'Панель администратора'
admin.site.index_title = 'Управление сайтом объявлений'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'advertisement_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def advertisement_count(self, obj):
        return obj.advertisements.count()
    advertisement_count.short_description = 'Количество объявлений'

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'

# Расширяем стандартную админку пользователей
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'view_profile')
    
    def view_profile(self, obj):
        if hasattr(obj, 'profile'):
            url = reverse('admin:advertisements_userprofile_change', args=[obj.profile.id])
            return format_html('<a href="{}">Просмотр профиля</a>', url)
        return "Нет профиля"
    view_profile.short_description = 'Профиль'

# Перерегистрируем модель User с нашей кастомной админкой
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_link', 'category_link', 'price', 'status', 'created', 'updated')
    list_filter = ('status', 'created', 'category')
    search_fields = ('title', 'description', 'author__username', 'location')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created'
    list_editable = ('status',)
    list_per_page = 20
    readonly_fields = ('created', 'updated')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'author', 'category', 'description')
        }),
        ('Детали объявления', {
            'fields': ('price', 'contact_info', 'location')
        }),
        ('Статус и даты', {
            'fields': ('status', 'created', 'updated')
        }),
    )
    
    def author_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.author.id])
        return format_html('<a href="{}">{}</a>', url, obj.author.username)
    author_link.short_description = 'Автор'
    
    def category_link(self, obj):
        url = reverse('admin:advertisements_category_change', args=[obj.category.id])
        return format_html('<a href="{}">{}</a>', url, obj.category.name)
    category_link.short_description = 'Категория'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если это новое объявление
            obj.status = 'active'  # Автоматически устанавливаем статус "активно" для админов
        super().save_model(request, obj, form, change)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'has_avatar')
    search_fields = ('user__username', 'user__email', 'phone')
    raw_id_fields = ('user',)
    
    def has_avatar(self, obj):
        return bool(obj.avatar)
    has_avatar.boolean = True
    has_avatar.short_description = 'Аватар'

# Отключаем отображение групп в админке, если они не используются
admin.site.unregister(Group)
