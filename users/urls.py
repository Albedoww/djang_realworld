from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.users),
    path('users/login/', views.login),
    path('user/', views.user.as_view()),

]
