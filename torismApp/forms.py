from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 
from . models import Post,Profile,Comment


class signupForm(UserCreationForm): # sign up form with usercreationform
    email = forms.EmailField(max_length=100, min_length=6, label="Email",
                             required=True, help_text="enter a valid email")
    class Meta:
        model = User 
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self): # clean and run validation on username
        username = self.cleaned_data['username'].lower()
        new_username = User.objects.filter(username=username)
        if new_username.count():
            raise ValidationError("username already exist")
        elif len(username) < 4 or len(username) > 25:
            raise ValidationError("username can not be lesser than 4 or greater than 25 characters")
        else:
            pass 
        return username

    def clean_email(self): # clean and run validation on email
        email = self.cleaned_data["email"].lower()
        new_email = User.objects.filter(email=email)
        if new_email.count():
            raise ValidationError("email already exist")
        elif len(email) < 6 or len(email) > 100:
            raise ValidationError("invalid length of email")
        else:
            pass 
        return email 

    def clean_password(self): # clean and run validation on password
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("passwords do not match")
        return password2
    
    
    def save(self, commit=True): # commit(save) cleaned data
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user 


class loginForm(forms.Form): # login form
    username = forms.CharField(max_length=25, min_length=4, label="Username",
                            required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class CreatePost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content','hide']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']


class UserUpdateForm(forms.ModelForm):# update user form 
    email = forms.EmailField(max_length=100, min_length=6, label="Email",
                             required=True, help_text="enter a valid email")
    class Meta:
        model = User 
        fields = ['username','email']

    def clean_username(self): # clean and validate username
        username = self.cleaned_data['username'].lower()
        current_user = self.instance.username
        new_username = User.objects.filter(username=username)
        if new_username.count() and current_user != username:
            raise ValidationError("username already exist")
        elif len(username) < 4 or len(username) > 25:
            raise forms.ValidationError("username can not be lesser than 4 or greater than 25 characters")
        else:
            pass 
        return username

    def clean_email(self): # clean and validate email
        email = self.cleaned_data['email'].lower()
        current_email = self.instance.email
        new_Email = User.objects.filter(email=email)
        if new_Email.count() and current_email.lower() != email:
            raise forms.ValidationError("email already exist")
        elif len(email) < 8 or len(email) > 100:
            raise ValidationError("invalid length of email")
        return email

    # def save(self, commit=True): # commit(save) cleaned data
    #     user = User.objects.create_user(
    #         self.cleaned_data['username'],
    #         self.cleaned_data['email']
    #     )
    #     return user 

class ProfileUpdateForm(forms.ModelForm):# update profile form 
    class Meta:
        model = Profile
        fields = ('picture','first_name','last_name','location','bio')