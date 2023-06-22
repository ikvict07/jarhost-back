from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404

# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_create.html', {'post': post})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_update.html', {'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_delete.html', {'post': post})