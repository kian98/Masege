from django.urls import path, re_path

from Masege_app import views

urlpatterns = [
    path(r'', views.index),
    re_path(r'detail/(\d+)/', views.post_detail),
]
