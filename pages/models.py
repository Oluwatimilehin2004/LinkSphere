from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    post_img = models.ImageField(upload_to='post_imgs', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes= models.ManyToManyField(User, related_name='post_likes', blank=True)

    class Meta:
        ordering= ['-created_at']

    def _str_(self):
        return self.author.username

class Comment(models.Model):
    post= models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    content= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta: 
        ordering= ['-created_at']

    def __str__(self):
        return self.author.username 
    
