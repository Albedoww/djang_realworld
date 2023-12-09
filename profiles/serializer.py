from rest_framework import serializers
from .models import Following_User_Info
from users.models import UserInfo

class UserInfoSerializer(serializers.ModelSerializer):
        following = serializers.BooleanField(default=False,label='关注', allow_null=True)
        class Meta:
                model = UserInfo
                fields = ('username', 'bio', 'image', 'following')
class Following_User_InfoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Following_User_Info
                fields = ('username','bio','image','follow','huser')
