#from __future__ import unicode_literals #TODO VERIFICAR PARA QUE SERVE ISTO http://python-future.org/unicode_literals.html
from django.contrib.auth.models import User
from django.db.transaction import commit
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, render_to_response
from django.views import View
from django.views.decorators.csrf import csrf_protect

from sgidi.forms import IdeiasForm
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
    print("##############""############")
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
                return render(request,'ideias.html', {'form': form})
        else:
            return render(request, 'registration/login.html')

    @staticmethod
    def tipos_ideia(__x,tipo):
        return{
            0: "Novo produto",
            1: "Novo processo",
            2: "Melhoria de produto existente",
            3: "Melhoria de processo existente",
        }.get(__x,"erro")



class IdeiasAvaliacaoView(View):
    template_name = "ideias_avaliacao.html"
    estados_ideia = {0: "Em análise", 1: "Projeto", 2: "Arquivada", 3: "Reprovada"}

    def get(self, request, ideia_id):
        if request.user.is_authenticated:
            ideia = Ideias.objects.get(id=ideia_id)
            autor = User.objects.get(id=ideia.autor_id)
            estados = []
            estados_nome = []
            estados_nome.append(ideia.estado_nome)
            estados.append(ideia.estado)
            for key, value in self.estados_ideia.items():
                if key != ideia.estado:
                    estados_nome.append(value)
                    estados.append(key)
            return render(request, self.template_name,{'ideia':ideia,'autor':autor,'estados_nome':estados_nome,'estados':estados})
        else:
            return render(request, 'registration/login.html')

@csrf_protect
def post_atualizar_estado(request):
    print("asdasopdkqkweopqwkddpo213890217591208301283")
    if request.is_ajax():
        if request.user.is_authenticated:
            estado = request.GET.get('estado',None)
            estado_nome = request.GET.get('estado_nome',None)
            ideia_id = request.GET.get('ideia_id',None)

            data = {
                "ideia":Ideias.objects.filter(id=ideia_id).update(estado_nome=estado_nome,estado=estado),
            }
            return JsonResponse(data)
        else:
            return render(request, 'registration/login.html')



















