# Generated by Django 4.2.8 on 2023-12-09 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0002_favorite_articlesinfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="favorite_articlesinfo",
            name="slug",
            field=models.CharField(
                default=1, max_length=256, unique=True, verbose_name="标称"
            ),
            preserve_default=False,
        ),
    ]
