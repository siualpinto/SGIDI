import json
from itertools import chain
from django.contrib.auth.models import Group
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
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views import View
from django.utils import timezone
from notifications.models import Notification
from notifications.signals import notify
from django.views.generic import DetailView, CreateView, ListView
from notifications.views import AllNotificationsList, NotificationViewList

from sgidi.forms import IdeiasForm, PreAnaliseForm, AnaliseForm, ConhecimentoForm
from sgidi.models import Ideias, Analises, AnalisesDefault, Tokens, Conhecimentos, Tags, Projetos, Tasks

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
                            description="tag-"+str(commit_connhecimento.id))
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
        if query != '':
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


class ApagarNotificacao(View):

    def post(self, request):
        if request.is_ajax():
            notificacao_id = request.POST.get('notificacao_id', "error_notificacao_id")
            data = {
                "notificacao": Notification.objects.get(id=notificacao_id).delete(),
            }
            return JsonResponse(data)


class InterfacesView(View):
    template = "interfaces/interfaces.html"
    # form_class = ProjetoForm
    # TODO O BOTAO DE ATUALIZAR AS INTERFACES DEVE SER REDIRECIONADO PARA AQUI MAS COM ATUALIZAÇÃO DA DB

    def get(self, request, atualizar = None):
        # form = self.form_class
        token = get_object_or_404(Tokens, user_id=request.user.id)

        id_projeto = 2
        id_asana_projeto = 299870043677028
        if request.get_full_path() == '/interfaces/atualizar/':
            grupo = Group.objects.get(name='grupo_atividades')
            project, created = saveproject(token, 2)
            created_final, new_tasks, modified_final, modified_tasks = saveprojecttasks(token, id_projeto, id_asana_projeto)
            if created_final:
                new_tasks_str = ""
                for new_task in new_tasks.values():
                    new_tasks_str += ", " + str(new_task)
                print(new_tasks)
                notify.send(request.user, recipient=grupo,
                            verb='Foram inseridas novas tasks no SGIDI Atividades'+new_tasks_str,
                            description='atividades-')

            if modified_final:
                modified_tasks_str = ""
                for modified_task in modified_tasks.values():
                    modified_tasks_str += ", " + str(modified_task)
                print(modified_tasks)
                notify.send(request.user, recipient=grupo,
                            verb='Foram alteradas algumas tasks no SGIDI Atividades' + modified_tasks_str,
                            description='atividades-')

        project = Projetos.objects.get(pk=id_projeto)
        # tasks = Tasks.objects.filter(projeto_id=210156681957457, parent=None, section=0)
        # subtasks = Tasks.objects.filter(projeto_id=210156681957457, section=0).exclude(parent__isnull=True)
        # sections = Tasks.objects.filter(projeto_id=210156681957457, parent=None, section=1)

        # TODO SEMPRE QUE SE ATUALIZAR A DB, VERIFICAR SE A MODIFIED DATA MUDOU FEITO!!!!
        # TODO SE SIM: MANDAR UM ALERT COM A TASK QUE FOI ALTERADA              FEITO!!!!

        # TODO E TAMBÉM SEMPRE QUE SURGIR UMA TASK NOVA                 FEITO!!!!
        # TODO PODE SER VERIFICADO CREATED DEVOLVIDO                    FEITO!!!!
        # TODO A NOTIFICAÇÃO MANDADA PODE SER PARA UM GRUPO CRIADO NA PAGINA DE ADMIN LIGADO AO SGIDI ATIVIDADES   FEITO!!!!

        tasks = Tasks.objects.filter(projeto_id=id_asana_projeto, parent=None, section=0)
        subtasks = Tasks.objects.filter(projeto_id=id_asana_projeto, section=0).exclude(parent__isnull=True)
        sections = Tasks.objects.filter(projeto_id=id_asana_projeto, parent=None, section=1)
        return render(request, self.template, {'token': token.token, 'project': project, 'tasks': tasks, 'subtasks': subtasks, 'sections': sections})


def saveproject(token, id_db):
    client = asana.Client.access_token(token.token)
    project = client.projects.find_by_id(Projetos.objects.get(pk=id_db).id_asana)
    status = 0
    if project['current_status'] is not None:
        if project['current_status']['color'] == 'green':
            status = 0
        elif project['current_status']['color'] == 'yellow':
            status = 1
        elif project['current_status']['color'] == 'red':
            status = 2

    return Projetos.objects.update_or_create(id_asana=project['id'],
                                             defaults={'name': project['name'],
                                                       'notes': 'Sem Notas' if  project['notes'] == '' else project['notes'],
                                                       'current_status': status,
                                                       'current_status_text': 'Sem estado' if project['current_status'] is None
                                                       else project['current_status']['text'],
                                                       'due_date': project['due_date'],
                                                       'created_at': project['created_at'],
                                                       'modified_at': project['modified_at']
                                                       })


