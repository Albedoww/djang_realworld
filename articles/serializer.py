from rest_framework import serializers
from .models import ArticlesInfo,Favorite_ArticlesInfo,CommentsInfo

class ArticlesInfoSerializer(serializers.ModelSerializer):
        class Meta:
                model = ArticlesInfo
                exclude = ('createdAt','updatedAt','favorited')


class ALLFlield_ArticlesInfoSerializer(serializers.ModelSerializer):
        class Meta:
                model = ArticlesInfo
                fields ='__all__'
                read_only_fields = ('createdAt', 'updatedAt', 'favorited','favoritesCount','author','taglist','slug','authorkey')

class Favorite_ArticlesInfoSerializer(serializers.ModelSerializer):
        class Meta:
                model = Favorite_ArticlesInfo
                fields = '__all__'

class CommentsInfoSerializer(serializers.ModelSerializer):
        class Meta:
                model = CommentsInfo
                fields = '__all__'
