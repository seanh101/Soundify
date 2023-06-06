import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Playlist, Song
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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

@login_required
def playlists_detail(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    return render(request, 'playlists/detail.html', {
        'playlist': playlist
    })

@login_required
def songs_index(request):
    songs = Song.objects.all()
    return render(request, 'songs/index.html', {
        'songs': songs
    })

@login_required
def songs_detail(request, song_id):
    song = Song.objects.get(id=song_id)
    return render(request, 'songs/detail.html', {
        'song': song
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

class PlaylistCreate(LoginRequiredMixin, CreateView):
    model = Playlist
    fields = ['name', 'description', 'is_public']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class PlaylistUpdate(LoginRequiredMixin, UpdateView):
    model = Playlist
    fields = ['name', 'description', 'is_public']

class PlaylistDelete(LoginRequiredMixin, DeleteView):
     model = Playlist
     success_url = '/playlists'

class SongCreate(LoginRequiredMixin, CreateView):
    model = Song
    fields = '__all__'
    success_url = '/songs'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SongUpdate(LoginRequiredMixin, UpdateView):
    model = Song
    fields = '__all__'

class SongDelete(LoginRequiredMixin, DeleteView):
    model = Song
    success_url = '/songs'

def assoc_song(reqeust, playlist_id, song_id):
    pass

def unassoc_song(request, playlist_id, song_id):
    pass

def spotify_connect(request):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = os.environ['CLIENT_ID'],
        client_secret = os.environ['SECRET_KEY'],
        redirect_uri='http://localhost:8000/spotify/auth',
        scope='user-read-playback-state user-modify-playback-state user-read-currently-playing app-remote-control streaming playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-read-playback-position user-top-read user-read-recently-played user-library-modify user-library-read'))
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    code = request.GET.get('code')
    sp_oauth = SpotifyOAuth(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['SECRET_KEY'], redirect_uri='http://localhost:8000/spotify/auth')
    token_info = sp_oauth.get_access_token(code)
    return redirect('playlists_index')

def song_search_page(request):
    return render(request, 'songs/search.html')
    
def song_search(request):
    query_string = request.GET.get('query')
    print('Query String: ', query_string)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['SECRET_KEY'], redirect_uri='http://localhost:8000/playlists'))
    results = sp.search(q=query_string, type='track', limit=10)

    print(results)

    return HttpResponse(f"Search results: {results}")