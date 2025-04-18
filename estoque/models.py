from django.db import models
from django.contrib.auth.models import User

from core.models import TimeStampedModel
from .managers import EstoqueEntradaManager, EstoqueSaidaManager
from produto.models import Produto

# Create your models here.


MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)


class Estoque(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    nf = models.PositiveIntegerField('nota fiscal', null=True, blank=True)
    movimento = models.CharField(max_length=1, choices=MOVIMENTO)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.nf, self.created_at.strftime('%d/%m/%Y'))



    def nf_formated(self):
        return str(self.nf).zfill(6)



class EstoqueEntrada(Estoque):
    objects = EstoqueEntradaManager()

    class Meta:
        proxy = True
        verbose_name = 'estoque entrada'
        verbose_name_plural = 'estoque entrada'


class EstoqueSaida(Estoque):
    objects = EstoqueSaidaManager()
    class Meta:
        proxy = True
        verbose_name = 'estoque saida'
        verbose_name_plural = 'estoque saida'


class EstoqueItens(models.Model):
    estoque = models.ForeignKey(
        Estoque,
        on_delete=models.CASCADE,
        related_name='estoques'
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField(blank=True)

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{} - {} - {}'.format(self.pk, self.estoque.pk, self.produto)



