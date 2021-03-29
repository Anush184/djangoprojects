from django.shortcuts import render, redirect, HttpResponse
from pytube import YouTube
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . decorators import allowed_users, admin_only
import os
import requests
from isodate import parse_duration
from django.conf import settings
import ffmpeg
import youtube_dl


@login_required(login_url='login')
def youtube_video_data(request, url):
    a = url
    url = F"https://www.youtube.com/watch?v={url}"
    obj = YouTube(url)
    thumbnail_url = obj.thumbnail_url
    title = obj.title
    rating = obj.rating
    view = obj.views
    length = obj.length
    desc = obj.description
    age_restricted = obj.age_restricted
    resolutions = []
    stream_all = obj.streams.all()
    for stm in stream_all:
        resolutions.append(stm.resolution)
    resolutions = list(dict.fromkeys(resolutions))
    embed_link = url.replace("watch?v=", "embed/")
    # path = 'C:\\Downloads'
    context = {'rsl': resolutions, 'embd': embed_link, 'thumbnail_url': thumbnail_url, 'title': title, 'view': view,
                   'rating': rating, 'length': length, 'desc': desc, 'age_restricted': age_restricted, 'a': a}
    return render(request, 'downloader/yt_download.html', context)


def home(request):
    return render(request, 'downloader/base.html')


@login_required(login_url='login')
def download_video(request, id):
    url = F"https://www.youtube.com/watch?v={id}"
    homedir = os.path.expanduser("~")
    dirs = homedir + '/Downloads/youtube_videos'
    if request.method == 'POST':
        res = request.POST.get('rsl')
        YouTube(url).streams.get_by_resolution(res).download(dirs)
        # messages.success(request, "Download completed!")
        # return redirect('YVD')
        return render(request, "downloader/download_complete.html")

    else:
        # messages.error(request, "Sorry, something wrong!")
        # return render(request, "downloader/yt_download.html")
        return render(request, 'downloader/sorry.html')


@login_required(login_url='login')
def convert_video_to_mp3(request, id):
    video_url = F"https://www.youtube.com/watch?v={id}"
    # save_path = '/'.join(os.getcwd().split('/')[:3]) + '/Downloads/Youtube_mp3'
    path = os.path.join(os.path.expanduser("~"), 'Downloads/Youtube_mp3')

    params = {
        'format': 'bestaudio/best',
        'nocheckcertificate': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '360',
            }],
        'outtmpl': path + '/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(params) as dl:
        dl.download([video_url])

    return render(request, "downloader/download_complete.html")


@login_required(login_url='login')
def index(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 12,
            'type': 'video',

        }
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'first':
            return redirect(f"https://www.youtube.com/watch?v={video_ids[0]}")
        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet, contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 12,
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']

        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f"https://www.youtube.com/watch?v={result['id']}",
                'duration': parse_duration(result['contentDetails']['duration']),
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
            }
            if request.POST['submit'] == 'download':
                download_video(request, video_data['url'])
            videos.append(video_data)

    context = {
        'videos': videos,
    }

    return render(request, 'downloader/home.html', context)



