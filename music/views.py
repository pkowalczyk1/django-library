from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from music.models import Song, Musician
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from music.forms import SongForm, MusicianForm, SignUpForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django import http
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required

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

    def form_invalid(self, form):
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' border border-danger'
        
        if 'password2' in form.errors:
            form['password1'].field.widget.attrs['class'] += ' border border-danger'
        return super().form_invalid(form)


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
    success_url = '/user_songs'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(added_by=self.request.user)


@login_required
def song_like(request):
    song = get_object_or_404(Song, id=request.POST.get('song_id'))
    page = request.POST.get('path', '/')
    if song.likes.filter(id=request.user.id).exists():
        song.likes.remove(request.user)
    else:
        song.likes.add(request.user)
    
    return HttpResponseRedirect(page)


def search(request):
    query = request.GET.get('q')
    if query:
        songs = Song.objects.filter(title__icontains=query)
        musicians = Musician.objects.filter(name__icontains=query)
    else:
        songs = []
        musicians = []
    
    return render(request, template_name='search_results.html', context={'songs': songs, 'musicians': musicians})


class SongDetailView(DetailView):
    model = Song
    context_object_name = 'song'
    template_name = 'song_detail.html'
