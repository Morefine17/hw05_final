from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


@cache_page(20)
def index(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, settings.TOTAL_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    paginator = Paginator(posts, settings.TOTAL_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'group': group,

    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_profile = author.posts.all().order_by('-pub_date')
    paginator = Paginator(posts_profile, settings.TOTAL_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        following = Follow.objects.get(user=request.user, author=author)
    except Exception:
        following = False
    context = {
        'author': author,
        'page_obj': page_obj,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    selected_post = get_object_or_404(Post, id=post_id)
    author = selected_post.author

    form = CommentForm()
    context = {
        'selected_post': selected_post,
        'author': author,
        'form': form,
        'post_id': post_id
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=request.user.username)
        return render(request, 'posts/post_create.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    if request.user == post.author:
        form = PostForm(request.POST or None,
                        files=request.FILES or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post_id)
        return render(request, 'posts/post_create.html',
                      {'form': form, 'is_edit': is_edit, 'post_id': post_id})
    return redirect('posts:post_detail', post_id=post_id, )


@login_required
def add_comment(request, post_id):
    selected_post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = selected_post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    follow_post = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(follow_post, settings.TOTAL_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    follow_author = get_object_or_404(User, username=username)
    unfollow = Follow.objects.get(user=request.user, author=follow_author)
    if unfollow is not None:
        unfollow.delete()
    return redirect('posts:profile', username=username)
