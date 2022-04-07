from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('<slug:post>/', views.post_single, name='post_single'),
]

