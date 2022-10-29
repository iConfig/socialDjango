from django.test import TestCase
from  django.contrib.auth.models import User 
from django.urls import reverse 
from .forms import CreatePost
# Create your tests here.

class registerTest(TestCase): # testing register action 

    def register(self):
        self.username = "mytestUser"
        self.email = "mytestemail@test.com"
        self.password = "myPa11Ss04TEst"

        response = self.client.post(reverse('register', data={
            'username': self.username,
            'email':self.email,
            'password1':self.password,
            'password2':self.password
        }))
        self.assertEqual(response.status_code,200)
        self.assertTrue["authenticated"]

class loginTest(TestCase): # testing login action
    
    def signIn(self):
        response = self.client.post(reverse('login'), data={
            'username':self.username,
            'password':self.password
        })
        self.assertEqual(response.status_code,200)
        self.assertTrue(response.data["authenticated"])

    def wrongInfo(self): #testing with wrong credentials
        response = self.client.post(reverse('login'), data={
            'username':self.username,
            'password':"shdjdjddks"
        })
        self.assertFalse(response.data["authentication failed"])


class postTest(TestCase): # testing post action
    
    def createPost(self): # testing post creation
        self.post = CreatePost(title="Test Post",
                    content="This is a test post",
                    created_by=self.username,
                    hide=False)
        self.post.save()
        self.assertEqual(response.status_code,200)
   
    def updatePost(self): #testing post update
        self.post = CreatePost(title="Test Post",
                    content="This is a test post",
                    created_by=self.username,
                    hide=False)
        self.post.content = "I changed it"
        self.post.save()
        self.assertEqual(self.post.content, "I changed it")

    
    
