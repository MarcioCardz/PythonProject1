from django.db import models
from django.urls import reverse_lazy


# Create your models here.


class Produto(models.Model):
    importado = models.BooleanField(default=False)
    ncm= models.CharField('NCM',max_length=10)
    produto = models.CharField('Produto',max_length=100, unique=True)
    preco= models.DecimalField('preço',decimal_places=2,max_digits=10)
    estoque= models.IntegerField('estoque atual',)
    estoque_minimo= models.PositiveIntegerField('estoque minimo',default=0)
    categoria= models.ForeignKey('Categoria',on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ('produto',)

    def __str__(self):
        return self.produto

    def get_absolute_url(self):
        return reverse_lazy('produto:produto_detail', kwargs={'pk': self.pk})

    def to_dict_json(self):
        return {
            'pk': self.pk,
            'produto': self.produto,
            'estoque': self.estoque,
        }

class Categoria(models.Model):
    categoria = models.CharField('Categoria',max_length=100, unique=True)
    class Meta:
        ordering = ('categoria',)
    def __str__(self):
        return self.categoria