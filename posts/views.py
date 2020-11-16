from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden, HttpResponseBadRequest
from .models import Post, Comment
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def check_arguments(request_arr, args):
    missing = []
    for arg in args:
        if arg not in request_arr:
            missing.append(arg)
    if missing:
        response = {
            'Missing argument': '%s' % ', '.join(missing),
        }
        return 1, HttpResponseBadRequest(response)
    return 0,

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
        res = check_arguments(request.POST, ['content'])
        if res[0]:
            return res[1]
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
        res = check_arguments(request.POST, ['content'])
        if res[0]:
            return res[1]
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
            if post.owner.id != request.user.id and not request.user.is_superuser:
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
            res = check_arguments(request.POST, ['content'])
            if res[0]:
                return res[1]
            post_id = kwargs['post_id']
            post = get_object_or_404(Post, pk=post_id)
            if post.owner.id != request.user.id and not request.user.is_superuser:
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
            if post.owner.id != request.user.id and not request.user.is_superuser:
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
            if comment.owner.id != request.user.id and not request.user.is_superuser:
                return HttpResponseForbidden()
            context = {'comment': comment}
            return render(request, 'posts/edit_comment.html', context)
        except Exception as e:
            print(e)
            return HttpResponseServerError()

    if request.method == "POST":
        try:
            res = check_arguments(request.POST, ['content'])
            if res[0]:
                return res[1]
            comment_id = kwargs['comment_id']
            comment = get_object_or_404(Comment, pk=comment_id)
            if comment.owner.id != request.user.id and not request.user.is_superuser:
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
            if comment.owner.id != request.user.id and not request.user.is_superuser:
                return HttpResponseForbidden()
            comment.delete()
            return render(request, 'appbar.html', {'message':'comment deleted.'})
        except Exception as e:
            raise e
            print(e)
            return HttpResponseServerError()
    else:
        return HttpResponseNotFound()