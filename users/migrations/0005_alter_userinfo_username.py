# Generated by Django 4.2.8 on 2023-12-07 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_userinfo_managers_userinfo_date_joined_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="username",
            field=models.CharField(max_length=254, unique=True, verbose_name="用户名"),
        ),
    ]