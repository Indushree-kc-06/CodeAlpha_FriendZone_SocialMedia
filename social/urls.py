from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('feed/', views.feed, name='feed'),
    
    path('register/', views.register_view, name='register'),

    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('profile/<str:username>/', views.profile_view, name='profile'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('search/', views.search_users, name='search_users'),

    path('create-post/', views.create_post, name='create_post'),

    path('like/<int:post_id>/', views.like_post, name='like_post'),

    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),

    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),

    path('edit-post/<int:post_id>/', views.edit_post, name='edit_post'),

    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('follow/<str:username>/', views.follow_user, name='follow_user'),

    path('profile/<str:username>/followers/', views.followers_list, name='followers_list'),

    path('profile/<str:username>/following/', views.following_list, name='following_list'),
]