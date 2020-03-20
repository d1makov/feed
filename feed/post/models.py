from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=now)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'title:{self.title}, author: {self.author}, time: {self.creation_date}'

    def get_absolute_url(self):
        return reverse_lazy('post_detail', args=[self.pk])


class Follower(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def follow(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def unfollow(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)