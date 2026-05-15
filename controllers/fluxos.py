from utils import *
from models import Transacao
from services import Financeiro

def fluxo_cadastro (financeiro:Financeiro) -> None:
    limpar_tela()
    titulo_categoria, enfeite, tamanho = "CATEGORIAS", "=", 50
    printar_cabecalho(titulo_categoria,enfeite,tamanho)
    enfeite2, tamanho2 = "-",50
    pritar_opcoes_categorias()
    printar_cabecalho_solto(mesage=None, enfeite=enfeite2, quantidade=tamanho2)
    t = capturar_transacao()
    financeiro.adicionar_transacao(t) 
    printar_ação_validada()
    financeiro.salvar_arquivo()
    inputar_retornar()

def fluxo_imprimir_relatorio (financeiro:Financeiro) -> None:
    tamanho_str_transacao = 114
    titulo_relatorio, enfeite = "RELATÓRIO IMPRESSO","="
    printar_cabecalho(titulo_relatorio,enfeite,tamanho_str_transacao)
    lista_para_imprimir = financeiro.lista_transacao
    printar_lista(lista_para_imprimir)
    inputar_retornar()

def fluxo_filtro (financeiro:Financeiro) -> None:
    tamanho_str_transacao = 114
    filtro_opcao = inputar_opcao_id()
    enfeite_padrao, tamanho_padrao = "=", 81
    instrucao_str = "INSTRUÇÕES"
    printar_cabecalho(instrucao_str,enfeite_padrao, tamanho_padrao)
    printar_instrucao_filtro()
    if filtro_opcao == 'S':
        ids_brutos = []
        multiplas_escolhas(inputar_id,ids_brutos)
        printar_cabecalho_solto(mesage=None, enfeite="-" ,quantidade=tamanho_str_transacao) 
        limpar_tela()                              
        transacoes_filtradas = financeiro.lista_filtro(ids_brutos)
        titulo_transacoes = "TRANSAÇÕES"
        printar_cabecalho(titulo_transacoes, enfeite_padrao, tamanho_str_transacao) 
        printar_lista(transacoes_filtradas)
    elif filtro_opcao == 'N':
        titulo_categoria = "CATEGORIAS"
        printar_cabecalho(titulo_categoria,enfeite_padrao,tamanho_padrao)
        pritar_opcoes_categorias()
        categorias_brutas = []
        multiplas_escolhas(inputar_categoria,categorias_brutas)                               
        printar_digita_data2
        data_input = inputar_data()
        printar_digita_data2 
        data_input_2 = inputar_data()                                
        transacoes_filtradas = financeiro.lista_filtro(filtro_id = None, filtro_cat=Categoria.validacao_categoria(categorias_brutas), filtro_dat_1=data_input,filtro_dat_2= data_input_2)
        limpar_tela()       
        titulo_transacoes = "TRANSAÇÕES"
        printar_cabecalho(titulo_transacoes, enfeite_padrao, tamanho_str_transacao)                       
        printar_lista(transacoes_filtradas)                                 
        total_categoria: list[tuple[Categoria,int]]= financeiro.total_categorias(transacoes_filtradas)
        printar_cabecalho_solto(mesage=None,enfeite="-", quantidade=tamanho_str_transacao)
        printar_valores_categorias(total_categoria) 
    inputar_retornar()

def fluxo_metricas (financeiro:Financeiro) -> None:
    total_categoria = financeiro.total_categorias(financeiro.lista_transacao) 
    if total_categoria:
        s, d, t = financeiro.metrica(total_categoria) 
        maior_s, maior_d = financeiro.max_valor_transacao(financeiro.lista_transacao)
        titulo_principal, enfeite, quantidade = "SAÚDE FINANCEIRA", "=", 92 
        printar_metrica(titulo_principal,enfeite,quantidade,s,d,t)
        printar_valores_categorias(total_categoria)
        despesastr, enfeite1,quantidade1 = "DESPESA", "-", 92
        saldostr, enfeite1,quantidade1 =  "SALDO", "-", 92
        printar_cabecalho_solto(saldostr,enfeite1,quantidade1)
        printar_max_transacao_saldo(maior_s)
        printar_cabecalho_solto(despesastr,enfeite1,quantidade1)
        printar_max_transacao_despesa(maior_d)
    else:
        print("Não há transações.")
    inputar_retornar()



def fluxo_remover_transacao (financeiro:Financeiro) -> None:
    printar_cancelamento()
    id_removed = inputar_id()
    confirmação = financeiro.remover_transacao(id_removed)
    if confirmação:
        financeiro.salvar_arquivo()
        printar_ação_validada()
    else:
        printar_id_inexistente(id_removed)
    inputar_retornar()


def fluxo_corrigir_transacao (financeiro:Financeiro) -> None:
    printar_cancelamento()
    corrigir_id = inputar_id()
    transacao : Transacao = financeiro.buscar_transacao(corrigir_id)
    if transacao:
        capturar_transacao(transacao)
        financeiro.salvar_arquivo()
        printar_ação_validada()
    else:
        printar_id_inexistente(corrigir_id)
    inputar_retornar()