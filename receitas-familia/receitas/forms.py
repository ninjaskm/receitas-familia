from django import forms
from .models import Receita, GrupoFamiliar, Avaliacao

class GrupoForm(forms.ModelForm):
    class Meta:
        model = GrupoFamiliar
        fields = ['nome', 'descricao']

class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['titulo', 'ingredientes', 'modo_preparo', 'imagem']

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['estrelas', 'comentario']