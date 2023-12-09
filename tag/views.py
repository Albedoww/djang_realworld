from django.shortcuts import render

# Create your views here.
from django.db import models
from articles.models import ArticlesInfo
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from itertools import chain


# Create your models here.
class tags(ListModelMixin, GenericViewSet):

    def list(self, request, *args, **kwargs):
        all_taglist=[]
        articles = ArticlesInfo.objects.all()
        for article in articles:
            all_taglist=list(chain(all_taglist,article.taglist))
        all_taglist=list(set(all_taglist))
        return Response({
            'tags':all_taglist
        })