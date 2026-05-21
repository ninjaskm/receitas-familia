from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import GrupoFamiliar, Receita, Avaliacao
from .forms import ReceitaForm, GrupoForm, AvaliacaoForm

def home(request):
    grupos = request.user.grupos.all()
    return render(request, 'home.html', {'grupos': grupos})

def registrar(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'auth/registrar.html', {'form': form})


def fazer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


@login_required
def fazer_logout(request):
    logout(request)
    return redirect('login')

@login_required
def criar_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.admin = request.user
            grupo.save()
            grupo.membros.add(request.user)
            return redirect('detalhe_grupo', pk=grupo.pk)
    else:
        form = GrupoForm()
    return render(request, 'grupos/criar_grupo.html', {'form': form})


@login_required
def adicionar_receita(request, grupo_pk):
    grupo = get_object_or_404(GrupoFamiliar, pk=grupo_pk)
    if request.user not in grupo.membros.all():
        messages.error(request, 'Você não é membro deste grupo.')
        return redirect('home')

    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES)
        if form.is_valid():
            receita = form.save(commit=False)
            receita.grupo = grupo
            receita.autor = request.user
            receita.save()
            return redirect('detalhe_receita', pk=receita.pk)
    else:
        form = ReceitaForm()
    return render(request, 'receitas/adicionar.html', {'form': form, 'grupo': grupo})


@login_required
def avaliar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            Avaliacao.objects.update_or_create(
                receita=receita,
                usuario=request.user,
                defaults=form.cleaned_data
            )
            return redirect('detalhe_receita', pk=pk)
    else:
        form = AvaliacaoForm()
    return render(request, 'receitas/avaliar.html', {'form': form, 'receita': receita})


@login_required
def favoritar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    if request.user in receita.favoritos.all():
        receita.favoritos.remove(request.user)
    else:
        receita.favoritos.add(request.user)
    return redirect('detalhe_receita', pk=pk)


@login_required
def sair_grupo(request, grupo_pk):
    grupo = get_object_or_404(GrupoFamiliar, pk=grupo_pk)

    if grupo.admin == request.user:
        outros_membros = grupo.membros.exclude(pk=request.user.pk)

        if not outros_membros.exists():
            messages.error(request, 'Você é o único membro do grupo. Delete o grupo para sair.')
            return redirect('detalhe_grupo', pk=grupo_pk)
        else:
            messages.info(request, 'Escolha um novo admin antes de sair.')
            return redirect('transferir_admin', pk=grupo_pk)

    grupo.membros.remove(request.user)
    messages.success(request, 'Você saiu do grupo.')
    return redirect('home')


@login_required
def transferir_admin(request, grupo_pk):
    grupo = get_object_or_404(GrupoFamiliar, pk=grupo_pk)

    if grupo.admin != request.user:
        return redirect('home')

    outros_membros = grupo.membros.exclude(pk=request.user.pk)

    if request.method == 'POST':
        novo_admin_id = request.POST.get('novo_admin')
        novo_admin = get_object_or_404(User, pk=novo_admin_id)
        grupo.admin = novo_admin
        grupo.save()
        grupo.membros.remove(request.user)
        messages.success(request, f'{novo_admin.username} agora é o admin do grupo.')
        return redirect('home')

    return render(request, 'grupos/transferir_admin.html', {
        'grupo': grupo,
        'membros': outros_membros
    })


@login_required
def remover_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)

    if receita.autor != request.user:
        messages.error(request, 'Você não tem permissão para remover esta receita.')
        return redirect('detalhe_receita', pk=pk)

    grupo_pk = receita.grupo.pk
    receita.delete()
    messages.success(request, 'Receita removida com sucesso.')
    return redirect('detalhe_grupo', pk=grupo_pk)


@login_required
def remover_avaliacao(request, pk):
    avaliacao = get_object_or_404(Avaliacao, pk=pk, usuario=request.user)
    receita_pk = avaliacao.receita.pk
    avaliacao.delete()
    messages.success(request, 'Avaliação removida com sucesso.')
    return redirect('detalhe_receita', pk=receita_pk)


@login_required
def detalhe_grupo(request, pk):
    grupo = get_object_or_404(GrupoFamiliar, pk=pk)

    if request.user not in grupo.membros.all():
        messages.error(request, 'Você não é membro deste grupo.')
        return redirect('home')

    receitas = grupo.receitas.all()
    return render(request, 'grupos/detalhe_grupo.html', {
        'grupo': grupo,
        'receitas': receitas
    })


@login_required
def detalhe_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)

    if request.user not in receita.grupo.membros.all():
        messages.error(request, 'Você não tem acesso a esta receita.')
        return redirect('home')

    avaliacoes = receita.avaliacoes.all()
    ja_avaliou = avaliacoes.filter(usuario=request.user).exists()
    ja_favoritou = request.user in receita.favoritos.all()

    return render(request, 'receitas/detalhe_receita.html', {
        'receita': receita,
        'avaliacoes': avaliacoes,
        'ja_avaliou': ja_avaliou,
        'ja_favoritou': ja_favoritou
    })


@login_required
def excluir_grupo(request, pk):
    grupo = get_object_or_404(GrupoFamiliar, pk=pk)

    # Só o admin pode excluir
    if grupo.admin != request.user:
        messages.error(request, 'Apenas o admin pode excluir o grupo.')
        return redirect('detalhe_grupo', pk=pk)

    grupo.delete()
    messages.success(request, 'Grupo excluído com sucesso.')
    return redirect('home')