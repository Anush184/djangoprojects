from django.db import models


class Singer(models.Model):
    singer_name = models.CharField(max_length=50)
    singer_birthdate = models.CharField(max_length=50)
    description = models.TextField()
    number_songs = models.IntegerField()
    total_awards = models.IntegerField(default=0)

    def __str__(self):
        return self.singer_name


GENRE_CHOICES = (
        (0, "Performance"),
        (1, "Narrative"),
        (2, "Concept"),
        (3, "Lyric"),
        (4, "Animated"),
    )


class Genre(models.Model):
    type = models.IntegerField(choices=GENRE_CHOICES)
    description = models.TextField()

    def __str__(self):

        return f"{GENRE_CHOICES[self.type][1]}"


class MusicVideo(models.Model):
    artist = models.CharField(max_length=50)
    video_title = models.CharField(max_length=50)
    director = models.CharField(max_length=30)
    duration = models.FloatField()
    issue_year = models.IntegerField()
    video_genre = models.CharField(max_length=30)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)

    def __str__(self):
        return self.artist + ' - ' + self.video_title


class Album(models.Model):
    artist = models.CharField(max_length=50)
    album_title = models.CharField(max_length=100)
    album_genre = models.CharField(max_length=50)
    album_logo = models.CharField(max_length=150)
    music_video = models.OneToOneField(MusicVideo, on_delete=models.CASCADE, primary_key=True)
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE)

    def __str__(self):
        return self.artist + ' - ' + self.album_title



