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
    duration = models.IntegerField()

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('song_detail', kwargs={'pk': self.id})

class Playlist(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_public = models.BooleanField(default=False)
    songs = models.ManyToManyField(Song) 
    duration = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('playlist_detail', kwargs={'playlist_id': self.id})