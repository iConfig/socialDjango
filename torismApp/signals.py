from django.db.models.signals import post_save 
from django.contrib.auth.models import User 
from django.dispatch import receiver 
from .models import Profile

@receiver(post_save, sender=User) #signal to create user profile on sign up
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance,email=instance.email)

@receiver(post_save, sender=User)#signal to save user profile after creation
def save_profile(sender, instance, **kwargs):
    instance.profile_user.save()

    