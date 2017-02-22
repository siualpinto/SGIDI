#from __future__ import unicode_literals #TODO VERIFICAR PARA QUE SERVE ISTO http://python-future.org/unicode_literals.html

from django.db.transaction import commit
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views import View
from django.views.decorators.csrf import csrf_protect

from sgidi.forms import IdeiasForm

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

    def post(self,request):
        print("ideias")
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
    def tipos_ideia(__x,form):
        return{
            0: "Novo produto",
            1: "Novo processo",
            2: "Melhoria de produto existente",
            3: "Melhoria de processo existente",
        }.get(__x,"erro")



