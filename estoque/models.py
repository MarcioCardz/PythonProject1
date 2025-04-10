from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from core.models import TimeStampedModel
from .managers import EstoqueEntradaManager, EstoqueSaidaManager
from produto.models import Produto

# Create your models here.


MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)


class Estoque(TimeStampedModel):
    funcionario = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def get_absolute_url(self):
        return reverse_lazy('estoque:estoque_entrada_detail', kwargs={'pk': self.pk})



class EstoqueSaida(Estoque):
    objects = EstoqueSaidaManager()
    class Meta:
        proxy = True
        verbose_name = 'estoque saida'
        verbose_name_plural = 'estoque saida'

    def get_absolute_url(self):
        return reverse_lazy('estoque:estoque_saida_detail', kwargs={'pk': self.pk})


class EstoqueItens(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='estoques')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField()

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{}{}{}'.format(self.estoque, self.produto, self.quantidade)



