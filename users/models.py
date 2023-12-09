from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser,models.Model):
    username = models.CharField(unique=True,max_length=254, verbose_name='用户名')
    email = models.CharField(max_length=256, verbose_name='邮箱')
    password = models.CharField(max_length=256, verbose_name='密码')
    bio= models.CharField(max_length=256,null=True, verbose_name='爱好')
    image=models.ImageField(upload_to='users',verbose_name="头像",null=True)
    token = models.TextField(verbose_name='token',default="")
    class Meta:
        db_table = 'users'  # 指明数据库表名
        verbose_name = '用户'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.username
# Create your models here.
