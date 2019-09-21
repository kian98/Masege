from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    # User模型自带有username password date_joined is_superuser
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # # 学号 primary_key=True: 该字段为主键
    # sno = models.IntegerField(primary_key=True)
    # # 密码 字符串 最大长度30 不可为空
    # spwd = models.CharField(max_length=30, null=False)

    # 姓名 字符串 最大长度20
    sname = models.CharField(max_length=20)
    # 性别 布尔类型 默认True: 男生 False:女生
    ssex = models.BooleanField(default=True)

    # # 创建时间 auto_now_add：只有在新增的时候才会生效
    # registTime = models.DateTimeField(auto_now_add=True)

    # 学院
    sinst = models.CharField(max_length=30)
    # 专业
    sdept = models.CharField(max_length=30)
    # 班级
    sclass = models.CharField(max_length=30)

    # 头像
    avatar = models.ImageField(upload_to='uploads_imgs/', default='uploads_imgs/default.jpg')
    # 自我介绍
    signature = models.CharField(max_length=128, default='The quick brown fox jumps over the lazy dog.')


    def __unicode__(self):
        return ' '.join(self.user.username, self.sname)


class Posts(models.Model):
    # 帖子id
    pid = models.IntegerField(primary_key=True)
    # 帖子标题
    ptitle = models.CharField(max_length=64)
    # 内容
    pcontent = models.TextField(null=False)
    # 作者
    pauth = models.ForeignKey('Student', on_delete=models.CASCADE)
    # 查看数
    view_cnt = models.IntegerField()
    # 点赞数
    like_cnt = models.IntegerField()
    # 置顶排名
    ranking = models.IntegerField()
    # 创建日期
    createTime = models.DateTimeField(auto_now_add=True)
    # 更新日期
    updateTime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.ptitle
