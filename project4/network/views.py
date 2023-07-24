from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator





def index(request):
    all_post = Post.objects.all().order_by("-date")
    paginator = Paginator(all_post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "page_obj":page_obj,
    })


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

@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST['post-content']
        new_post = Post(
            user = request.user,
            post_content = content
        )
        new_post.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "network/new_post.html")


@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edited_post = Post.objects.get(pk=post_id)
        edited_post.post_content = data["edited_post"]
        edited_post.save()
        return JsonResponse({
            "message":"edited successfully",
            "data":data["edited_post"]
        })
    else:
        post = Post.objects.get(pk=post_id)
        return render(request, "network/edit_post.html",{
            "post":post,
        }
        )


def profile(request, username):
    if request.user.is_authenticated:
        is_following = False
        user = User.objects.get(username=username)
        for i in request.user.people_followed.all().iterator():
            if i == user:
                is_following = True
                break

        users_posts = Post.objects.filter(user=user).order_by("-date")
        paginator = Paginator(users_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        
        return render(request, "network/profile.html", {
            "page_obj":page_obj,
            "user":user,
            "is_following": is_following,
        })
    else:
        user = User.objects.get(username=username)
        users_posts = Post.objects.filter(user=user).order_by("-date")
        return render(request, "network/profile.html", {
            "posts":users_posts,
            "user":user,
        })


@login_required
def follow(request, username):

    user = User.objects.get(username=username)
    request.user.people_followed.add(user)
    return profile(request, username)

@login_required
def unfollow(request, username):
    user = User.objects.get(username=username)
    request.user.people_followed.remove(user)
    return profile(request, username)

@login_required
def delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return HttpResponseRedirect(reverse('index'))


@login_required
def following(request):
    posts = []
    for i in Post.objects.all().iterator():
        if i.user in request.user.people_followed.iterator():
            posts.append(i)
    
    return render(request, "network/following.html", {
        "posts": posts,
    })


@login_required
@csrf_exempt
def like(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username=data["username"])
        post = Post.objects.get(pk=post_id)
        post.liked_by.add(user)
        return JsonResponse({
            "message":"Like post",
        })

@login_required
@csrf_exempt
def unlike(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        user = User.objects.get(username=data["username"])
        post = Post.objects.get(pk=post_id)
        post.liked_by.remove(user)
        return JsonResponse({
            "message":"Unlike post",
        })