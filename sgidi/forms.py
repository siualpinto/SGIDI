from django import forms
from .models import Ideias

class IdeiasForm(forms.ModelForm):
   class Meta:
       model = Ideias
       fields = ['nome','tipo','problema','solucao']
       exclude = ['autor','tipo_nome'] #permite introduzir campos que não estão no form
