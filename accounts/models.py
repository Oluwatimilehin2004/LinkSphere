from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.db.models.signals import post_save # type: ignore
from django.dispatch import receiver # type: ignore

GENDER_CHOICES= (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

# Create your models here.
class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank= True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, default='profile_pics/default.png')
    country= models.CharField(max_length=100, blank=True)
    banner= models.ImageField(upload_to='banner', blank=True, default='banner/backdrop-blur.png')
    gender= models.CharField(max_length=100, choices=GENDER_CHOICES, default='Male')


    def __str__(self):
        return self.user.username
    
    # def get_profile_picture(self):
    #     if self.profile_pic:
    #         return self.profile_pic.url
    #     return '/static/images/default_profile_pic.jpg'

        
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user= instance)


@receiver(post_save, sender=User)
def save_user(sender, instance, **kwargs):
    instance.profile.save()

class Follow(models.Model):
    follower= models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed=models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at= models.DateField(auto_now_add=True)

 

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'