from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('play/<slug:id>', views.play, name='play'),
    path('test',views.test,name='test')
]





