from django.db import models
from django.contrib.auth.models import User


STATUS_CHOICES = (
    (0, 'new'),
    (1, 'doing'),
    (2, 'done'),
)


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(default='Write your description here!')
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return F"{self.name} {STATUS_CHOICES[self.status][1]}"
