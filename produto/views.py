from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from .forms import ProdutoForm
from .models import Produto


# Create your views here.

def produto_list(request):
    template_name='produto_list.html'
    objects = Produto.objects.all()
    context = {'object_list':objects }
    return render(request, template_name, context)

def produto_detail(request,pk):
    template_name='produto_detail.html'
    obj = Produto.objects.get(pk=pk)
    context = {'object':obj }
    return render(request, template_name, context)

def produto_add(request):
    template_name='produto_form.html'
    return render(request, template_name,)

class ProdutoCreate(CreateView):
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm

class ProdutoUpdate(UpdateView):
    model = Produto
    template_name = 'produto_form.html'
    form_class = ProdutoForm

def produto_json(request, pk):
    ''' Retorna o produto json'''
    produto = Produto.objects.filter(pk=pk)
    data = [item.to_dict_json() for item in produto]
    return JsonResponse({'data':data})