# Generated by Django 4.2.8 on 2023-12-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "username",
                    models.CharField(max_length=256, unique=True, verbose_name="用户名"),
                ),
                ("email", models.CharField(max_length=256, verbose_name="邮箱")),
                ("password", models.CharField(max_length=256, verbose_name="密码")),
                ("bio", models.CharField(max_length=256, null=True, verbose_name="爱好")),
                (
                    "image",
                    models.ImageField(null=True, upload_to="users", verbose_name="头像"),
                ),
            ],
            options={
                "verbose_name": "用户",
                "verbose_name_plural": "用户",
                "db_table": "users",
            },
        ),
    ]
