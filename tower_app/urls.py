from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.loginPost, name='login-base'),
    path('test',views.test, name='test'),
    url(r'^login/$', views.loginPost, name='login'),
    url(r'^register/$', views.registerPost, name='signup'),
    path('start', views.start, name='start'),
    path('play/<slug:id>', views.play, name='play')
]





