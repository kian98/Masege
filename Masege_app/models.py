from django.db import models
from django.contrib.auth.models import AbstractUser
from django_comments.models import Comment
from django.db.models.signals import post_save, post_delete,pre_delete
from django.dispatch import receiver

class Student(AbstractUser):

    # # 学号 primary_key=True: 该字段为主键
    # sno = models.IntegerField(primary_key=True)
    # # 密码 字符串 最大长度30 不可为空
    # spwd = models.CharField(max_length=30, null=False)

    # 姓名 字符串 最大长度20
    sname = models.CharField('姓名', max_length=20, default="某热心网友")
    # 性别 布尔类型 默认True: 男生 False:女生
    ssex = models.BooleanField('性别', default=True)

    # # 创建时间 auto_now_add：只有在新增的时候才会生效
    # registTime = models.DateTimeField(auto_now_add=True)

    # 学院
    sinst = models.CharField('学院', max_length=30)
    # 专业
    sdept = models.CharField('专业', max_length=30)
    # 班级
    sclass = models.CharField('班级', max_length=30)

    # 头像
    avatar = models.ImageField('头像', upload_to='', default='static/image/info-image.jpg')
    # 自我介绍
    signature = models.CharField('个性签名', max_length=128, default='The quick brown fox jumps over the lazy dog.')


    def __unicode__(self):
        return ' '.join(self.user.username, self.sname)


class Post(models.Model):
    # 帖子id
    pid = models.IntegerField('ID', primary_key=True)
    # 帖子标题
    ptitle = models.CharField('标题', max_length=64)
    # 摘要
    pabstract = models.CharField('摘要', max_length=20, default='')
    # 内容
    pcontent = models.TextField('内容', null=False)
    # 作者
    pauth = models.ForeignKey('Student', on_delete=models.CASCADE)
    # 查看数
    view_cnt = models.IntegerField('阅读量', default=0)
    # 点赞数
    like_cnt = models.IntegerField('点赞量', default=0)
    # 评论数
    comment_cnt = models.IntegerField('评论量', default=0)
    # 置顶排名
    ranking = models.IntegerField('排名', default=-1)
    # 创建日期
    createTime = models.DateTimeField('创建日期', auto_now_add=True)
    # 更新日期
    updateTime = models.DateTimeField('更新日期', auto_now=True)

    def __unicode__(self):
        return self.ptitle


@receiver(pre_delete, sender=Comment)
def before_delete_comment(sender, instance, **kwargs):
    post = Post.objects.get(pid=instance.object_pk)
    post.comment_cnt -= 1
    post.save()