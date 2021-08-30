from django.contrib import admin

# Register your models here.
from music.models import Song
from music.models import Musician
from music.models import Review

class SongAdmin(admin.ModelAdmin):
    exclude = ('added_by',)
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Song, SongAdmin)
admin.site.register(Musician)
admin.site.register(Review)