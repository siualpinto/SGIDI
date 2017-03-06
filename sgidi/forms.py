from django import forms
from .models import Ideias

class IdeiasForm(forms.ModelForm):
   class Meta:
       model = Ideias
       fields = ['nome', 'tipo', 'problema', 'solucao']
       exclude = ['autor', 'tipo_nome', 'estado', 'estado_nome'] #permite introduzir campos que não estão no form

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Ideias
        fields = ['pre_analise']
        exclude = ['autor_pre_analise']
