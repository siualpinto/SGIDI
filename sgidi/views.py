#from __future__ import unicode_literals #TODO VERIFICAR PARA QUE SERVE ISTO http://python-future.org/unicode_literals.html

from django.db.transaction import commit

from django.http import HttpResponseRedirect
from django.shortcuts import render
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


def post_ideias(request):
    if request.user.is_authenticated():
        form = IdeiasForm(request.POST)
        if form.is_valid():
            commit.Autor = request.user.id
            commit.save()
            return HttpResponseRedirect('/ideias/')
       # else
           # return render(request, 'error.html', {"erro": "erro"})

