from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

app_name = "post"

urlpatterns = [
	url(r'^users/$', views.UsersView.as_view(), name='users'),
	url(r'^login/$', auth_views.LoginView.as_view(template_name='post/login.html'), name='login'),
	url(r'^dashboard/$', views.Dashboard.as_view(), name='dashboard'),
	url(r'^post/add/$', views.PostCreate.as_view(), name='post_add'),
	url(r'^post/(?P<pk>[\d]+)/$', views.PostDetail.as_view(), name='post_detail'),
    url(r'^$', views.Home.as_view(), name='home'),
]