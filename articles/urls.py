from django.urls import re_path
from . import views

urlpatterns = [
    re_path('articles/$', views.articles.as_view({'get': 'list','post':'create'})),
    re_path('articles/feed/$',views.feed.as_view({'get': 'list'})),
    re_path('articles/(?P<slug>[-\w]+)/$', views.slug.as_view({'get': 'retrieve','put':'update','delete':'destroy'})),
    re_path('articles/(?P<slug>[-\w]+)/comments/$',views.comment.as_view({'get': 'list','post':'create'}) ),
    re_path('articles/(?P<slug>[-\w]+)/comments/(?P<id>\w+)/$',views.delete_comment.as_view({'delete':'destroy'}) ),
    re_path('articles/(?P<slug>[-\w]+)/favorite/$',views.favorite.as_view({'delete':'destroy','post':'create'}) ),

]