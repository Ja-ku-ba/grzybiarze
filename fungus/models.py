from contextlib import nullcontext
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Fung(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    poisoning = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    like_post = models.ManyToManyField(User, related_name='like', default=None ,blank=True)
    dislike_post = models.ManyToManyField(User, related_name='dislike', default=None ,blank=True)

    def __str__(self):
        return self.body[:50]

    @property
    def num_likes(self):
        return self.like.all().count()
    
    @property
    def num_dislike(self):
        return self.dislike.all().count()

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Like', 'Like')
)

class Like(models.Model):
    user_like = models.ForeignKey(User, related_name='user_like', on_delete=models.CASCADE)
    post_likes = models.ForeignKey(Post, related_name='post_like', on_delete=models.CASCADE)
    value_like = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post_likes)

DISLIKE_CHOICES = (
    ('Dislike', 'Dislike'),
    ('Dislike', 'Dislike')
)

class Dislike(models.Model):
    user_dislike = models.ForeignKey(User, related_name='user_dislike', on_delete=models.CASCADE)
    post_dislikes = models.ForeignKey(Post, related_name='post_dislike', on_delete=models.CASCADE)
    value_dislike = models.CharField(choices=DISLIKE_CHOICES, default='Dislike', max_length=10)

    def __str__(self):
        return str(self.post_dislikes)