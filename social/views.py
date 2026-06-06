import base64
from urllib import request
from django.core.files.base import ContentFile
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Profile, Post, Comment, Like, Follow
from .forms import RegisterForm, ProfileForm, PostForm, CommentForm, EditPostForm

def home(request):

    if request.user.is_authenticated:
        return redirect('feed')

    return redirect('login')

def feed(request):

    if request.user.is_authenticated:
        posts = Post.objects.exclude(
            author=request.user
        ).order_by('-created_at')

        liked_post_ids = Like.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True)

    else:
        posts = Post.objects.all().order_by('-created_at')
        liked_post_ids = []

    return render(request, 'social/feed.html', {
        'posts': posts,
        'liked_post_ids': liked_post_ids
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('feed')
    else:
        form = RegisterForm()

    return render(request, 'social/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
    else:
        form = AuthenticationForm()

    return render(request, 'social/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)

    posts = Post.objects.filter(author=profile_user).order_by('-created_at')

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

    liked_post_ids = []

    if request.user.is_authenticated:
        liked_post_ids = Like.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True)

    return render(request, 'social/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'liked_post_ids': liked_post_ids
    })


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')

    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)

            cropped_image = request.POST.get('cropped_image')

            if cropped_image:
                format, imgstr = cropped_image.split(';base64,')
                ext = format.split('/')[-1]

                profile.profile_photo.save(
                    f'{request.user.username}_profile.{ext}',
                    ContentFile(base64.b64decode(imgstr)),
                    save=False
                )

            profile.save()

            return redirect('profile', username=request.user.username)

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'social/edit_profile.html', {'form': form})


def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()

    return render(request, 'social/create_post.html', {'form': form})


def like_post(request, post_id):

    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'Login required'
        }, status=403)

    post = get_object_or_404(Post, id=post_id)

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })


def add_comment(request, post_id):

    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

    return redirect(request.META.get('HTTP_REFERER', 'feed'))


def delete_comment(request, comment_id):

    if not request.user.is_authenticated:
        return redirect('login')

    comment = get_object_or_404(
        Comment,
        id=comment_id,
        user=request.user
    )

    comment.delete()

    return redirect(request.META.get('HTTP_REFERER', 'feed'))


def follow_user(request, username):

    if not request.user.is_authenticated:
        return redirect('login')

    user_to_follow = get_object_or_404(
        User,
        username=username
    )

    if request.user != user_to_follow:

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            follow.delete()

    return redirect(request.META.get('HTTP_REFERER', 'feed'))


def delete_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    post.delete()

    return redirect('feed')


def edit_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect('feed')
    else:
        form = EditPostForm(instance=post)

    return render(request, 'social/edit_post.html', {
        'form': form,
        'post': post
    })


def search_users(request):
    query = request.GET.get('q')
    users = []

    if query:
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )

        if request.user.is_authenticated:
            users = users.exclude(id=request.user.id)

    return render(request, 'social/search_users.html', {
        'query': query,
        'users': users
    })

def followers_list(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    followers = Follow.objects.filter(
        following=profile_user
    )

    return render(
        request,
        'social/followers_list.html',
        {
            'profile_user': profile_user,
            'followers': followers
        }
    )


def following_list(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    following = Follow.objects.filter(
        follower=profile_user
    )

    return render(
        request,
        'social/following_list.html',
        {
            'profile_user': profile_user,
            'following': following
        }
    )