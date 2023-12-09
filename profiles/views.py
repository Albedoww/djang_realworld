from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import UserInfo
from .models import Following_User_Info
from .serializer import Following_User_InfoSerializer,UserInfoSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_204_NO_CONTENT

# Create your views here.
class profiles(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly ,)

    def get(self,request,username):
        users=UserInfo.objects.get(username=username)
        return Response(UserInfoSerializer(users).data)
class follow(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request,username):
        users=UserInfo.objects.get(username=username)
        users.follow=True
        users.huser=request.user.id
        if Following_User_Info.objects.filter(username=username,huser=users.huser):
            return Response('重复关注')
        following_user=Following_User_InfoSerializer(users)
        following_user=Following_User_InfoSerializer(data=following_user.data)
        following_user.is_valid(raise_exception=True)
        following_user.save()
        profile=following_user.data
        profile.pop('huser')
        return Response(profile)

    def delete(self, request,username):
        following_user=Following_User_Info.objects.filter(username=username,huser=request.user.id)
        following_user.delete()
        return Response(status=HTTP_204_NO_CONTENT)