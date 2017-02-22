#from __future__ import unicode_literals #TODO VERIFICAR PARA QUE SERVE ISTO http://python-future.org/unicode_literals.html

from django.db.transaction import commit
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_protect

from sgidi.forms import IdeiasForm

# Create your views here.

# TODO Verificar a autenticação do user, em cada função automaticamente (ATUALIDADE: sem repetição de code )
def index_view(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        return HttpResponseRedirect('/login/')


def ideias_view(request):
    if request.user.is_authenticated():
        return render(request, 'ideias.html')
    else:
        return HttpResponseRedirect('/login/')



class IdeiasView(View):
    print("asdasd")
    def post(self,request):
        print("ideias")
        if request.user.is_authenticated():
            form = IdeiasForm(request.POST)
            if form.is_valid():
                commit = form.save(commit=False) #TODO comentar para k serve este commit
                commit.autor = request.user
                teste = "asd"
                teste = form.data['outra_text']
                commit.tipo_nome = self.tipos_ideia(form.cleaned_data['tipo'], teste)
                commit.tipo_nome = self.tipos_ideia(0, form)
                commit.save()
                return HttpResponseRedirect('/sgidi/ideias')
            else:
                print("Não é válido")
                # form = IdeiasForm(initial={'key': 'value'})
                return render(request, 'ideias.html', {'form': form})

        else:
            return HttpResponseRedirect('/login/')

    @staticmethod
    def tipos_ideia(__x,form):
        return{
            0: "Novo produto",
            1: "Novo processo",
            2: "Melhoria de produto existente",
            3: "Melhoria de processo existente",
            4: form,
        }.get(__x,"erro")

# def post_ideias(request):
#     print("ideias")
#     if request.user.is_authenticated():
#         form = IdeiasForm(request.POST)
#         if form.is_valid():
#             nome = form.cleaned_data['nome']
#             print("Teste "+str(nome))
#             commit = form.save(commit=False)
#             commit.autor = request.user
#             commit.save()
#             return HttpResponseRedirect('/ideias/')
#         else:
#             print("Não é válido")
#             #form = IdeiasForm(initial={'key': 'value'})
#             return render(request, 'ideias.html', {'form': form})
#
#     else:
#         return  HttpResponseRedirect('/login/')


