from django.urls import path
from . import views


urlpatterns = [
    path('post/new/', views.post_new, name='post_new'),
    path('', views.post_list, name='post_list'),
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    path('post/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path('user/signup/', views.signup, name='signup'),
    path('user/login/', views.log_in, name='login'),
    path('user/logout/', views.log_out, name='logout'),
    path('category/<str:slug>/', views.category, name='category_detail'),
    path('tag/<str:slug>/', views.tag, name='tag_detail'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
