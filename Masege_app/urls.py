import notifications.urls
from django.urls import path, re_path, include

from Masege_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(r'', views.index),
    path(r'signin/', views.signin),
    path(r'signup/', views.signup),
    re_path(r'detail/(\d+)/', views.post_detail),
    path(r'about/', views.about),
    path(r'signout/', views.signout),
    path(r'sub_comment/', views.sub_comment),
    path(r'new_post/', views.new_post),
    path(r'myinfo/', views.myinfo),
    path(r'search/', views.search),
    path(r'/notifications/', include(notifications.urls, namespace='notifications')),

    path('notice/', views.CommentNoticeListView.as_view(), name='notice'),
    path('update/', views.CommentNoticeUpdateView.as_view(), name='update'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)