from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Song(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_date = models.DateField('Release Date')
    album = models.CharField(max_length=100)
    duration = models.IntegerField('Duration (ms)')

    def __str__(self):
        return f"{self.name} by {self.artist}" 
    
    def get_absolute_url(self):
        return reverse('songs_detail', kwargs={'pk': self.id})

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_public = models.BooleanField(default=False)
    songs = models.ManyToManyField(Song, blank=True) 
    duration = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('playlists_detail', kwargs={'playlist_id': self.id})