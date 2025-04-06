from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from core.models import TimeStampedModel
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

    def get_absolute_url(self):
        return reverse_lazy('estoque:estoque_entrada_detail', kwargs={'pk': self.pk})

    def nf_formated(self):
        return str(self.nf).zfill(6)


class EstoqueItens(models.Model):
    estoque = models.ForeignKey(Estoque, on_delete=models.CASCADE, related_name='estoques')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    saldo = models.PositiveIntegerField()

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return '{}{}{}'.format(self.estoque, self.produto, self.quantidade)



