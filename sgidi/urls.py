from django.conf.urls import url

from sgidi.views import IdeiasView
from . import views


urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^ideias/$', IdeiasView.as_view(), name='ideias'),
    url(r'^ideias/postIdeia/$', IdeiasView.as_view(), name='ideias'),
]