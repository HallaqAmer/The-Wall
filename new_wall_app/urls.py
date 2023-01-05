from django.urls import path
from . import views
from django.contrib.sessions.models import Session

app_name = 'wall'

urlpatterns = [

    path('', views.display_wall),
    path('post/message', views.post_message, name="message"),
    path('comment', views.add_comment, name="comment"),
    path('delete', views.delete_message, name="delete"),

]