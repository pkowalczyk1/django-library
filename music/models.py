from django.db import models

# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    short_description = models.TextField()
    published_at = models.DateField()
    text_link = models.CharField(max_length=150, default='No link')

    def __str__(self):
        return 'Piosenka: ' + self.title
