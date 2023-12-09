from django.db import models
from users.models import UserInfo
# Create your models here.
class Following_User_Info(models.Model):
    username = models.CharField(max_length=256, verbose_name='用户名')
    bio= models.CharField(max_length=256,null=True, verbose_name='爱好')
    image=models.ImageField(upload_to='users',verbose_name="头像",null=True)
    follow=models.BooleanField(default=False,verbose_name="关注")
    huser=models.ForeignKey(UserInfo,on_delete=models.CASCADE,verbose_name="原用户")
    class Meta:
        db_table = 'following_users'  # 指明数据库表名
        verbose_name = '关注的人'  # 在admin站点中显示的名称
        verbose_name_plural = verbose_name  # 显示的复数名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.username

