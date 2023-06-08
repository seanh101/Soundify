import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.http import HttpResponse, request, HttpResponseRedirect
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
    playlists = Playlist.objects.all()
    return render(request, 'songs/detail.html', {
        'song': song,
        'playlists': playlists
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

    def get_success_url(self):
        return reverse('songs_detail', kwargs={'song_id': self.object.pk})

class SongDelete(LoginRequiredMixin, DeleteView):
    model = Song
    success_url = '/songs'

def assoc_song(request):
    playlist_id = request.GET.get('playlist')
    song_id = request.GET.get('song_id')
    playlist = Playlist.objects.get(id=playlist_id)
    song = Song.objects.get(id=song_id)
    playlist.songs.add(song)
    return redirect('playlists_detail', playlist_id=playlist_id)


def unassoc_song(request, playlist_id, song_id):
    playlist = Playlist.objects.get(id=playlist_id)
    song = Song.objects.get(id=song_id)
    playlist.songs.remove(song)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
    search_type = request.GET.get('search_type')
    playlists = Playlist.objects.filter(user=request.user)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['SECRET_KEY'], redirect_uri='http://localhost:8000/playlists'))
    if search_type == 'artist':
        results = sp.search(q=query_string, type='artist', limit=50)
    elif search_type == 'album':
        results = sp.search(q=query_string, type='album', limit=50)
    else:
        results = sp.search(q=query_string, type='track', limit=50)

    return render(request, 'songs/search_results.html', {
        'results': results,
        'search_type': search_type,
        'playlists': playlists
    })


@login_required
def add_song(request, track_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['SECRET_KEY'], redirect_uri='http://localhost:8000/playlists'))
    track = sp.track(track_id)

    song = Song.objects.create(
        name=track['name'],
        artist=track['artists'][0]['name'],
        genre=track['album'].get('genres', ['Unknown'])[0],
        album=track['album']['name'],
        duration=track['duration_ms'],
        release_date=track['album']['release_date'],  # Set the release_date to the current date
    )

    return redirect('songs_index')

def add_song_and_assoc(request):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist')
        track_id = request.POST.get('track_id')

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['SECRET_KEY'], redirect_uri='http://localhost:8000/playlists'))
        track = sp.track(track_id)

        # Check if the song already exists in the database
        existing_song = Song.objects.filter(
            name=track['name'],
            artist=track['artists'][0]['name'],
            album=track['album']['name'],
            duration=track['duration_ms'],
            release_date=track['album']['release_date'],
        ).first()

        if existing_song:
            song = existing_song
        else:
            # Create a new song record
            song = Song.objects.create(
                name=track['name'],
                artist=track['artists'][0]['name'],
                genre=track['album'].get('genres', ['Unknown'])[0],
                album=track['album']['name'],
                duration=track['duration_ms'],
                release_date=track['album']['release_date'],
            )

        playlist = Playlist.objects.get(id=playlist_id)
        playlist.songs.add(song)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

