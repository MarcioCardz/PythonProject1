import csv
import io
from datetime import datetime
from re import search
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView
from produto.actions.import_xlsx import import_xlsx as action_import_xlsx
from produto.actions.export_xlsx import export_xlsx
from .forms import ProdutoForm
from .models import Produto


# Create your views here.

def produto_list(request):
    template_name='produto_list.html'
    objects = Produto.objects.all()
    search= request.GET.get('search')
    if search:
        objects = objects.filter(produto__icontains=search)
    context = {'object_list':objects }
    return render(request, template_name, context)

class ProdutoList(ListView):
    model = Produto
    template_name = 'produto_list.html'
    paginate_by = 10

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

def save_data(data):
    '''
    Salva os dados no banco.
    '''
    aux = []
    for item in data:
        produto = item.get('produto')
        ncm = str(item.get('ncm'))
        importado = True if item.get('importado') == 'True' else False
        preco = item.get('preco')
        estoque = item.get('estoque')
        estoque_minimo = item.get('estoque_minimo')
        obj = Produto(
            produto=produto,
            ncm=ncm,
            importado=importado,
            preco=preco,
            estoque=estoque,
            estoque_minimo=estoque_minimo,
        )
        aux.append(obj)
    Produto.objects.bulk_create(aux)

def import_csv(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        file= myfile.read().decode('utf8')
        reader = csv.DictReader(io.StringIO(file))
        data= [line for line in reader]
        save_data(data)
        return HttpResponseRedirect(reverse('produto:produto_list'))

    template_name = 'produto_import.html'
    return render(request, template_name)

def export_csv(request):
    header= ('importado', 'ncm' , 'produto', 'preco', 'estoque', 'estoque_minimo',)
    produtos = Produto.objects.all().values_list(*header)
    with open('fix/produtos_exportados.csv', 'w') as csvfile:
        produtos_writer = csv.writer(csvfile)
        produtos_writer.writerow(header)
        for produto in produtos:
            produtos_writer.writerow(produto)
    messages.success(request, 'Produtos exportados com sucesso!')
    return HttpResponseRedirect(reverse('produto:produto_list'))

def import_xlsx(request):
    filename= 'fix/produtos.xlsx'
    action_import_xlsx(filename)
    messages.success(request, 'Produtos importados com sucesso!')
    return HttpResponseRedirect(reverse('produto:produto_list'))

def exportar_produtos_xlsx(request):
    MDATA = datetime.now().strftime('%Y-%m-%d')
    model = 'Produto'
    filename = 'produtos_exportados.xlsx'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{MDATA}.{_filename[1]}'
    queryset = Produto.objects.all().values_list(
        'importado',
        'ncm',
        'produto',
        'preco',
        'estoque',
        'estoque_minimo',
        'categoria__categoria',
    )
    columns = ('Importado', 'NCM', 'Produto', 'Preço',
               'Estoque', 'Estoque mínimo', 'Categoria')
    response = export_xlsx(model, filename_final, queryset, columns)
    return response