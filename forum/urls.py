from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('question/<int:id>', views.questionpage, name='question'),
    path('new-question', views.newquestionpage, name='new-question'),
    path('reply', views.replypage, name='reply')
]