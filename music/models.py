from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=100, verbose_name='tytuł')
    musician = models.ManyToManyField(to='music.Musician', verbose_name='wykonawcy', related_name='songs')
    short_description = models.TextField(verbose_name='opis')
    published_at = models.DateField(verbose_name='data publikacji', blank=True, null=True)
    text_link = models.CharField(max_length=150, default='No link', verbose_name='link do tekstu')
    added_by = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='songs', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='song_likes', blank=True)

    class Meta:
        verbose_name = 'piosenka'
        verbose_name_plural = 'piosenki'
    
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return 'Piosenka: ' + self.title


class Musician(models.Model):
    name = models.CharField(max_length=100, verbose_name='nazwa')
    about = models.TextField(verbose_name='opis', blank=True)
    photo = models.ImageField(verbose_name='zdjęcie', blank=True)

    class Meta:
        verbose_name = 'wykonawca'
        verbose_name_plural = 'wykonawcy'
    
    def __str__(self):
        return 'Wykonawca: ' + self.name

    def get_absolute_url(self):
        return reverse('musician_detail', args=[str(self.id)])


class Review(models.Model):
    song = models.ForeignKey(to=Song, on_delete=models.CASCADE, related_name='reviews')
    author = models.CharField(max_length=150)
    content = models.TextField()
    is_recommended = models.BooleanField()
    
    class Meta:
        verbose_name = 'recenzja'
        verbose_name_plural = 'recenzje'
