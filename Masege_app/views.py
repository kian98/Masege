from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from Masege_app import models

# Create your views here.
def index(request):
    posts_list = models.Post.objects.all()
    return render_to_response('index.html', {'posts_list': posts_list})

def post_detail(request, post_id):
    post = models.Post.objects.get(pid=post_id)
    auth_name = models.Student.objects.get(username=post.pauth).sname
    return render_to_response('post_detail.html', {'post_obj': post, 'post_auth': auth_name})