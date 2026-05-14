from utils import limpar_tela,printar_cabecalho,printar_menu_finpy,  inputar_fazer_escolha
from services import Financeiro
from controllers import *

def main():
     financeiro = Financeiro()
     while True:
          limpar_tela()
          titulo_finpy, enfeite, tamanho  = "FINPY SISTEMA V-01", "=", 30
          printar_cabecalho(titulo_finpy,enfeite,tamanho)
          printar_menu_finpy()
          opcao = inputar_fazer_escolha()
          if opcao == '1':
               fluxo_cadastro(financeiro)
          elif opcao == '2':
               fluxo_imprimir_relatorio(financeiro)
          elif opcao == '3':
               fluxo_filtro(financeiro)
          elif opcao == '4':
               fluxo_metricas(financeiro)
          elif opcao == '5':
               fluxo_remover_transacao(financeiro)
          elif opcao == '6': 
               fluxo_corrigir_transacao(financeiro)
          elif opcao == '0':
               break 

if __name__ == "__main__":
     main()