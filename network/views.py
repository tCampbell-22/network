import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms.models import ModelForm
from django.http import JsonResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import *

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['body']

def index(request):
    pre_posts =  Post.objects.all().order_by("-timestamp")
    
    paginator = Paginator(pre_posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.get_page(request.GET.get("page"))
        except:
            posts = paginator.get_page(1)
    else:
        posts = paginator.get_page(1)

    return render(request, "network/index.html", {
        "form" : PostForm(),
        "posts" : posts,
    })

def following(request):
    pre_posts = Post.objects.filter(author__in=request.user.following.all()).order_by("-timestamp")
    paginator = Paginator(pre_posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.get_page(request.GET.get("page"))
        except:
            posts = paginator.get_page(1)
    else:
        posts = paginator.get_page(1)

    return render(request, "network/index.html", {
        "posts" : posts,
    })

def profile_view(request, name):
    curUser = User.objects.get(username=name)
    user = request.user
    return render(request, "network/profile.html", {
        "curUser" : curUser,
        "posts" : Post.objects.filter(author=curUser).order_by("-timestamp"),
    })
@csrf_exempt
def edit(request):
    if request.method == "POST":
        id = request.POST.get('id')
        newText = request.POST.get('newText')
        post = Post.objects.get(id=id)
        post.body = newText
        post.save()
        data = {
            "post" : newText
        }
        return JsonResponse(data, status=200)
    return JsonResponse({}, status=400)


@csrf_exempt
def follow(request):
    if request.method == "POST":
        profileName = request.POST.get('profileName') 
        profileUser = User.objects.get(username=profileName)
        if  profileUser in request.user.following.all():
            request.user.following.remove(profileUser)
        else:
            request.user.following.add(profileUser)
        request.user.save()
        data = {
            "numFollowers" : profileUser.follow_count()
        }
        return JsonResponse(data, status=200)
    return JsonResponse({}, status=400)

@csrf_exempt
def like(request): 
    if request.method == "POST":
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post.save()
        data = {
            "likes" : post.likes_count()
        }
        return JsonResponse(data, status=200)
    return JsonResponse({}, status=400)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create(request):
    if request.method == "POST":
        form_post = PostForm(request.POST)
        user=request.user
        if form_post.is_valid():
            new_post = form_post.save(commit=False)
            new_post.author = user
            new_post.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "index.html", {
        "form" : PostForm(),
        "posts" : Post.objects.all(),
        "request" : user
    })
