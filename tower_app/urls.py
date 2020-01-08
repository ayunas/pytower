from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('^play/([1-9])\w+/$', views.play, name='play'),
    path('test',views.test,name='test')
]




