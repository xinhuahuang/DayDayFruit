from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^index_handle/(\d+)/$', views.index_handle),
    url(r'^list(\d+)/(\d*)/*/*(\d*)/*$', views.list),
    url(r'^detail(\d+)/(\d+)/$', views.detail),
]