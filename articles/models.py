from django.db import models
from django.contrib.postgres.fields import ArrayField
from users.models import UserInfo
# Create your models here.

class ArticlesInfo(models.Model):
    slug = models.CharField(unique=True,verbose_name='标称',max_length=256)
    title = models.CharField(verbose_name='标题',max_length=256)
    description = models.CharField(verbose_name='描述',max_length=256)
    body = models.TextField(verbose_name='主体内容')
    createdAt = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    updatedAt = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    favorited = models.BooleanField(default=False,verbose_name='喜欢',null=False)
    favoritesCount =models.IntegerField(default=0,verbose_name='被喜欢次数')
    author = models.JSONField(verbose_name="原用户",default=dict)
    taglist = models.JSONField(verbose_name='标签表',default=list)
    authorkey = models.ForeignKey(UserInfo,verbose_name="原用户外键",on_delete=models.CASCADE)
    class Meta:
        db_table = 'article'  # 指明数据库表名
        verbose_name = '文章'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.title

class Favorite_ArticlesInfo(models.Model):
    slug = models.CharField(verbose_name='标称',max_length=256)
    hariticle=models.ForeignKey(ArticlesInfo,verbose_name='文章外键',on_delete=models.CASCADE)
    huser=models.ForeignKey(UserInfo,verbose_name="原用户外键",on_delete=models.CASCADE)
    class Meta:
        db_table = 'Favorite_Articles'  # 指明数据库表名
        verbose_name = '喜欢的文章'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

class CommentsInfo(models.Model):
    body = models.TextField(verbose_name='主体内容')
    createdAt = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    updatedAt = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    author = models.JSONField(verbose_name="原用户",default=dict)
    hariticle=models.ForeignKey(ArticlesInfo,verbose_name='文章外键',on_delete=models.CASCADE)
    authorkey = models.ForeignKey(UserInfo,verbose_name="原用户外键",on_delete=models.CASCADE)
    class Meta:
        db_table = 'comment'  # 指明数据库表名
        verbose_name = '评论'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称
