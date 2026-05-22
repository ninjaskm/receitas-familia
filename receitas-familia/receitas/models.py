from django.db import models
from django.contrib.auth.models import User

class GrupoFamiliar (models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField(blank=True)
    admin = models.ForeignKey(User, on_delete=models.PROTECT, related_name='grupos_admin')
    membros = models.ManyToManyField(User, related_name='grupos', blank=True)
    criado_em = models.DateField(auto_now_add=True)

    def __str__(self):
       return self.nome
    
class Receita(models.Model):
    titulo = models.CharField(max_length=50)
    ingredientes = models.TextField()
    modo_preparo = models.TextField()
    imagem = models.ImageField(upload_to='receitas/', blank=True, null=True)
    grupo = models.ForeignKey(GrupoFamiliar, on_delete=models.CASCADE, related_name='receitas')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    favoritos = models.ManyToManyField(User, related_name='favoritos', blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def media_avaliacao(self):
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            return round(sum(a.estrelas for a in avaliacoes) / avaliacoes.count(), 1)
        return None

    def __str__(self):
        return self.titulo

class Avaliacao(models.Model):
    receita = models.ForeignKey(Receita, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estrelas = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('receita', 'usuario')

    def __str__(self):
        return f"{self.usuario} - {self.receita} ({self.estrelas}★)"
    
class ReceitaPublica(models.Model):
    titulo = models.CharField(max_length=50)
    ingredientes = models.TextField()
    modo_preparo = models.TextField()
    imagem = models.ImageField(upload_to='receitas_publicas/', blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    favoritos = models.ManyToManyField(User, related_name='receitas_publicas_favoritas', blank=True)
    privada = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def media_avaliacao(self):
        avaliacoes = self.avaliacoes_publicas.all()
        if avaliacoes.exists():
            return round(sum(a.estrelas for a in avaliacoes) / avaliacoes.count(), 1)
        return None

    def __str__(self):
        return f"{self.titulo} - {self.autor.username}"





class AvaliacaoPublica(models.Model):
    receita = models.ForeignKey(ReceitaPublica, on_delete=models.CASCADE, related_name='avaliacoes_publicas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estrelas = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('receita', 'usuario')

    def __str__(self):
        return f"{self.usuario} - {self.receita} ({self.estrelas}★)"
    

class Convite(models.Model):
    grupo = models.ForeignKey(GrupoFamiliar, on_delete=models.CASCADE, related_name='convites')
    convidado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='convites_recebidos')
    convidado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='convites_enviados')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('grupo', 'convidado')

    def __str__(self):
        return f"{self.convidado_por} convidou {self.convidado} para {self.grupo}"