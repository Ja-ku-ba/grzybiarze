from django.contrib import admin
from .models import Fung, Post, Like, Dislike, Room, Message
# Register your models here.

admin.site.register(Fung)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Room)
admin.site.register(Message)