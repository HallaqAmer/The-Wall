from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.display_form),
    path('logout', views.go_backhome),
    path('adduser', views.create_user),
    path('userlogin', views.login_user),
    path('success', views.success),
]