def saveprojecttasks(token, id_db, id_asana):
    client = asana.Client.access_token(token.token)
    projeto_id = Projetos.objects.get(pk=id_db).id_asana
    tasks = client.tasks.find_by_project(projeto_id)
    sections = client.projects.sections(projeto_id)
    section_id = 0
    new_tasks_id = 0
    modified_tasks_id = 0
    created_final = False
    modified_final = False
    modified_tmp = False
    new_tasks = {}
    modified_tasks = {}
    tasks_db = Tasks.objects.filter(projeto_id=id_asana)
    for task in tasks:
        task_asana = client.tasks.find_by_id(task['id'])
        try:
            if task_asana['memberships'] is not None:
                members = task_asana['memberships']
                for member in members:
                    if member['section'] is not None:
                        section_id = member['section']['id']
        except ValueError:
            print(ValueError)
        if tasks_db.filter(id_asana=task['id']).exists():
            data_1 = task_asana['modified_at'][:-1]
            data_2 = tasks_db.get(id_asana=task['id']).modified_at.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]
            if data_1 != data_2:
                print("task modificada")
                modified_final = True
                modified_tmp = True
        task_db, created = Tasks.objects.update_or_create(id_asana=task['id'],
                                                          defaults={'name': task_asana['name'],
                                                                    'notes': task_asana['notes'],
                                                                    'assignee': 'Sem atribuição' if task_asana['assignee'] is None
                                                                    else task_asana['assignee']['name'],
                                                                    'assignee_status': 'Sem atribuição' if task_asana['assignee_status']
                                                                                                           is None else task_asana['assignee_status'],
                                                                    'completed': task_asana['completed'],
                                                                    'created_at': task_asana['created_at'],
                                                                    'completed_at': task_asana['completed_at'],
                                                                    'due_at': task_asana['due_at'],
                                                                    'due_on': task_asana['due_on'],
                                                                    'modified_at': task_asana['modified_at'],
                                                                    'section': False,
                                                                    'projeto_id': projeto_id,
                                                                    'section_id': section_id
                                                                    })
        if modified_tmp:
            modified_tasks.setdefault(modified_tasks_id, [])
            modified_tasks[modified_tasks_id].append(tasks_db.filter(id_asana=task['id']).get().name)
            modified_tasks_id = modified_tasks_id + 1
            modified_tmp = False
        if created:
            new_tasks.setdefault(new_tasks_id, [])
            new_tasks[new_tasks_id].append(task_db.name)
            new_tasks_id = new_tasks_id+1
        created_final = created_final | created
        subtasks = client.tasks.subtasks(task=task['id'])
        for task_db in tasks_db:
            if task_db.name == task['name']:
                tasks_db = tasks_db.exclude(name=task['name'])
        for subtask_compact in subtasks:
            subtask = client.tasks.find_by_id(subtask_compact['id'])
            for task_db in tasks_db:
                if task_db.name == subtask['name']:
                    tasks_db = tasks_db.exclude(name=subtask['name'])
            Tasks.objects.update_or_create(id_asana=subtask['id'],
                                           defaults={'name': subtask['name'],
                                                     'notes': subtask['notes'],
                                                     'assignee': 'Sem atribuição' if subtask['assignee'] is None
                                                     else subtask['assignee']['name'],
                                                     'assignee_status': 'Sem atribuição' if subtask[
                                                                                                'assignee_status']
                                                                                            is None else subtask[
                                                         'assignee_status'],
                                                     'completed': subtask['completed'],
                                                     'created_at': subtask['created_at'],
                                                     'completed_at': subtask['completed_at'],
                                                     'due_at': subtask['due_at'],
                                                     'due_on': subtask['due_on'],
                                                     'modified_at': subtask['modified_at'],
                                                     'section': False,
                                                     'projeto_id': projeto_id,
                                                     'section_id': '0',
                                                     'parent_id': task_db.id
                                                     })
    for section in sections:
        Tasks.objects.filter(id_asana=section['id']).update(section=True)
    tasks_db.delete()

    return created_final, new_tasks, modified_final, modified_tasks

