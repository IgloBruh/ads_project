from django.urls import path
from . import views

app_name = 'advertisements'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('advertisement/create/', views.advertisement_create, name='advertisement_create'),
    path('advertisement/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('advertisement/<int:pk>/edit/', views.advertisement_edit, name='advertisement_edit'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('search/', views.search_advertisements, name='search'),
]
