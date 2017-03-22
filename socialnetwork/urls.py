"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.contrib.auth import views as auth_views
from socialnetwork import views

urlpatterns = [
	url(r'^$', views.home,name='home'),
	url(r'^profile/', views.profile,name="view_profile"),
	url(r'^new_posts', views.new_posts,name="new_posts"),
	url(r'^follow/(?P<post_user>\w+)$', views.follow_user,name="follow"),
	url(r'^unfollow/(?P<post_user>\w+)$', views.un_follow_user,name="unfollow"),
	url(r'^followers_stream$', views.followers,name="followers_stream"),
	url(r'^edit_profile$', views.edit_profile,name="edit_profile"),
	url(r'^create_comment$', views.create_comment,name="comment"),
	url(r'^login$', auth_views.login, {'template_name':'login.html'}, name='login'),
   #Route to logout a user and send them back to the login page (?P<username>w+)$
	url(r'^logout$', auth_views.logout_then_login, name='logout'),
	url(r'^create_post', views.create_post,name='create'),
	url(r'^register$', views.register,name='register'),
	url(r'^profile_picture/(?P<user>\w+)$', views.profile_picture,name='profile_pic'),
	url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',views.confirm_registration, name='confirm'),
]
