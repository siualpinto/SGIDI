#from __future__ import unicode_literals #TODO VERIFICAR PARA QUE SERVE ISTO http://python-future.org/unicode_literals.html
from django.contrib.auth.models import User
from django.db.transaction import commit
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_protect

from sgidi.forms import IdeiasForm, PreAnaliseForm, AnaliseForm
from sgidi.models import Ideias

# Create your views here.

def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'registration/login.html')


# def ideias_view(request):
#     if request.user.is_authenticated:
#         return render(request, 'ideias.html')
#     else:
#         return render(request, 'registration/login.html')




class IdeiasView(View):
    template_name = "ideias.html"
    form_class = IdeiasForm
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return render(request, 'registration/login.html')

    def post(self, request):
        if request.user.is_authenticated:
            form = self.form_class(request.POST)
            if form.is_valid():
                commit = form.save(commit=False) #Pára o auto-commit do django para introduzir campos que não estão no form mas no modelo.
                commit.autor = request.user
                if form.cleaned_data['tipo'] == 4:
                    commit.tipo_nome = form.data['outra_text']
                else:
                    commit.tipo_nome = self.tipos_ideia(form.cleaned_data['tipo'], form)
                commit.estado = 0
                commit.estado_nome = "Em análise"
                commit.save()
                return HttpResponseRedirect('/sgidi/ideias')
            else:
                return render(request, 'ideias.html', {'form': form})
        else:
            return render(request, 'registration/login.html')

    @staticmethod
    def tipos_ideia(__x,tipo):
        return{
            0: "Novo produto",
            1: "Novo processo",
            2: "Melhoria de produto existente",
            3: "Melhoria de processo existente",
        }.get(__x, "erro")



class IdeiasAvaliacaoView(View):
    form_class = PreAnaliseForm
    second_form_class = AnaliseForm
    template_name = "ideias_avaliacao.html"
    estados_ideia = {0: "Em análise", 1: "Projeto", 2: "Arquivada", 3: "Reprovada"}

    def get(self, request, ideia_id):
        if request.user.is_authenticated:
            ideia = Ideias.objects.get(id=ideia_id)
            autor = User.objects.get(id=ideia.autor_id)
            if ideia.autor_pre_analise_id is None:
                avaliador_pre_analise = ideia.autor_pre_analise_id
            else:
                avaliador_pre_analise = User.objects.get(id=ideia.autor_pre_analise_id)

            if ideia.autor_analise_id is not None:
                avaliador_analise = User.objects.get(id=ideia.autor_analise_id)
            else:
                avaliador_analise = ideia.autor_analise_id

            estados = []
            estados_nome = []
            estados_nome.append(ideia.estado_nome)
            estados.append(ideia.estado)
            for key, value in self.estados_ideia.items():
                if key != ideia.estado:
                    estados_nome.append(value)
                    estados.append(key)
            return render(request, self.template_name, {'ideia': ideia, 'autor': autor, 'avaliador1': avaliador_pre_analise, 'avaliador2': avaliador_analise, 'estados_nome': estados_nome, 'estados': estados})
        else:
            return render(request, 'registration/login.html')

    def post(self, request):
        if request.user.is_authenticated:

            if "form1" in request.POST:
                instance = get_object_or_404(Ideias, id=request.POST.get("id", ""))
                form = self.form_class(request.POST, instance=instance)
                if form.is_valid():
                    print("########## FORMULARIO 1 #############"+str(request.POST))
                    commit = form.save(commit=False)
                    commit.autor_pre_analise = request.user
                    print(str(commit))
                    commit.save()
                    return HttpResponseRedirect('/sgidi/ideias/avaliacao/'+request.POST.get("id", ""))
                else:
                    return render(request, 'ideias_avaliacao.html', {'form': form})

            elif "form2" in request.POST:
                instance = get_object_or_404(Ideias, id=request.POST.get("id", ""))
                form = self.second_form_class(request.POST, instance=instance)
                if form.is_valid():
                    commit = form.save(commit=False)
                    commit.autor_analise = request.user
                    print(str(commit))
                    commit.save()
                    return HttpResponseRedirect('/sgidi/ideias/avaliacao/' + request.POST.get("id", ""))
                else:
                    return render(request, 'ideias_avaliacao.html', {'form': form})

            elif request.is_ajax():
                estado = request.POST.get('estado', "error_estado")
                estado_nome = request.POST.get('estado_nome', "error_estado_nome")
                ideia_id = request.POST.get('ideia_id', "error_ideia_id")
                data = {
                    "ideia": Ideias.objects.filter(id=ideia_id).update(estado_nome=estado_nome, estado=estado),
                }
                return JsonResponse(data)

        else:
            return render(request, 'registration/login.html')




#@csrf_exempt TODO Descomentar para funcionar sem token
# @csrf_protect
# def post_atualizar_estado(request):
#     print("asdasopdkqkweopqwkddpo213890217591208301283")
#     if request.is_ajax():
#         if request.user.is_authenticated:
#             estado = request.GET.get('estado',None)
#             estado_nome = request.GET.get('estado_nome',None)
#             ideia_id = request.GET.get('ideia_id',None)
#
#             data = {
#                 "ideia" : Ideias.objects.filter(id=ideia_id).update(estado_nome=estado_nome, estado=estado),
#             }
#             return JsonResponse(data)
#         else:
#             return render(request, 'registration/login.html')
