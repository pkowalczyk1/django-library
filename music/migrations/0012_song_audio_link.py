# Generated by Django 3.2.6 on 2021-09-21 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0011_alter_song_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='audio_link',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='link do muzyki'),
        ),
    ]
