from django.contrib import admin
from .models import EstoqueEntrada, EstoqueSaida, EstoqueItens


# Register your models here.

class EstoqueItensInline(admin.TabularInline):
    model = EstoqueItens
    extra = 0

@admin.register(EstoqueEntrada)
class EstoqueEntradaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf', 'funcionario')
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created_at'

@admin.register(EstoqueSaida)
class EstoqueSaidaAdmin(admin.ModelAdmin):
    inlines = (EstoqueItensInline,)
    list_display = ('__str__', 'nf', 'funcionario')
    search_fields = ('nf',)
    list_filter = ('funcionario',)
    date_hierarchy = 'created_at'