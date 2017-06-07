from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'^display/$', views.display),
    url(r'^add/$', views.add),
    url(r'^calcNum/$', views.cart_count),
    url(r'^modify_num/$', views.modify_num),
    url(r'^modify/$', views.modify),
    url(r'^delete_cart/(\d+)/(\d+)/$', views.delete_cart),
    url(r'^cart_count/$', views.cart_count),

]