from django.shortcuts import render
from django.http import HttpResponse
from music.models import Song
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout

# Create your views here.

def main_page(request):
    return render(request, template_name='index.html')


def songs_list(request):
    songs = Song.objects.all()
    return render(request, template_name='songs_list.html', context={'songs': songs})


def profile_view(request):
    return render(request, template_name='registration/profile.html')


def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, template_name='registration/signup_complete.html')
    else:
        form = UserCreationForm()
    
    return render(request, template_name='registration/signup.html', context={'form': form})


def logout_view(request):
    logout(request)
    return render(request, template_name='index.html')
