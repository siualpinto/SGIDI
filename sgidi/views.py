import json
from itertools import chain

import asana
from django.contrib.auth.models import User
from operator import attrgetter
import operator
from django.conf import settings
from django.db.models import Q
from functools import reduce
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from notifications.signals import notify
from django.views.generic import DetailView, CreateView, ListView
from notifications.views import AllNotificationsList, NotificationViewList

from sgidi.forms import IdeiasForm, PreAnaliseForm, AnaliseForm, ConhecimentoForm
from sgidi.models import Ideias, Analises, AnalisesDefault, Tokens, Conhecimentos, Tags

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Create your views here.

# @csrf_protect
# def login_user(request):
#     logout(request)
#     username = password = ''
#     if request.POST:
#         username = request.POST['username']
#         password = request.POST['password']
#
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 # me = client.users.me()
#                 #projects_id = me['projects'][0]['id']
#                 #project = client.projects.create_in_workspace(projects_id, {'name': 'new project'})
#                 #print("Created project with id: " + str(project['id']))
#                 return render(request, 'index.html')
#     return render(request, 'registration/login.html')

# @csrf_protect
# def asana_view(request):
#     print("ASANA")
#     if request.params['state'] == state:
#         token = client.session.fetch_token(code=request.params['code'])
#         return render(request, 'index.html')
#     else:
#         return render(request, 'registration/login.html')
#
# # error! possible CSRF attack


def index_view(request):
    return render(request, 'index.html')
    # if request.user.is_authenticated:
    #     return render(request, 'index.html')
    #     (url, state) = client.session.authorization_url()
    #     print(url)
    #     if request.params['state'] == state:
    #         token = client.session.fetch_token(code=request.params['code'])
    #         # ...
    #     else:
    #         return render(request, 'registration/login.html')
    # else:
    #     return render(request, 'registration/login.html')


# error! possible CSRF attack
# return redirect(url)
# if request.params['state'] == state:
#     token = client.session.fetch_token(code=request.params['code'])
#     return redirect(url)
# else:
#     return render(request, 'index.html')
# error! possible CSRF attack


class IdeiasView(View):
    template_name = "ideias_nova.html"
    form_class = IdeiasForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            commit = form.save(
                commit=False)  # Pára o auto-commit do django para introduzir campos que não estão no form mas no modelo.
            commit.autor = request.user
            if form.cleaned_data['tipo'] == 4:
                commit.tipo_nome = form.data['outra_text']
            else:
                commit.tipo_nome = self.tipos_ideia(form.cleaned_data['tipo'], form)
            commit.estado = 0
            commit.estado_nome = "Em análise"
            commit.save()
            analises_default = AnalisesDefault.objects.all()
            for analise in analises_default:
                Analises.objects.create(ideia=commit, ordem=(analise.id - 1), peso=analise.peso, tipo=1, avaliacao=analise.avaliacao)
            return HttpResponseRedirect('/ideias')
        else:
            return render(request, 'ideias/ideias_nova.html', {'form': form})

    @staticmethod
    def tipos_ideia(__x, tipo):
        return {
            0: "Novo produto",
            1: "Novo processo",
            2: "Melhoria de produto existente",
            3: "Melhoria de processo existente",
        }.get(__x, "erro_tipos_ideia")


