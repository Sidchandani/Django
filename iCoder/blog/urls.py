from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blogHome, name="bloghome"),
    path('postComment', views.postComment, name="postComment"),

    # We must keep it al last, otherwise it will catch all the urls & pass it to blogPost func() 
    path('<str:slug>', views.blogPost, name="blogPost")
]
