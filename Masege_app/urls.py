from django.urls import path, re_path

from Masege_app import views

urlpatterns = [
    path(r'', views.index),
    path(r'signin/', views.signin),
    path(r'signup/', views.signup),
    re_path(r'detail/(\d+)/', views.post_detail),
    path(r'about/', views.about),
    path(r'signout/', views.signout),
]
