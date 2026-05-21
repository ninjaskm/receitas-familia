from django import forms
from .models import Receita, GrupoFamiliar, Avaliacao
from .models import Receita, GrupoFamiliar, Avaliacao, ReceitaPublica, AvaliacaoPublica

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

class ReceitaPublicaForm(forms.ModelForm):
    class Meta:
        model = ReceitaPublica
        fields = ['titulo', 'ingredientes', 'modo_preparo', 'imagem', 'privada']
        labels = {
            'privada': 'Receita privada (só você verá)'
        }
        
class AvaliacaoPublicaForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoPublica
        fields = ['estrelas', 'comentario']