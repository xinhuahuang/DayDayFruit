from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^display/$', views.display),
    url(r'^add(\d+)/(\d+)/$', views.add),
    url(r'^calcNum/$', views.cart_count),
    url(r'^modify_num(\d+)/(-*\d+)/$', views.modify_num),
    url(r'^modify(\d+)/(-*\d+)/$', views.modify),
    url(r'^delete_cart/(\d+)/$', views.delete_cart),
    url(r'^cart_count/$', views.cart_count),

]