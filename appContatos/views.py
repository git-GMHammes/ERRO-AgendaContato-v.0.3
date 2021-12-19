from django.shortcuts import render, get_object_or_404, redirect
# ↓ Importar o modulo ↓ DbTabContatos
from .models import DbTabContatos
# O . ↑ É um detalhe importante
# ↓ Importando o erro 404 ↓
from django.http import Http404, response
# ↓ Para fazer a paginação do django ↓↘
from django.core.paginator import Paginator
# Para select Or importar o Q ↙
from django.db.models import Q, Value
# Importar o Value para o espaço ↗ no Concat('campo', Value(' '), 'campo')
# Para utilizar campos com concatenação ↘
from django.db.models.functions import Concat
# Mensagens
# ↙ ----- ALERTAS SISTEMA ---- ↘
from django.contrib import messages

# Create your views here.

# Vou copiar e preservar esse método para ver como era antes
# def index(request):
#   Aqui não é ponto (.) é barra ( / )
#   -------------------------------- ↓ -----------------
#   return render(request, 'appContatos/contatoIndex.html')
# Pasta Templates past appContatos ↑   e     ↑ arquivo.html da past appContatos


# Este metodo foi copiado para ser alterado com um dicionário {}
def index(request):
    # ↙ ----- ALERTAS SISTEMA ---- ↘
    # messages.add_message(request, messages.ERROR, 'ERRO')
    # messages.add_message(request, messages.INFO, 'INFO')
    # messages.add_message(request, messages.SUCCESS, 'SUCESSO')
    # messages.add_message(request, messages.WARNING, 'ALERTA')
    #
    # Esta ↓ variável irá ser passada como chave do dicionário
    # varHtmlContatos = DbTabContatos.objects.all()
    # ↑ Vou preservar esta linha e criar outra com ordem e filtro abaixo
    # Mudei o Comando para orde_by e filter ↓
    varHtmlContatos = DbTabContatos.objects.order_by('-id').filter(
        bolExibir=True
    )
    # Utilizando o ↓ Paginator
    paginacao = Paginator(varHtmlContatos, 6)
    page = request.GET.get('p')
    varHtmlContatos = paginacao.get_page(page)
    return render(request, 'appContatos/contatoIndex.html', {
        # Aqui ↓ a chave do dicionário
        'passaHtmlContatos': varHtmlContatos,
        # Aqui  recebe a variável acima ↑
    })


# Aqui colocar a TAG HTML ↓ do path '<int:contato_id>'
def verContato(request, contato_id):
    # Esta ↓ variável irá ser passada como chave do dicionário
    # varHtmlContatoUnico = DbTabContatos.objects.get(id=contato_id)
    # ----------------------- Trocar all por get ↑ e utilizar ↖ o contato_id
    # Substituição para o tratamento ↓ do erro 404 ↓
    varHtmlContatoUnico = get_object_or_404(DbTabContatos, id=contato_id)
    # Não permitir que seja exibido o registro desabilitado
    if not varHtmlContatoUnico.bolExibir:
        raise Http404()
    # O que vc colocar no dicionário {var : var} será passado para o HTML
    return render(request, 'appContatos/verContato.html', {
        # ------------------ Criar o arquivo ↑ verContato.html
        # Aqui ↓ a chave do dicionário
        'passaHtmlContato': varHtmlContatoUnico
        # Aqui  recebe a variável acima ↑
    }
    )


def busca(request):
    # Cadeia de funções que recebe o termo
    # ----------- ↙ --------------- ↘
    recebeTermo = request.GET.get('termo')
    # ------------------ Este termo ↗ ...
    # ... veio do djTemplates\parciais\tempBusca.html
    if recebeTermo is None or not recebeTermo:
        messages.add_message(request, messages.WARNING,
                             'ALERTA: Você não deve realizar uma busca em branco'
                             )
        return redirect('index')
    campos = Concat(
        'strNome',
        Value(' '),
        'strSobreNome',
        Value(' '),
        'strTelefone'
    )
    varHtmlContatos = DbTabContatos.objects.annotate(
        strNomeCompleto=campos
    ).filter(
        Q(strNomeCompleto__icontains=recebeTermo) | Q(
            strEmail__icontains=recebeTermo)
    )
    # Vou preservar este código que utiliza Or
    # varHtmlContatos = DbTabContatos.objects.order_by('-id').filter(
    #    Q(strNome__icontains=recebeTermo) | Q(strSobreNome__icontains=recebeTermo),
    #    bolExibir=True
    # )
    # → print(varHtmlContatos.query) - Atualizar a página...
    # ... apresenta a consulta SQL no terminal
    paginacao = Paginator(varHtmlContatos, 6)
    page = request.GET.get('p')
    varHtmlContatos = paginacao.get_page(page)
    return render(request, 'appContatos/contatoBusca.html', {
        'passaHtmlContatos': varHtmlContatos,
    })
