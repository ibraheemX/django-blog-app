from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from . forms import PostForm


def home(request):
    posts = Post.objects.all()

    return render(request, 'blog/home.html', {'posts': posts})


def details(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    return render(request, 'blog/details.html', {'post': post})


def create_post(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':

        form = PostForm(request.POST)

        if form.is_valid():

            post = form.save(commit=False)

            post.author = request.user

            post.save()

            return redirect('home')

    else:
        form = PostForm()

    return render(request, 'blog/create_post.html', {
        'form': form
    })


def update_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':

        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return redirect('details', post.id)

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/update_post.html', {
        'form': form
    })


def delete_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'blog/delete_post.html', {
        'post': post
    })
