# Generated by Django 4.2.8 on 2023-12-09 06:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0004_alter_favorite_articlesinfo_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="CommentsInfo",
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
                ("body", models.TextField(verbose_name="主体内容")),
                (
                    "createdAt",
                    models.DateTimeField(auto_now_add=True, verbose_name="创建时间"),
                ),
                ("updatedAt", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("author", models.JSONField(default=dict, verbose_name="原用户")),
                (
                    "authorkey",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="原用户外键",
                    ),
                ),
                (
                    "hariticle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="articles.articlesinfo",
                        verbose_name="文章外键",
                    ),
                ),
            ],
            options={
                "verbose_name": "评论",
                "verbose_name_plural": "评论",
                "db_table": "comment",
            },
        ),
    ]
