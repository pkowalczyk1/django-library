from django import forms
from music.models import Song, Musician
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=120, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=120, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