class IdeiasAvaliacaoView(View):
    form_class = PreAnaliseForm
    second_form_class = AnaliseForm
    template_name = "ideias_avaliacao.html"
    estados_ideia_dic = {
        0: "Em análise",
        1: "Projeto",
        2: "Arquivada",
        3: "Reprovada"}

    def get(self, request, ideia_id):
        ideia = get_object_or_404(Ideias, id=ideia_id)
        autor = get_object_or_404(User, id=ideia.autor_id)
        analises = list(Analises.objects.filter(ideia_id=ideia_id))

        if ideia.autor_pre_analise_id is None:
            avaliador_pre_analise = ideia.autor_pre_analise_id
        else:
            avaliador_pre_analise = User.objects.get(id=ideia.autor_pre_analise_id)

        if ideia.autor_analise_id is not None:
            avaliador_analise = User.objects.get(id=ideia.autor_analise_id)
        else:
            avaliador_analise = ideia.autor_analise_id
        estados = {}
        estados.update({ideia.estado: ideia.estado_nome})
        for key, value in self.estados_ideia_dic.items():
            if key != ideia.estado:
                estados.update({key: value})
        tipos_avaliacao = {}

        for a in analises:
            tipos_avaliacao.setdefault(a.ordem, [])
            tipos_avaliacao[a.ordem].append(a.avaliacao)
            tipos_avaliacao[a.ordem].append(a.tipo)
            tipos_avaliacao[a.ordem].append(a.peso)
        return render(request, self.template_name,
                      {'ideia': ideia, 'autor': autor, 'avaliador1': avaliador_pre_analise,
                       'avaliador2': avaliador_analise,
                       'estados': estados.items(), 'tipos_avalicao': sorted(tipos_avaliacao.items())})

    def post(self, request):
        if "form1" in request.POST:
            instance = get_object_or_404(Ideias, id=request.POST.get("id", ""))
            form = self.form_class(request.POST, instance=instance)
            if form.is_valid():
                commit = form.save(commit=False)
                commit.autor_pre_analise = request.user
                commit.data_pre_analise = timezone.now()
                commit.save()
                return HttpResponseRedirect('/ideias/avaliacao/' + request.POST.get("id", ""))
            else:
                return render(request, 'ideias/ideias_avaliacao.html', {'form': form})

        elif "form2" in request.POST:
            ideia_id = request.POST.get("id", "")
            instance = get_object_or_404(Ideias, id=ideia_id)
            form = self.second_form_class(request.POST, instance=instance)
            analises = list(Analises.objects.filter(ordem__gte=8, ideia_id=ideia_id))
            if form.is_valid():
                commit = form.save(commit=False)
                commit.autor_analise = request.user
                commit.data_analise = timezone.now()
                commit.save()
                avaliacoes = {}
                for key, value in request.POST.items():
                    if key.startswith('avaliacao'):
                        avaliacoes.setdefault(key[+9:], [])
                        avaliacoes[key[+9:]].append(value)
                    if key.startswith('tipo'):
                        avaliacoes[key[+4:]].append(value)
                    if key.startswith('peso'):
                        avaliacoes[key[+4:]].append(value)
                for key, value in avaliacoes.items():
                    Analises.objects.update_or_create(ideia_id=ideia_id, ordem=key,
                                                      defaults={"avaliacao": value[0], "tipo": value[1], "peso": value[2]})
                for a in analises:
                    if str(a.ordem) not in avaliacoes.keys():
                        Analises.objects.filter(ideia_id=a.ideia_id, ordem=a.ordem).delete()

                return HttpResponseRedirect('/ideias/avaliacao/' + ideia_id)
            else:
                return render(request, 'ideias/ideias_avaliacao.html', {'form': form})

        elif request.is_ajax():
            estado = request.POST.get('estado', "error_estado")
            estado_nome = request.POST.get('estado_nome', "error_estado_nome")
            ideia_id = request.POST.get('ideia_id', "error_ideia_id")
            data = {
                "ideia": Ideias.objects.filter(id=ideia_id).update(estado_nome=estado_nome, estado=estado),
            }
            return JsonResponse(data)


