from django import forms
from .models import Ideias

class IdeiasForm(forms.Form):
   class Meta:
       model = Ideias
       fields = ['nome','tipo','tipo_nome','problema','solucao']
       exclude = ['autor']

