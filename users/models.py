from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


EXPERIENCE_CHOICES = (
    ("Less than 1 year", "Less than 1 year"),
    ("1 to 3 year", "1 to 3 year"),
    ("More than 3 year", "More than 3 year"),
)


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    career = models.CharField(max_length=200, blank=True, null=True)
    experience = models.CharField("Experience", max_length=80, choices=EXPERIENCE_CHOICES, default="More than 3 year")
    phone_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return F"{self.user.username} {self.phone_number}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
