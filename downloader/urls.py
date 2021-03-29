from django.urls import path
from .import views


urlpatterns = [
        path('', views.home, name='homepage'),
        path('youtube_video_data/<str:url>', views.youtube_video_data, name='youtube_video_data'),
        path('download_video/<str:id>', views.download_video, name='download_video'),
        path('convert_mp3/<str:id>', views.convert_video_to_mp3, name='convert_mp3'),
        path('YVD', views.index, name='YVD'),


]
