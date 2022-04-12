from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('new/', views.post_create, name='ask_question'),
    path('<slug:post>/edit/', views.post_edit, name='edit_question'),
    path('<slug:post>/del/',views.deletePost, name='del_question'),
    path('search/', views.post_search, name='post_search'),
    path('<slug:post>/', views.post_single, name='post_single'),
]

