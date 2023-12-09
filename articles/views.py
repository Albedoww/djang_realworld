import json


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,CreateModelMixin
from .serializer import ArticlesInfoSerializer,ALLFlield_ArticlesInfoSerializer,CommentsInfoSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.response import Response
from users.models import UserInfo
from .models import ArticlesInfo,Favorite_ArticlesInfo,CommentsInfo
from django.db.models import Max
import json
from profiles.models import Following_User_Info
from profiles.serializer import Following_User_InfoSerializer
from django.db.models import F

# Create your views here.
class articles(RetrieveModelMixin,ListModelMixin,CreateModelMixin,GenericViewSet):
  serializer_class = ArticlesInfoSerializer
  permission_classes = (IsAuthenticatedOrReadOnly,)
  def articlesCount(self,all_Articles):
      return len(all_Articles)
  def retrieve(self, request, *args, **kwargs):
             New_Article = ArticlesInfo.objects.aggregate(Max('createdAt'))
             all=ArticlesInfo.objects.get(createdAt=New_Article['createdAt__max'])
             all_ArticlesInfoSerializer = ALLFlield_ArticlesInfoSerializer(all)
             return Response(all_ArticlesInfoSerializer.data)

  def list(self, request, *args, **kwargs):
      if request.user.username == '':
          return self.retrieve(request)
      else:
          params=request.query_params
          if params=={}:
            all=ArticlesInfo.objects.all().order_by('-createdAt')
            all_ArticlesInfoSerializer = ALLFlield_ArticlesInfoSerializer(all,many=True)
          else:
              all = ArticlesInfo.objects.all().order_by('-createdAt')
              if params.get('tag'):
                  all = all.filter(taglist__contains=params['tag'])
              if params.get('author'):
                  all = all.filter(author__username=params['author'])
              if params.get('favorited'):
                  all = all.filter(favorite_articlesinfo__huser_id=request.user.id)
              if params.get('offset') or params.get('limit'):
                  if params.get('offset'):
                      offset=params.get('offset')
                  else:
                      offset =0
                  if params.get('limit'):
                      limit=params.get('limit')
                  else:
                      limit =20
                  all = all[int(offset):int(offset)+int(limit)]
              all_ArticlesInfoSerializer = ALLFlield_ArticlesInfoSerializer(all, many=True)
          dict_all={'articles':all_ArticlesInfoSerializer.data,"articlesCount": self.articlesCount(all_ArticlesInfoSerializer.data)}
          return Response(dict_all)

  def create(self, request, *args, **kwargs):
          user=UserInfo.objects.get(username=request.user.username)
          request.data['authorkey'] = user.id
          author=Following_User_Info.objects.filter(username=request.user.username).first()
          author_json=Following_User_InfoSerializer(author)
          author_json=author_json.data
          author_json.pop('huser')
          request.data['author']=author_json
          serializer = self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          self.perform_create(serializer)
          all = ArticlesInfo.objects.get(id=serializer.data['id'])
          all_ArticlesInfoSerializer=ALLFlield_ArticlesInfoSerializer(all)
          headers = self.get_success_headers(serializer.data)
          return Response(all_ArticlesInfoSerializer.data, status=status.HTTP_201_CREATED, headers=headers)

class feed(ListModelMixin,GenericViewSet):
    serializer_class = ALLFlield_ArticlesInfoSerializer
    permission_classes = (IsAuthenticated,)

    def articlesCount(self, all_Articles):
        return len(all_Articles)


    def list(self, request, *args, **kwargs):
        params = request.query_params
        Following_list=[]
        Following_Users=Following_User_Info.objects.filter(huser=request.user.id)
        for Following_User in Following_Users:
            Following_list.append(Following_User.username)

        all = ArticlesInfo.objects.filter(authorkey__username__in=Following_list).order_by('-createdAt')
        if params.get('tag'):
            all = all.filter(taglist__contains=params['tag'])
        if params.get('author'):
            all = all.filter(author__username=params['author'])
        if params.get('favorited'):
            all = all.filter(favorite_articlesinfo__huser_id=request.user.id)
        if params.get('offset') or params.get('limit'):
            if params.get('offset'):
                offset = params.get('offset')
            else:
                offset = 0
            if params.get('limit'):
                limit = params.get('limit')
            else:
                limit = 20
            all = all[int(offset):int(offset) + int(limit)]
        all_ArticlesInfoSerializer = ALLFlield_ArticlesInfoSerializer(all, many=True)

        dict_all = {'articles': all_ArticlesInfoSerializer.data,
                "articlesCount": self.articlesCount(all_ArticlesInfoSerializer.data)}
        return Response(dict_all)

class slug(RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,GenericViewSet):
    queryset = ArticlesInfo.objects.all()
    serializer_class = ALLFlield_ArticlesInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'slug'
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user=UserInfo.objects.get(id=instance.author.id)
        token_str=user.token.replace("'",'"')
        token=json.loads(token_str)
        if token['access']==(request.META['HTTP_AUTHORIZATION'])[7:]:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)
        else:
            return Response('没有权限')

    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            user = UserInfo.objects.get(id=instance.author.id)
            token_str = user.token.replace("'", '"')
            token = json.loads(token_str)
            if token['access'] == (request.META['HTTP_AUTHORIZATION'])[7:]:
               instance = self.get_object()
               self.perform_destroy(instance)
               return Response(status=status.HTTP_204_NO_CONTENT)

            else:
               return Response('没有权限')


class comment(CreateModelMixin,ListModelMixin,GenericViewSet):
    queryset = CommentsInfo.objects.all()
    serializer_class = CommentsInfoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        article=ArticlesInfo.objects.get(slug=kwargs['slug'])
        data=request.data
        data['hariticle']=article.id
        data['authorkey']=request.user.id
        author = Following_User_Info.objects.filter(username=request.user.username).first()
        author_json = Following_User_InfoSerializer(author)
        author_json = author_json.data
        data['author']=author_json
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class delete_comment(DestroyModelMixin,GenericViewSet):
    queryset = CommentsInfo.objects.all()
    serializer_class = CommentsInfoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = UserInfo.objects.get(id=instance.authorkey.id)
        token_str = user.token.replace("'", '"')
        token = json.loads(token_str)
        if token['access'] == (request.META['HTTP_AUTHORIZATION'])[7:]:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response('没有权限')


class favorite(DestroyModelMixin,CreateModelMixin,GenericViewSet):
    queryset = Favorite_ArticlesInfo.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        article=ArticlesInfo.objects.get(slug=kwargs['slug'])
        article_slug=article.slug
        user=UserInfo.objects.get(id=request.user.id)
        if Favorite_ArticlesInfo.objects.filter(huser_id=request.user.id, slug=article.slug):
            return Response('重复关注')
        favorite_article=Favorite_ArticlesInfo.objects.create(
            slug=article_slug,
            hariticle=article,
            huser = user
        )
        article.favoritesCount+=1
        article.save()
        article.favorited=True
        article=ALLFlield_ArticlesInfoSerializer(article)
        return Response(article.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        article=ArticlesInfo.objects.get(slug=kwargs['slug'])
        article.favoritesCount -= 1
        article=Favorite_ArticlesInfo.objects.filter(slug=kwargs['slug'],huser_id=request.user.id)
        article.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)