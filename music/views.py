from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from music.models import Song, Musician
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from music.forms import SongForm, MusicianForm, SignUpForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django import http
from django.urls import reverse_lazy, reverse

# Create your views here.

def main_page(request):
    return render(request, template_name='index.html')


class SongList(ListView):
    model = Song
    template_name = 'songs_list.html'
    context_object_name = 'songs'


def profile_view(request):
    return render(request, template_name='registration/profile.html')


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


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


class SongDeleteView(LoginRequiredMixin, DeleteView):
    model = Song
    template_name = 'song_confirm_delete.html'
    success_url = '/user_songs'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(added_by=self.request.user)


def song_like(request, pk):
    song = get_object_or_404(Song, id=request.POST.get('song_id'))
    if song.likes.filter(id=request.user.id).exists():
        song.likes.remove(request.user)
    else:
        song.likes.add(request.user)
    
    return HttpResponseRedirect(reverse('list'))
