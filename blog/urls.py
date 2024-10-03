from django.urls import path
from . import views
from .feeds import PostFeed

app_name = 'blog'

urlpatterns = [

    path('', views.home, name='home'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/tag/<str:tag_slug>/', views.post_list, name="posts_by_tag"),
    path("posts/<str:post_slug>/share/", views.post_share, name='post_share'),
    path('posts/<int:year>/<int:month>/<int:day>/<str:post_slug>/',
         views.post_details, name="post_details"),
    path('posts/edit/<int:id>/', views.edit, name='post_edit'),
    path('posts/delete/', views.delete, name='delete_post'),
    path('posts/<str:post_slug>/comments/',
         views.post_comment, name='post_comment'),

    path('feeds/', PostFeed(), name='post_feeds'),
    path('like-archive/', views.like_archive, name='like_archive'),
    path('check-auth/', views.check_auth, name='check_auth'),
    path('file_url_constructor/', views.file_url_constructor,
         name='file_url_constructor'),
]
