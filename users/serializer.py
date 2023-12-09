from rest_framework import serializers
from .models import UserInfo
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserInfoSerializer(serializers.Serializer):
        token=serializers.CharField(label='token',read_only=True)
        id = serializers.IntegerField(label='ID', read_only=True)
        username = serializers.CharField(max_length=256, label='用户名',required=False)
        email = serializers.CharField(max_length=256, label='邮箱',required=False)
        bio = serializers.CharField(max_length=256, label='爱好',required=False)
        image = serializers.ImageField(required=False, label="头像")

        def save(self, **kwargs):
                user = UserInfo.objects.create(**kwargs)
                return user
        def update(self, instance, validated_data):
                instance.username=validated_data.get('username')
                instance.email = validated_data.get('email')
                instance.password = validated_data.get('password')
                instance.bio = validated_data.get('bio')
                instance.image = validated_data.get('image')
                instance.save()
                return instance


