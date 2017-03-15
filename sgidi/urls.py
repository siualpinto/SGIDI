from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from sgidi.views import IdeiasView, IdeiasAvaliacaoView, IdeiasListView
from . import views

urlpatterns = [
    url(r'^$', views.index_view, name='index'),
    url(r'^ideias/$', IdeiasListView.as_view(), name='ideias_lista'),
    url(r'^ideias/nova/$', IdeiasView.as_view(template_name='ideias/ideias_nova.html'), name='ideias_nova'),
    url(r'^ideias/postIdeia/$', IdeiasView.as_view(), name='ideias_post'),
    url(r'^ideias/avaliacao/(?P<ideia_id>[0-9]+)/$', IdeiasAvaliacaoView.as_view(template_name='ideias/ideias_avaliacao.html'), name='ideias_avaliacao'),
    url(r'^ideias/avaliacao/mudar_estado/$', IdeiasAvaliacaoView.as_view(), name='post_atualizar_estado'),
    url(r'^ideias/avaliacao/postPreAnalise/$', IdeiasAvaliacaoView.as_view(), name='post_pre_analise'),
    url(r'^ideias/avaliacao/postAnalise/$', IdeiasAvaliacaoView.as_view(), name='post_analise'),
]
urlpatterns += staticfiles_urlpatterns() #TODO REMOVER NO FIM DO PROJETO e correr "python manage.py collectstatic"