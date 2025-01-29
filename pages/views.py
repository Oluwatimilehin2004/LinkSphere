from django.http import HttpResponseRedirect # type: ignore
from django.shortcuts import render, redirect # type: ignore
from accounts.models import Follow, Profile
from pages.forms import CreatePostForm, updatePost
from django.contrib import messages # type: ignore
from pages.models import Posts, Comment
from django.contrib.auth.decorators import login_required # type: ignore
from django.shortcuts import render, get_object_or_404


# Create your views here.
@login_required(login_url='signin')
def feeds(request):
    posts = Posts.objects.all().order_by('-created_at')
    followers = Follow.objects.filter(followed=request.user)
    return render(request, 'feeds.html', {'posts': posts, 'followers': followers})

@login_required(login_url='sigin')
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author =request.user
            post.save()
            messages.success(request, 'Post created successfully')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'Error creating post')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        form = CreatePostForm()
    return render(request, 'create-post.html')

@login_required(login_url='signin')
def like_post(request, id):
    post = Posts.objects.get(id=id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        post.likes.add(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render('feeds')

@login_required(login_url='signin')
def add_comment(request, id):
    post= Posts.objects.get(id=id)
    if request.method== 'POST':
        post_comment= request.POST['comment']
        form= Comment.objects.create(post= post, author= request.user, content= post_comment)
        form.save()
        messages.success(request, 'Form Added Successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'feeds.html', {'post': post})

@login_required(login_url= 'signin')
def edit_post(request, id):
    post= Posts.objects.get(id=id)
    form = updatePost(instance=post)

    if request.method == "POST":
        form= updatePost(request.POST, request.FILES, instance= post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('feeds')
        else: 
            messages.error(request, 'Error editing post')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required(login_url= 'signin')
def delete_post(request, id):
    post=  Posts.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='signin')
def post_detail(request, id):
    post = get_object_or_404(Posts, id=id)  # Fetch a single post
    followers = Follow.objects.filter(followed=request.user)
    return render(request, 'post-detail.html', {'post': post, 'followers': followers})


def followers_page(request):
    # Get the followers of the current user
    followers = Follow.objects.filter(followed=request.user)
    context = {
        'followers': followers,
    }
    return render(request, 'followers.html', context)
