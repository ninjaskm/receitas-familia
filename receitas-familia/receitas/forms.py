from django import forms
from .models import Receita, GrupoFamiliar, Avaliacao, ReceitaPublica, AvaliacaoPublica

INPUT_CLASS = 'form-control'
TEXTAREA_CLASS = 'form-control'
CHECK_CLASS = 'form-check-input'


class GrupoForm(forms.ModelForm):
    class Meta:
        model = GrupoFamiliar
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Ex: Família Silva'}),
            'descricao': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 3, 'placeholder': 'Descreva o grupo...'}),
        }


class ReceitaForm(forms.ModelForm):
    class Meta:
        model = Receita
        fields = ['titulo', 'ingredientes', 'modo_preparo', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Nome da receita'}),
            'ingredientes': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 5, 'placeholder': 'Liste os ingredientes...'}),
            'modo_preparo': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 6, 'placeholder': 'Passo a passo do preparo...'}),
            'imagem': forms.FileInput(attrs={'class': INPUT_CLASS}),
        }


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['estrelas', 'comentario']
        widgets = {
            'estrelas': forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': 1, 'max': 5, 'placeholder': '1 a 5'}),
            'comentario': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4, 'placeholder': 'Comentário opcional...'}),
        }


class ReceitaPublicaForm(forms.ModelForm):
    class Meta:
        model = ReceitaPublica
        fields = ['titulo', 'ingredientes', 'modo_preparo', 'imagem', 'privada']
        labels = {
            'privada': 'Receita privada (só você verá)',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Nome da receita'}),
            'ingredientes': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 5, 'placeholder': 'Liste os ingredientes...'}),
            'modo_preparo': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 6, 'placeholder': 'Passo a passo do preparo...'}),
            'imagem': forms.FileInput(attrs={'class': INPUT_CLASS}),
            'privada': forms.CheckboxInput(attrs={'class': CHECK_CLASS}),
        }


class AvaliacaoPublicaForm(forms.ModelForm):
    class Meta:
        model = AvaliacaoPublica
        fields = ['estrelas', 'comentario']
        widgets = {
            'estrelas': forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': 1, 'max': 5, 'placeholder': '1 a 5'}),
            'comentario': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4, 'placeholder': 'Comentário opcional...'}),
        }
