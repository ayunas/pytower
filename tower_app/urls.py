from django.urls import include, path
from django.conf.urls import url
from . import views
from django.conf import settings

urlpatterns = [
    path("start", views.start, name="start"),
    path("play/<slug:id>", views.play, name="play"),
    path("test", views.test, name="test"),
    path("", views.loginPost, name="login-base"),
    url(r"^login/$", views.loginPost, name="login"),
    url(r"^register/$", views.registerPost, name="signup"),
]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns
