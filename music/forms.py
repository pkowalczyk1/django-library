from django import forms
from music.models import Song, Musician

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('title', 'musician', 'short_description', 'published_at', 'text_link')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'musician': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control'}),
            'published_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'text_link': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MusicianForm(forms.ModelForm):
    class Meta:
        model = Musician
        fields = ('name', 'about', 'photo')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'about': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'}),
        }
