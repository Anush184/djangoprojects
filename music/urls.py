from django.urls import path
from .import views


urlpatterns = [
        path('singers', views.singers, name='singers'),
        path('videos', views.music_video, name='music_video'),
        path('genres', views.video_genres, name='video_genres'),
        path('albums', views.album, name='albums'),
]
