from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import PostForm
from .models import Group
from .models import Post
from .models import User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, settings.POSTS_NUMBERS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).all()
    paginator = Paginator(post_list, settings.POSTS_NUMBERS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = User.objects.get(username=username)
    post_list = Post.objects.filter(author=author)
    paginator = Paginator(post_list, settings.POSTS_NUMBERS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'author': author,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {
        'post': post,
        'is_edit': True
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('posts:profile', username=request.user.username)
        return render(request, 'posts/create.html', {'form': form, 'is_edit': False})
    form = PostForm()
    return render(request, 'posts/create.html', {'form': form, 'is_edit': False})


def post_edit(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('posts:profile', username=request.user.username)
        return render(request, 'posts/update_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/update_post.html', {'form': form})