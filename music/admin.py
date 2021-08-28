from django.contrib import admin

# Register your models here.
from music.models import Song
from music.models import Musician
from music.models import Review

admin.site.register(Song)
admin.site.register(Musician)
admin.site.register(Review)
