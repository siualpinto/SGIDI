from django import forms

from .models import Ideias, Analises, Conhecimentos, Tags
from django.forms.models import inlineformset_factory

class IdeiasForm(forms.ModelForm):
   class Meta:
       model = Ideias
       fields = ['nome', 'tipo', 'problema', 'solucao']
       exclude = ['autor', 'tipo_nome', 'estado', 'estado_nome'] #permite introduzir campos que não estão no form


class PreAnaliseForm(forms.ModelForm):
    class Meta:
        model = Ideias
        fields = ['pre_analise']
        exclude = ['autor_pre_analise', 'data_pre_analise']


class AnaliseForm(forms.ModelForm):
    class Meta:
        model = Ideias
        fields = ['analise']
        exclude = ['autor_analise', 'data_analise']


class ConhecimentoForm(forms.ModelForm):
    class Meta:
        model = Conhecimentos
        fields = ['titulo', 'texto']
        exclude = ['autor']


# class TagForm(forms.ModelForm):
#     tag = forms.CharField(required=False)
#
#     class Meta:
#         model = Tag
#         fields = ['tag']