class IdeiasListView(ListView):
    template_name = "ideias/ideias.html"
    model = Ideias
    queryset = Ideias.objects.order_by('-data')
    allow_empty = True
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """add range template context variable that we can loop through pages"""
        context = super(IdeiasListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context


#  Token
# client = asana.Client.access_token('0/8f62a923af9681d7530fe81d36ea3f0b')


class ProjetosDetailView(View):
    template_name = "projetos/projetos.html"

    def get(self, request, *args, **kwargs):
        data = {'projects': [], 'fullprojects':[], 'tasks': [], 'subtasks':[]}
        # client = asana.Client.access_token('0/ce4e5bf93acd15f0121a88a142be4548')
        token = get_object_or_404(Tokens, user_id=request.user.id)
        client = asana.Client.access_token(token.token)


        me = client.users.me()
        workspace_id = me['workspaces'][0]['id']
        projects = client.projects.find_by_workspace(workspace_id)
        for project in projects:
            data['projects'].append(project)
            # full_project = client.projects.find_by_id(project['id'])
            # data['fullprojects'].append(full_project)
            # data['projects'].append(full_project)
            # tasks = client.projects.tasks(project['id'])
            # for task in tasks:
            #     data['tasks'].append(client.tasks.find_by_id(task['id']))
            #     # data['tasks'].append(client.tasks.find_by_id(task.id))
            #     subtasks = client.tasks.subtasks(task['id'])
            #     for subtask in subtasks:
            #         data['subtasks'].append(client.tasks.find_by_id(subtask['id']))
        # return HttpResponse(json.dumps(data['projects'][0]), content_type="application/json")
        return render(request, self.template_name, {'projects': data['projects'], 'fullprojects': data['fullprojects'], 'token': token.token})


class ConhecimentoCreateView(CreateView):
    template_name = 'conhecimento/conhecimento_novo.html'
    model = Conhecimentos
    form_class = ConhecimentoForm

    def get(self, request, *args, **kwargs):
        super(ConhecimentoCreateView, self).get(request, *args, **kwargs)
        form = self.form_class
        tags = Tags.objects.order_by('-id')
        return self.render_to_response(self.get_context_data(
            object=self.object, form=form, tags=tags))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            commit_connhecimento = form.save(commit=False)
            commit_connhecimento.autor = request.user
            commit_connhecimento.save()
            tags = ""
            result_list = []
            for tag in request.POST.getlist("existing_tag", ""):
                obj, created = Tags.objects.update_or_create(tag=tag)
                commit_connhecimento.tag.add(obj.id)
                tags += ", " + str(obj)
                result_list = sorted(
                    chain(obj.user.all(), result_list),
                    key=attrgetter('username'))
            for user in list(set(result_list)):
                notify.send(request.user, recipient=user,
                            verb='introduziu uma nova aprendizagem com as seguintes tags' + tags,
                            description=str(commit_connhecimento.id))
            return HttpResponseRedirect('/conhecimentos/')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ConhecimentoListView(ListView):
    template_name = 'conhecimento/conhecimentos.html'
    model = Conhecimentos
    paginate_by = 14

    def get_queryset(self):
        try:
            query = self.request.GET.get('query')
        except:
            query = ''
        if query is None:
            query = ''
        if (query != ''):
            object_list = Conhecimentos.objects.filter(Q(titulo__icontains=query) | Q(texto__icontains=query) | Q(tag__tag__icontains=query) | Q(autor__username__icontains=query) | Q(data__icontains=query)).distinct()
        else:
            object_list = Conhecimentos.objects.order_by('-data').filter(autor=self.request.user)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(ConhecimentoListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context


class ConhecimentoDetailView(DetailView):
    template_name = 'conhecimento/conhecimento.html'
    model = Conhecimentos

    def get_context_data(self, **kwargs):
        context = super(ConhecimentoDetailView, self).get_context_data(**kwargs)
        context['tags'] = context['conhecimentos'].tag.all()
        return context


class UserView(View):
    template_name = "user/profile.html"

    def get(self, request, username):
        user = User.objects.get(username=username)
        tags_db = Tags.objects.all()
        tags = {}
        for tag in tags_db:
            tags.setdefault(tag.id, [])
            tags[tag.id].append(tag.tag)
            for user_tag in tag.user.all():
                if str(user_tag) == request.user.username:
                    tags[tag.id].append(1)
        return render(request, 'user/profile.html', {"user": user, "user_tags": tags.items(), "all_tags": tags_db})

    def post(self, request, *args, **kwargs):
        tags_db = Tags.objects.all()
        for tag in tags_db:
            tag.user.remove(request.user)
        for tag in request.POST.getlist("existing_tag", ""):
            tag_db = Tags.objects.get(tag=tag)
            tag_db.user.add(request.user.id)
        return HttpResponseRedirect('/profile/'+str(request.user.username))


