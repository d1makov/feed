from django.contrib import admin

# Register your models here.
from .models import Post, Follower

admin.site.register(Post)
admin.site.register(Follower)