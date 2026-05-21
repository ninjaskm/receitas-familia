from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.fazer_login, name='login'),
    path('logout/', views.fazer_logout, name='logout'),
    path('grupo/criar/', views.criar_grupo, name='criar_grupo'),
    path('grupo/<int:pk>/', views.detalhe_grupo, name='detalhe_grupo'),
    path('grupo/<int:grupo_pk>/sair/', views.sair_grupo, name='sair_grupo'),
    path('grupo/<int:pk>/excluir/', views.excluir_grupo, name='excluir_grupo'),
    path('grupo/<int:grupo_pk>/transferir-admin/', views.transferir_admin, name='transferir_admin'),
    path('grupo/<int:grupo_pk>/receita/adicionar/', views.adicionar_receita, name='adicionar_receita'),
    path('receita/<int:pk>/favoritar/', views.favoritar_receita, name='favoritar_receita'),
    path('receita/<int:pk>/remover/', views.remover_receita, name='remover_receita'),
    path('receita/<int:pk>/', views.detalhe_receita, name='detalhe_receita'),
    path('receita/<int:pk>/avaliar/', views.avaliar_receita, name='avaliar_receita'),
    path('avaliacao/<int:pk>/remover/', views.remover_avaliacao, name='remover_avaliacao'),
]