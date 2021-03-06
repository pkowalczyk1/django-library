# Generated by Django 3.2.6 on 2021-09-07 10:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0009_alter_song_published_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='song_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
