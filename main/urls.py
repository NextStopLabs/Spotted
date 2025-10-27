from django.contrib.auth import views as auth_views
from django.urls import path
from .views import *
from posts.views import create_post

urlpatterns = [
    path('', home, name='home'),
    path('api/following_feed/', following_feed_api, name='following_feed_api'),
    path('api/following/', following_api, name='following_api'),
    path('u/register/', register, name='register'),
    path('u/login/', auth_views.LoginView.as_view(), name='login'),
    path('u/<str:username>/', user_profile, name='user_profile'),
    path('accounts/register/', register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/<str:username>/', user_profile, name='user_profile'),
    path('post/create/', create_post, name='create_post'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', add_comment, name='add_comment'),
    path('post/<slug:slug>/like/', toggle_like, name='toggle_like'),
    path('post/<slug:slug>/dislike/', toggle_dislike, name='toggle_dislike'),
    path('follow/<str:username>/', toggle_follow, name='toggle_follow'),
]
