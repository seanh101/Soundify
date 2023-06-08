from django.contrib import admin
from .models import Playlist, Song, UserProfile

admin.site.register(Playlist)
admin.site.register(Song)
admin.site.register(UserProfile)


