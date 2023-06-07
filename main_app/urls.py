from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('playlists/', views.playlists_index, name='playlists_index'),
    path('playlists/<int:playlist_id>/', views.playlists_detail, name='playlists_detail'),
    path('playlists/create/', views.PlaylistCreate.as_view(), name='playlist_create'),
    path('playlists/<int:pk>/update', views.PlaylistUpdate.as_view(), name='playlists_update'),
    path('playlists/<int:pk>/delete', views.PlaylistDelete.as_view(), name='playlists_delete'),
    path('songs/', views.songs_index, name='songs_index'),
    path('songs/<int:song_id>/', views.songs_detail, name='songs_detail'),
    path('songs/create/', views.SongCreate.as_view(), name='song_create'),
    path('songs/<int:pk>/update', views.SongUpdate.as_view(), name='song_update'),
    path('songs/<int:pk>/delete', views.SongDelete.as_view(), name='song_delete'),
    path('songs/search', views.song_search_page, name='song_search_page'),
    path('songs/search/results', views.song_search, name='song_search'),
    path('spotify/', views.spotify_connect, name='spotify_connect'),
    path('spotify/auth', views.spotify_callback, name='spotify_callback'),
    path('songs/add/<str:track_id>/', views.add_song, name='add_song'),
   
    path('songs/assoc_song/', views.assoc_song, name='assoc_song'),
    
    path('accounts/signup/', views.signup, name='signup'),
    
]