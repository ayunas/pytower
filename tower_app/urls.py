from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('start',views.index,name='index'),
    path('play/<slug:id>', views.play, name='play'),
    path('test',views.test,name='test'),
    path('',views.loginPost,name='login-base'),
    url(r'^login/$', views.loginPost, name='login'),
    url(r'^register/$', views.registerPost, name='signup'),
]
