from django.shortcuts import render
from .models import Singer, Genre, MusicVideo, Album
from .decorators import allowed_users
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def singers(request):
    singer_list = Singer.objects.all()

    return render(request, 'music/singers.html', {'singer_list': singer_list})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def video_genres(request):
    genre_list = Genre.objects.all()

    return render(request, 'music/genres.html', {'genre_list': genre_list})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def music_video(request):
    video_list = MusicVideo.objects.all()

    return render(request, 'music/music_video.html', {'video_list': video_list})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def album(request):
    albums = Album.objects.all()

    return render(request, 'music/album.html', {'albums': albums})

