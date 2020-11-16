from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

def logout_view(request):
    logout(request)

    return redirect('/')

def homepage(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return redirect('/posts')

def login(request):
    if request.method == "GET":
        return  render(request, 'login.html', {'next': request.GET.get('next')})

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(request.GET.get('next', '/posts'))
        else:
            return render(request, 'login.html', {'error_message':'username or password not correct.'})