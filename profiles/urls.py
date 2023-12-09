from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path('profiles/(?P<username>\w+)$', views.profiles.as_view()),
    re_path(r'profiles/(?P<username>\w+)/follow/', views.follow.as_view()),

]
