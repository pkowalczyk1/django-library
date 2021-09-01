from django.shortcuts import render
from django.http import HttpResponse
from music.models import Song, Musician
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from music.forms import SongForm, MusicianForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django import http

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


class SongCreate(LoginRequiredMixin, CreateView):
    form_class = SongForm
    template_name = 'song_create.html'
    success_url = '/song_list'
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.added_by = self.request.user
        return super().form_valid(form)


class MusicianCreate(LoginRequiredMixin, CreateView):
    form_class = MusicianForm
    template_name = 'musician_create.html'
    success_url = '/'


class MusicianList(ListView):
    model = Musician
    template_name = 'musician_list.html'


class MusicianDetail(DetailView):
    model = Musician
    context_object_name = 'musician'
    template_name = 'musician_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = Song.objects.filter(musician__id=self.kwargs['pk'])
        return context


class UserSongList(LoginRequiredMixin, ListView):
    model = Song
    context_object_name = 'songs'
    template_name = 'user_songs.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(added_by=self.request.user)


class SongUpdateView(LoginRequiredMixin, UpdateView):
    model = Song
    form_class = SongForm
    context_object_name = 'songs'
    template_name = 'song_update.html'
    success_url = '/user_songs'
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(added_by=self.request.user)
