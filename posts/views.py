from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden
from .models import Post, Comment
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def index(request):

    posts = Post.objects.order_by('created_at')
    context = {
        'posts': posts,
        'uid': request.user.id,
    }
    print(context)

    return render(request, 'posts/index.html', context)

def view_post(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(on_post=post).order_by('created_at')
    context = {
        'post': post,
        'comments': comments,
        'uid': request.user.id,
        'method': 'show'
    }

    return render(request, 'posts/post.html', context)

@login_required
def create_post_form(request):

    return render(request, 'posts/create.html', {'method': 'create'})

@login_required
def create_post(request):

    if request.method == "GET":
        return HttpResponseNotFound()

    try:
        content = request.POST['content']
        user = request.user
        post = Post.objects.create(content=content, owner=user)
        return HttpResponseRedirect(reverse('post', args=(post.id, )))
    except Exception as e:
        print(e)
        return HttpResponseServerError()

@login_required
def create_comment(request, *args, **kwargs):

    if request.method == "GET":
        return HttpResponseNotFound()

    try:
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        content = request.POST['content']
        comment = Comment.objects.create(content=content, owner=request.user, on_post=post)
        return HttpResponseRedirect(reverse('post', args=(post.id, )))
    except Exception as e:
        print(e)
        return HttpResponseServerError()

@login_required
def edit_post(request, *args, **kwargs):

    if request.method == "GET":
        try:
            post_id = kwargs['post_id']
            post = get_object_or_404(Post, pk=post_id)
            if post.owner.id != request.user.id:
                return HttpResponseForbidden()
            context = {
            'method': 'edit',
            'post': post,
        }
            return render(request, 'posts/create.html', context)
        except Exception as e:
            print(e)
            return HttpResponseServerError()

    if request.method == "POST":
        try:
            post_id = kwargs['post_id']
            post = get_object_or_404(Post, pk=post_id)
            if post.owner.id != request.user.id:
                return HttpResponseForbidden()
            content = request.POST['content']
            post.content = content
            post.save()
            return HttpResponseRedirect(reverse('post', args=(post.id, )))
        except Exception as e:
            print(e)
            return HttpResponseServerError()

@login_required
def delete_post(request, *args, **kwargs):
    
    if request.method == "POST":
        try:
            post_id = kwargs['post_id']
            post = get_object_or_404(Post, pk=post_id)
            if post.owner.id != request.user.id:
                return HttpResponseForbidden()
            post.delete()
            return render(request, 'appbar.html', {'message':'post deleted.'})
        except Exception as e:
            print(e)
            return HttpResponseServerError()
    else:
        return HttpResponseNotFound()

@login_required
def edit_comment(request, *args, **kwargs):
    if request.method == "GET":
        try:
            comment_id = kwargs['comment_id']
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.owner.id != request.user.id:
                return HttpResponseForbidden()
            context = {'comment': comment}
            return render(request, 'posts/edit_comment.html', context)
        except Exception as e:
            print(e)
            return HttpResponseServerError()

    if request.method == "POST":
        try:
            comment_id = kwargs['comment_id']
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.owner.id != request.user.id:
                return HttpResponseForbidden()
            content = request.POST['content']
            comment.content = content
            comment.save()
            return HttpResponseRedirect(reverse('post', args=(comment.on_post.id, )))
        except Exception as e:
            print(e)
            return HttpResponseServerError()

@login_required
def delete_comment(request, *args, **kwargs):

    if request.method == "POST":
        try:
            comment_id = kwargs['comment_id']
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.owner.id != request.user.id:
                return HttpResponseForbidden()
            comment.delete()
            return render(request, 'appbar.html', {'message':'comment deleted.'})
        except Exception as e:
            raise e
            print(e)
            return HttpResponseServerError()
    else:
        return HttpResponseNotFound()