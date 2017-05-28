from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from sgidi.views import IdeiasView, IdeiasAvaliacaoView, IdeiasListView, ProjetosDetailView, ConhecimentoCreateView, \
    ConhecimentoListView, ConhecimentoDetailView, UserView, ApagarNotificacao, InterfacesView
from . import views

urlpatterns = [
    # url(r'^auth/asana/callback/$', views.asana_view, name='asana'),
    url(r'^profile/(?P<username>[a-zA-Z0-9]+)/$', login_required(UserView.as_view()), name='profile'),
    url(r'^profile/postTags/$', login_required(UserView.as_view()), name='profle_subscribe_tags'),
    url(r'^$', login_required(views.index_view), name='index'),
    url(r'^ideias/$', login_required(IdeiasListView.as_view()), name='ideias_lista'),
    url(r'^ideias/nova/$', login_required(IdeiasView.as_view(template_name='ideias/ideias_nova.html')), name='ideias_nova'),
    url(r'^ideias/postIdeia/$', login_required(IdeiasView.as_view()), name='ideias_post'),
    url(r'^ideias/avaliacao/(?P<ideia_id>[0-9]+)/$', login_required(IdeiasAvaliacaoView.as_view(template_name='ideias/ideias_avaliacao.html')), name='ideias_avaliacao'),
    url(r'^ideias/avaliacao/mudar_estado/$', login_required(IdeiasAvaliacaoView.as_view()), name='post_atualizar_estado'),
    url(r'^ideias/avaliacao/postPreAnalise/$', login_required(IdeiasAvaliacaoView.as_view()), name='post_pre_analise'),
    url(r'^ideias/avaliacao/postAnalise/$', login_required(IdeiasAvaliacaoView.as_view()), name='post_analise'),
    url(r'^projetos/$', login_required(ProjetosDetailView.as_view()), name='projetos'),
    url(r'^conhecimentos/novo/$', login_required(ConhecimentoCreateView.as_view()), name='conhecimento_novo'),
    url(r'^conhecimentos/$', login_required(ConhecimentoListView.as_view()), name='conhecimento_lista'),
    url(r'^conhecimentos/(?P<pk>[0-9]+)/$', login_required(ConhecimentoDetailView.as_view()), name='conhecimento'),
    url(r'^notificacoes/apagar_notificacao/$', login_required(ApagarNotificacao.as_view()), name='post_apagar_notificacao'),
    url(r'^notificacoes/', login_required(TemplateView.as_view(template_name='notificacoes/notificacoes.html')), name="notificacoes"),
    url(r'^interfaces/', login_required(InterfacesView.as_view()), name="interfaces"),
    url(r'^interfaces/novo/$', login_required(InterfacesView.as_view()), name='atualizar_interfaces'),
]
urlpatterns += staticfiles_urlpatterns() #TODO REMOVER NO FIM DO PROJETO e correr "python manage.py collectstatic"