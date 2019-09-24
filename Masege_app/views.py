from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from Masege_app.models import Student

from Masege_app import models


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            response = HttpResponseRedirect(r'/')
            response.set_cookie('login', username, 60 * 60 * 24 * 1)
            return response
    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Student.objects.create_user(username=username, password=password, email=email)
        if user:
            login(request, user)
            response = HttpResponseRedirect('/')
            response.set_cookie('name', username, 60 * 60 * 24 * 1)
            return response
    return render(request, 'signup.html')


@login_required(login_url='/signin/')
def signout(request):
    auth.logout(request)
    return HttpResponseRedirect("/signin/")


@login_required(login_url='/signin/')
def index(request):
    posts_list = models.Post.objects.all()
    return render_to_response('index.html', {'posts_list': posts_list})


@login_required(login_url='/signin/')
def post_detail(request, post_id):
    post = models.Post.objects.get(pid=post_id)
    auth_name = models.Student.objects.get(username=post.pauth).sname
    return render_to_response('post_detail.html', {'post_obj': post, 'post_auth': auth_name})


@login_required(login_url='/signin/')
def about(request):
    return render_to_response('about.html')
