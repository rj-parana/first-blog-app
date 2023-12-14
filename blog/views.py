from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.db.models import Count
from .models import Post, Category, Tag, Comment
from .forms import PostForm, SignUpForm, LogInForm, CommentForm, ReplyForm
import sys


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = SignUpForm()   
    return render(request, 'blog/signup.html', {'form': form})

def log_in(request):
    error = False
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)  
                return redirect('post_list')
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'blog/login.html', {'form': form, 'error': error})

def log_out(request):
    logout(request)
    return redirect(reverse('login'))

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(parent__isnull=True).all()
    new_comment = None
    if request.method == 'POST':
        parent_id = request.POST.get('parent_id', None)
        if parent_id:
            c_obj = Comment.objects.filter(id=parent_id).last()
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.parent = c_obj
                new_comment.save()
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
        # reply_form = ReplyForm(request.POST)
        # if reply_form.is_valid():
        #     post_id = request.POST.get('post_id')
        #     parent_id = request.POST.get('parent')
        #     reply = reply_form.save(commit=False)
        #     reply.post = Post(id=post_id)
        #     reply.parent = Comment(id=parent_id)
        #     reply.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def category(request, slug):
    cat = Category.objects.filter(slug=slug).last()
    posts = Post.objects.filter(category=cat).all()
    # num=Category.objects.all().annotate(posts_count=Count('post'))
    return render(request, 'blog/category_detail.html', {'cat': cat, 'posts': posts, 'num': posts.count()})

def tag(request, slug):
    rfr = Tag.objects.filter(slug=slug).last()
    posts = Post.objects.filter(tag=rfr).all()
    return render(request, 'blog/tag_detail.html', {'posts': posts, 'rfr': rfr, 'num': posts.count()})