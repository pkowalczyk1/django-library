from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=100)
    musician = models.ManyToManyField(to='music.Musician', verbose_name='wykonawcy', related_name='music')
    short_description = models.TextField()
    published_at = models.DateField()
    text_link = models.CharField(max_length=150, default='No link')

    def __str__(self):
        return 'Piosenka: ' + self.title


class Musician(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    photo = models.ImageField()

    class Meta:
        verbose_name = 'wykonawca'
        verbose_name_plural = 'wykonawcy'
    
    def __str__(self):
        return 'Wykonawca: ' + self.name


class Review(models.Model):
    song = models.ForeignKey(to=Song, on_delete=models.CASCADE)
    author = models.CharField(max_length=150)
    content = models.TextField()
    is_recommended = models.BooleanField()
    
    class Meta:
        verbose_name = 'recenzja'
        verbose_name_plural = 'recenzje'
