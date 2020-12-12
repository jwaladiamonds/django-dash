from django.urls import path, include
from accounts import views

app_name = 'auth'
urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('force_logout/<username>', views.user_force_logout, name='force_logout'),
    path('enable/<username>', views.user_enable, name='enable'),
    path('disable/<username>', views.user_disable, name='disable'),
    path('delete/<username>', views.user_delete, name='delete'),
    path('verify/<username>/<token>', views.user_verify_email, name='verify_email'),
    path('gmail/', include('gmailer.urls')),
]
