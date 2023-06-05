import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Playlist, Song

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def playlists_index(request):
    playlists = Playlist.objects.filter(user=request.user)
    return render(request, 'playlists/index.html', {
        'playlists': playlists
    })

def playlists_detail(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    return render(request, 'playlists/detail.html', {
        'playlist': playlist
    })


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('playlists_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class PlaylistCreate(CreateView):
    model = Playlist
    fields = ['name', 'description', 'is_public', 'songs']

    def form_valid(self, form):
        form.instance.user = self.reqeust.user
        return super().form_valid(form)
    
class PlaylistUpdate(UpdateView):
    model = Playlist
    fields = ['name', 'description', 'is_public']

class PlaylistDelete(DeleteView):
     model = Playlist
     success_url = '/playlists'

def create_song(request, playlist_id):
    pass

def assoc_song(reqeust, playlist_id, song_id):
    pass

def unassoc_song(request, playlist_id, song_id):
    pass
