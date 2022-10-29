from django.db import models
from django.contrib.auth.models import User 
from PIL import Image 
from datetime import date


today = date.today()
# Create your models here.


class Post(models.Model): # post model
    title = models.CharField(max_length=150,verbose_name="Title", null=False)
    content = models.TextField(verbose_name="Content", null=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User,related_name="user_liked")
    comments = models.ManyToManyField(User, related_name="user_comments")
    hide = models.BooleanField(verbose_name="Hide", default=False)

    def __str__(self):
        return self.title 
        

LIKE_OPTION = (
    ('LIKE', 'like'),
    ('UNLIKE', 'unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, related_name="like_user", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="post_likes", on_delete=models.CASCADE)
    likes = models.CharField(choices=LIKE_OPTION, default='LIKE', max_length=10)



class Profile(models.Model): #profile model 
    picture = models.ImageField( default="pic.jpg",upload_to =f"DPs/{today}",
                                blank=True, null=True)
    first_name = models.CharField(max_length=40, verbose_name="FirstName",
                                blank=True, null=True)
    last_name = models.CharField(max_length=40, verbose_name="LastName",
                                blank=True, null=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile_user")

    email = models.EmailField(max_length=100, verbose_name="Email", null=True)

    location = models.CharField(max_length=200, verbose_name="Location",
                                blank=True, null=True)
    bio = models.CharField(max_length=2000, verbose_name="Bio",
                            blank=True, null=True)


    def __str__(self):
        return f"{self.username} Profile"

    def save(self, *args, **kwargs): # setting default image size before saving
        super().save()
        img = Image.open(self.picture.path)
        if img.height > 1000 or img.width > 1000:
            new_img = (1000,1000)
            img.thumbnail(new_img)
            img.save(self.picture.path)

class Comment(models.Model): 
    post = models.ForeignKey(Post, related_name="post_comment", on_delete=models.CASCADE)
    username = models.ForeignKey(User, related_name="comment_user", on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000, null=False)