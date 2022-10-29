from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect 
from django.contrib import messages 
from django.urls import reverse 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User 
from .models import Post,Profile,Like,Comment
from .forms import CreatePost,signupForm,loginForm,UserUpdateForm,ProfileUpdateForm,CommentForm
# Create your views here.

# home view 
def HomeView(request): # home view to display all post title and author
    posts = Post.objects.filter(hide=False).order_by('-created_date')
    for i in posts:
        user = i.created_by
        pass
    profiles = Profile.objects.filter(username=user)
    return render(request, "posts/home.html", {"posts":posts,"profiles":profiles})

""" auth view begins """

def signupView(request): # ----> signup 
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = signupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = form.save()
            login(request, user)
            return redirect('home')
            messages.success(request, f"Account successfully created for {username}")
    else:
        form = signupForm()
    return render(request, "account/register.html", {"form":form})


def loginView(request): # -------- login
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"logged in as {username}")
                return redirect('home')
            else:
                messages.error(request, "invalid username or password")
                return redirect("login")

    else:
        form = loginForm()
    return render(request, 'account/login.html', {"form":form})


@login_required(login_url='login')
def logoutView(request):# -------- logout
    logout(request)
    messages.success(request, "you've logged out successfully")
    return redirect('home')

""" auth view ends """



""" post view  begins """

@login_required(login_url='login')
def PostDetails(request, pk): # post deteails view
    post = get_object_or_404(Post,pk=pk)
    profile = Profile.objects.filter(username=post.created_by)
    comments = Comment.objects.select_related('post').filter(post=pk)

    form = CommentForm()
    return render(request, "posts/postdetail.html", {"post":post,"profile":profile,
    "form":form,"comments":comments}) 

def CommentView(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            post_id = request.POST.get('post_id') 
            post_obj = Post.objects.get(id=post_id)
            comment_form = form.save(commit=False)
            comment_form.username= user
            comment_form.post = post_obj
            comment_form.save()
            if user not in post_obj.comments.all():
                post_obj.comments.add(user)
    return redirect(reverse('post_details' , args=[str(post_id)]))



@login_required(login_url='login')
def LikePostView(request): #post like view
    user = request.user 
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.likes == "LIKE":
                like.likes == "UNLIKE"
            else:
                like.likes == "LIKE"
        
        like.save()
    return HttpResponseRedirect(reverse('post_details', args=[str(post_id)]))

@login_required(login_url='login')
def PostCreate(request): # post create view
    if request.method == "POST":
        form = CreatePost(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user 
            instance.save()
            return redirect('home')

    else:
        form = CreatePost()
    return render(request, "posts/postcreate.html", {"form":form})


@login_required(login_url='login')
def PostUpdate(request, id): # post update view
    posts = get_object_or_404(Post, id=id)
    form = CreatePost(instance=posts)
    if request.method == "POST":
        form = CreatePost(request.POST, instance=posts)
        if form.is_valid():
            instance = form.save(commit=False)
# only owner of post can update, it was set in the template also, only owner of post can see the update or delete button
            if request.user == posts.created_by:  
                instance.save()
                return redirect('home')
    else: 
        form = CreatePost(instance=posts)
    return render(request, "posts/postedit.html", {"form":form})

@login_required(login_url='login')
def PostDelete(request, id): # post delete view
    post = get_object_or_404(Post, id=id)
# only owner of post can delete, it was set in the template also, only owner of post can see the update or delete button
    if request.user == post.created_by:
        post.delete()
        return redirect('home')



""" post view ends """
@login_required(login_url='login')
def ProfileView(request): # users profile view 
    post = Post.objects.filter(created_by=request.user).order_by('-created_date')
    profile = Profile.objects.filter(username=request.user)
    return render(request, "account/profile.html", {"post":post,"profile":profile})


@login_required(login_url='login') # --------- update profile 
def profileupdateView(request):
    if request.method == "POST":
        userform = UserUpdateForm(request.POST, instance=request.user)
        profileform = ProfileUpdateForm(request.POST, request.FILES, 
                        instance=request.user.profile_user)

        if userform.is_valid() and profileform.is_valid():
            username = userform.cleaned_data['username'] 
            email =   userform.cleaned_data['email']          
            userform.save()
            profile = profileform.save(commit=False)
            profile.email = email 
            profile.save()
            messages.success(request,"profile information updated successfully..")
            return redirect('profile')
    else:
        userform = UserUpdateForm(instance=request.user)
        profileform =ProfileUpdateForm(instance=request.user.profile_user)
    return render(request, 'account/editprofile.html', {
            "userform":userform,
            "profileform":profileform})