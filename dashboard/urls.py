from django.urls import path
from dashboard import views

app_name = 'dash'
urlpatterns = [
    path('', views.home, name="home"),
    path('users/', views.users, name='users'),
    path('gmail/', views.gmail, name='gmail'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
]
