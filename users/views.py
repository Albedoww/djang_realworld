from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import UserInfo
import json
from django.views.generic import View
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import UserInfoSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
def users(request):#注册
    json_bytes = request.body
    json_str = json_bytes.decode()
    user_dict = json.loads(json_str)
    user=UserInfo.objects.create(
     username=user_dict.get( 'username'),
     email=user_dict.get( 'email'),
     password=user_dict.get('password'),

    )
    user.token= get_tokens_for_user(user)
    user.save()
    return JsonResponse({
        'username':user.username,
        'email':user.email,
        "bio": user.bio,
        'image': user.image.url if user.image else '',
        'refresh':user.token['refresh'],
        'access': user.token['access'],
    },status=201)
def login(request):
    json_bytes_username=(json.loads((request.body).decode())).get('username')
    json_bytes_password=(json.loads((request.body).decode())).get('password')
    try:
        user=UserInfo.objects.get(username=json_bytes_username)
        user.token=request.META['HTTP_AUTHORIZATION']
    except UserInfo.DoesNotExist:
        return HttpResponse(status=404)
    if user.password!=json_bytes_password:
        return HttpResponse(status=404)
    return JsonResponse({
        'username':user.username,
        'email':user.email,
        "bio": user.bio,
        'token':user.token,
        'image': user.image.url if user.image else ''

    },status=201)
class user(APIView):
    permission_classes = (IsAuthenticated,)

    serializer_class=UserInfoSerializer
    def get(self,request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self,request):
        user = UserInfo.objects.get(username=request.data.get('username'))
        token_str = user.token.replace("'", '"')
        token = json.loads(token_str)
        if token['access'] == (request.META['HTTP_AUTHORIZATION'])[7:]:
            try:
             user=UserInfo.objects.get(username=request.data.get('username'))
            except UserInfo.DoesNotExist:
             return HttpResponse(status=404)
            serializer = self.serializer_class(instance=user,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=user,validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('没有权限')


# Create your views here.
