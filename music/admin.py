from django.contrib import admin

# Register your models here.
from music.models import Song

admin.site.register(Song)
