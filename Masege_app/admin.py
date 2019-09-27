from django.contrib import admin
from .models import Student, Post

# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'sname', 'sinst', 'sdept', 'sclass')

class PostAdmin(admin.ModelAdmin):
    list_display = ('ptitle', 'pid', 'pauth', 'view_cnt', 'comment_cnt', 'createTime')
    list_filter = ('createTime',)
    search_fields = ('ptitle', 'pauth')


admin.site.register(Student, StudentAdmin)
admin.site.register(Post, PostAdmin)