from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('<slug:slug>/', views.view_user_profile, name='view_user_profile'),
    path('<slug:slug>/<int:year>/', views.view_user_profile_year, name='view_user_profile_year'),
    path('settings/profile/', views.profile_settings, name='profile_settings'),
    # path('profile/<slug:slug>/', views.user_profile, name='user_profile'),
    path('leaderboard', views.leaderboard, name='leaderboard'),
]