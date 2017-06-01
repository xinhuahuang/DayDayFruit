from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^user_exit/$', views.user_exit),
]
