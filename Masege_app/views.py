from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, redirect
from django.views import View
from django.views.generic import ListView
from django_comments.models import Comment
from django.db.models import Max
from notifications.signals import notify

from Masege_app import models
from Masege_app.models import Student, Post


def signin(request):
    has_error = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            response = HttpResponseRedirect(r'/')
            response.set_cookie('login', username, 60 * 60 * 1 * 1)
            return response
        else:
            has_error = True
    return render(request, 'signin.html', {'has_error': has_error})


def signup(request):
    has_error = False
    error_msg = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Student.objects.all().filter(username=username).count() != 0:
            error_msg = "用户名已存在"
        elif Student.objects.all().filter(email=email).count() != 0:
            error_msg = "邮箱已存在"
        else:
            user = Student.objects.create_user(username=username, password=password, email=email)
            if user:
                login(request, user)
                response = HttpResponseRedirect('/')
                response.set_cookie('name', username, 60 * 60 * 1 * 1)
                return response
        has_error = True
    return render(request, 'signup.html', {'has_error': has_error, 'error_msg': error_msg})


@login_required(login_url='/signin/')
def signout(request):
    auth.logout(request)
    return HttpResponseRedirect("/signin/")


post_per_page = 10


@login_required(login_url='/signin/')
def index(request):
    # 也可以使用hidden属性来确定页面
    searchFlag = False
    posts_list = models.Post.objects.all().order_by("-createTime")
    page = request.GET.get('page')
    if page == None or int(page) == 0:
        has_older = ''

        if posts_list.count() < post_per_page:
            has_older = 'disabled'
        end = post_per_page if posts_list.count() > post_per_page else posts_list.count()
        sliced_posts_list = posts_list[:end]
        has_newer = 'disabled'
        return render(request, 'index.html',
                      {'posts_list': sliced_posts_list, 'next_page': 1, 'pre_page': -1, 'has_newer': has_newer,
                       'searchFlag': searchFlag, 'has_older': has_older})
    page = int(page)
    if page < 0 or page * post_per_page > posts_list.count():
        pass
    begin = post_per_page * page
    if posts_list.count() > post_per_page * (page + 1):
        end = post_per_page * (page + 1)
        has_older = ''
    else:
        end = posts_list.count()
        has_older = 'disabled'
    sliced_posts_list = posts_list[begin:end]
    return render(request, 'index.html',
                  {'posts_list': sliced_posts_list, 'pre_page': page - 1, 'next_page': page + 1,
                   'has_older': has_older, 'searchFlag': searchFlag})


@login_required(login_url='/signin/')
def post_detail(request, post_id):
    post = models.Post.objects.get(pid=post_id)
    auth_name = models.Student.objects.get(username=post.pauth).sname

    post.view_cnt += 1
    post.save()

    return render(request, 'post_detail.html', {'post_obj': post, 'post_auth': auth_name})


@login_required(login_url='/signin/')
def about(request):
    return render_to_response('about.html')


@login_required(login_url='/signin/')
def sub_comment(request):
    post_id = request.POST.get('post_id')
    comment_content = request.POST.get('comment_content')

    if str(comment_content).strip() != "":
        post_table_obj = ContentType.objects.get(id=15)
        comment_obj = Comment.objects.create(
            content_type=post_table_obj,
            site_id=1,
            object_pk=post_id,
            user=request.user,
            comment=comment_content,
        )
        post = models.Post.objects.get(pid=post_id)
        post.comment_cnt += 1
        post.save()
        notify.send(
            request.user,
            recipient=post.pauth,
            verb="评论了你",
            target=post,
            action_object=comment_obj,
        )

    return HttpResponseRedirect('/detail/' + post_id)


@login_required(login_url='/signin/')
def new_post(request):
    post_content = request.POST.get('post_content')
    post_title = request.POST.get('title')
    max_pid = Post.objects.all().aggregate(max_pid=Max('pid'))
    Post.objects.create(
        pid=max_pid['max_pid'] + 1,
        ptitle=post_title,
        pcontent=post_content,
        pabstract=post_content[0:10],
        pauth=request.user
    )
    return HttpResponseRedirect('/')


@login_required(login_url='/signin/')
def myinfo(request):
    myinfo = request.user

    if request.method == 'POST':
        sname = request.POST.get('name')
        ssex = request.POST.get('sex')
        sinst = request.POST.get('institution')
        sdept = request.POST.get('department')
        sclass = request.POST.get('class')
        signature = request.POST.get('signature')
        models.Student.objects.filter(username=myinfo.username).update(sname=sname, ssex=ssex, sinst=sinst, sdept=sdept,
                                                                       sclass=sclass, signature=signature)
        return HttpResponseRedirect('/myinfo/')
    return render(request, "myinfo.html", {'myinfo': myinfo})


@login_required(login_url='/signin/')
def notice(request):
    return render(request, 'notice.html')


class CommentNoticeListView(LoginRequiredMixin, ListView):
    """通知列表"""
    # 上下文的名称
    context_object_name = 'notices'
    # 模板位置
    template_name = 'notice.html'
    # 登录重定向
    login_url = '/signin/'

    # 未读通知的查询集
    def get_queryset(self):
        return self.request.user.notifications.unread()


class CommentNoticeUpdateView(View):
    """更新通知状态"""

    # 处理 get 请求
    def get(self, request):
        # 获取未读消息
        notice_id = request.GET.get('notice_id')
        # 更新单条通知
        if notice_id:
            post = Post.objects.get(pid=request.GET.get('post_id'))
            request.user.notifications.get(id=notice_id).mark_as_read()
            return redirect('/detail/' + str(post.pid))
        # 更新全部通知
        else:
            request.user.notifications.mark_all_as_read()
            return render(request, 'notice.html')


@login_required(login_url='/signin/')
def search(request):
    keyword = request.GET.get('keyword')
    error_msg = ''

    if not keyword:
        error_msg = '请输入关键词'
        return render(request, 'search.html', {'error_msg': error_msg})

    posts_list = models.Post.objects.filter(ptitle__icontains=keyword)
    page = request.GET.get('page')
    if page == None or int(page) == 0:
        if posts_list.count() < post_per_page:
            has_older = 'disabled'
        end = post_per_page if posts_list.count() > post_per_page else posts_list.count()
        sliced_posts_list = posts_list[:end]
        has_newer = 'disabled'
        return render(request, 'search.html',
                      {'posts_list': sliced_posts_list, 'next_page': 1, 'pre_page': -1,
                       'has_newer': has_newer, 'keyword': keyword, 'has_older': has_older})
    page = int(page)
    if page < 0 or page * post_per_page > posts_list.count():
        pass
    begin = post_per_page * page
    if posts_list.count() > post_per_page * (page + 1):
        end = post_per_page * (page + 1)
        has_older = ''
    else:
        end = posts_list.count()
        has_older = 'disabled'
    sliced_posts_list = posts_list[begin:end]
    return render(request, 'search.html',
                  {'posts_list': sliced_posts_list, 'pre_page': page - 1, 'next_page': page + 1,
                   'has_older': has_older, 'keyword': keyword})
