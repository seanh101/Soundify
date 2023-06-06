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
   
    path('accounts/signup/', views.signup, name='signup'),
    
]