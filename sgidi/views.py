from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404 , get_list_or_404
from django.views import View
from django.utils import timezone
from django.views.generic.list import ListView
from sgidi.forms import IdeiasForm, PreAnaliseForm, AnaliseForm
from sgidi.models import Ideias, Analises


# Create your views here.

def index_view(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'registration/login.html')


class IdeiasView(View):
    template_name = "ideias_nova.html"
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
                for x in range(8):
                    Analises.objects.create(ideia=commit, ordem=x, peso=1, tipo=1)
                return HttpResponseRedirect('/sgidi/ideias')
            else:
                return render(request, 'ideias_nova.html', {'form': form})
        else:
            return render(request, 'registration/login.html')

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
    tipos_avaliacao_dic = {
        0: "Duração e custo do projeto",
        1: "Impacto no cliente e impacto no volume de vendas",
        2: "Grau de inovação",
        3: "Fatores de risco",
        4: "Requisitos legais, sociais, tecnológicos e financeiros",
        5: "Estabelecimento de parcerias com entidades do SCTN",
        6: "Coerência com os objetivos de IDI",
        7: "Aprovação da Gestão de Topo"}

    def get(self, request, ideia_id):
        if request.user.is_authenticated:
            ideia = get_object_or_404(Ideias, id=ideia_id)
            autor = get_object_or_404(User, id=ideia.autor_id)
            analises = list(Analises.objects.filter(ordem__gte=8, ideia_id=ideia_id))

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
            for key, value in self.tipos_avaliacao_dic.items():
                tipos_avaliacao.setdefault(key, [])
                tipos_avaliacao[key].append(value)
                tipos_avaliacao[key].append(
                    Analises.objects.values_list('tipo', flat=True).get(ideia=ideia_id, ordem=key))
                tipos_avaliacao[key].append(
                    Analises.objects.values_list('peso', flat=True).get(ideia=ideia_id, ordem=key))

            for a in analises:
                tipos_avaliacao.setdefault(a.ordem, [])
                tipos_avaliacao[a.ordem].append(a.avaliacao)
                tipos_avaliacao[a.ordem].append(a.tipo)
                tipos_avaliacao[a.ordem].append(a.peso)
            return render(request, self.template_name,
                          {'ideia': ideia, 'autor': autor, 'avaliador1': avaliador_pre_analise,
                           'avaliador2': avaliador_analise,
                           'estados': estados.items(), 'tipos_avalicao': sorted(tipos_avaliacao.items())})
        else:
            return render(request, 'registration/login.html')

    def post(self, request):
        if request.user.is_authenticated:
            if "form1" in request.POST:
                instance = get_object_or_404(Ideias, id=request.POST.get("id", ""))
                form = self.form_class(request.POST, instance=instance)
                if form.is_valid():
                    commit = form.save(commit=False)
                    commit.autor_pre_analise = request.user
                    commit.data_pre_analise = timezone.now()
                    commit.save()
                    return HttpResponseRedirect('/sgidi/ideias/avaliacao/' + request.POST.get("id", ""))
                else:
                    return render(request, 'ideias_avaliacao.html', {'form': form})

            elif "form2" in request.POST:
                ideia_id = request.POST.get("id", "")
                instance = get_object_or_404(Ideias, id=ideia_id)
                form = self.second_form_class(request.POST, instance=instance)

                if form.is_valid():
                    commit = form.save(commit=False)
                    commit.autor_analise = request.user
                    commit.data_analise = timezone.now()
                    commit.save()
                    avaliacoes = {}
                    for key, value in request.POST.items():
                        if key.startswith('avaliacao'):
                            avaliacoes.setdefault(key[-1:], [])
                            avaliacoes[key[-1:]].append(value)
                        if key.startswith('tipo'):
                            avaliacoes[key[-1:]].append(value)
                        if key.startswith('peso'):
                            avaliacoes[key[-1:]].append(value)
                    for key, value in avaliacoes.items():
                        Analises.objects.update_or_create(ideia_id=ideia_id, ordem=key,
                                                          defaults={"tipo": value[1], "peso": value[2],
                                                          "avaliacao": None if value[0] == 'default' else value[0]})
                    return HttpResponseRedirect('/sgidi/ideias/avaliacao/' + ideia_id)
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


class IdeiasListView(ListView):
    template_name = "ideias.html"
    model = Ideias
    allow_empty = True
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """add range template context variable that we can loop through pages"""
        context = super(IdeiasListView, self).get_context_data(**kwargs)
        context['range'] = range(context["paginator"].num_pages)
        return context
