from django.db import models

# Create your models here.


class Produto(models.Model):
    importado = models.BooleanField(default=False)
    ncm= models.CharField('NCM',max_length=10)
    produto = models.CharField('Produto',max_length=100, unique=True)
    preco= models.DecimalField('preço',decimal_places=2,max_digits=10)
    estoque= models.IntegerField('estoque atual',)
    estoque_minimo= models.PositiveIntegerField('estoque minimo',default=0)

    class Meta:
        ordering = ('produto',)

    def __str__(self):
        return self.produto