from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^ideias/$', views.ideias_view, name='ideias'),
]