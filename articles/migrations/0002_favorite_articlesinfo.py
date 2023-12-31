# Generated by Django 4.2.8 on 2023-12-09 05:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Favorite_ArticlesInfo",
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
                    "hariticle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="articles.articlesinfo",
                        verbose_name="文章外键",
                    ),
                ),
                (
                    "huser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="原用户外键",
                    ),
                ),
            ],
            options={
                "verbose_name": "喜欢的文章",
                "verbose_name_plural": "喜欢的文章",
                "db_table": "Favorite_Articles",
            },
        ),
    ]
