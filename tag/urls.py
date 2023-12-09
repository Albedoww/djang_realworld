from django.urls import re_path
from . import views

urlpatterns = [
    re_path('tags/$', views.tags.as_view({'get': 'list'})),

]