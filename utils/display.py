from datetime import datetime, date
from models import Transacao
from enums import Categoria
import os 
from typing import Callable,Optional

def limpar_tela () -> int:
    return os.system( 'cls' if os.name == 'nt' else 'clear')

#CAPTURAS
def multiplas_escolhas (input_funcao: Callable, lista_escolhas : list ) -> list:
     while True:    
          escolhas_input = input_funcao()      
          if escolhas_input is None:
               return lista_escolhas
          lista_escolhas.append(escolhas_input)

def capturar_transacao (t:Optional[Transacao] = None) -> "Transacao":
     if t is None:
          t = Transacao()
     while True:
          try:
               t.categoria = inputar_categoria()
               if t.categoria:
                    break 
               else:
                    print("Categoria não esta sendo atribuída")
          except ValueError as e:
               print(f"Erro na data: {e}")
          except TypeError as e:
               print(f"Erro de tipo: {e}")

     while True:
          try:
               t.data = inputar_data()
               break 
          except ValueError as e:
               print(f"Erro na data: {e}")
          except TypeError as e:
               print(f"Erro de tipo: {e}")

     while True:
          try:
               t.valor = inputar_valor()
               break 
          except ValueError as e:
               print(f"Erro na data: {e}")
          except TypeError as e:
               print(f"Erro de tipo: {e}")
     while True:
          try:
               t.descricao = inputar_descricao()
               break 
          except ValueError as e:
               print(f"Erro na data: {e}")
          except TypeError as e:
               print(f"Erro de tipo: {e}")
     return t

          

               

          
# PRINTS


def printar_lista (lista_para_printar:list) -> None:
     if lista_para_printar:        
          for item in lista_para_printar:
               print(item)
     else:
          print("Não há itens dessa característica para ser impresso.")

def printar_max_transacao_saldo (maior_saldo:Transacao) -> None:
     if maior_saldo:
               print(f"Categoria da transação com maior valor foi {maior_saldo.categoria.name:<18} com um valor de R${maior_saldo.valor:>10.2f} ")
     elif maior_saldo is None:
          print("Não há transações com saldo positivo.")

def printar_max_transacao_despesa (maior_despesa:Transacao) -> None:
     if maior_despesa:
          print(f"Categoria da transação com maior valor foi {maior_despesa.categoria.name:<18} com um valor de R${maior_despesa.valor:>10.2f} ")
     elif maior_despesa is None:
          print("Não há transações com saldo negativo.")

def printar_id_inexistente (id:int) -> None:
     print(f"Este ID:{id} não existe.")


def printar_metrica (titulo:str, enfeite:str, quantidade:int, saldo:float, despesa:float, total:float) -> None:
     print(f"{titulo:=^{quantidade}}")
     print(f"SALDO TOTAL: R${saldo:>10.2f} | DESPESA TOTAL: R${despesa:>10.2f} | TOTAL LÍQUIDO: R${total:>10.2f}")
     print(enfeite * quantidade) 

def printar_valores_categorias (lista:list[tuple[Categoria,float]]) -> None:
     for categoria, valores in lista:
          print(f"A Categoria:{categoria.name:<18} gerou um valor acumulado de: R${valores:>10.2f}")

def printar_ação_validada () -> None:
     print('-' * 24)
     print("A ação foi bem sucedida!")

def printar_menu_finpy () -> None:
     print(''' 
1 - CADASTRO DA TRANSAÇÃO
2 - RELATORIO IMPRESSO
3 - FILTRAR TRANSAÇÃO
4 - VER MÉTRICAS DE SAÚDE 
5 - RETIRAR TRANSAÇÃO 
6 - CORRIGIR TRANSAÇÃO
0 - SAIR DO SISTEMA
               ''')
     
def pritar_opcoes_categorias () -> None:
     for cat in Categoria:
          print(f"{cat.value} - {cat.name}")

def printar_cancelamento() -> None:
     print("--------------------------------")
     print("|Você pode cancelar apertando 0|")
     print("--------------------------------")


def  printar_digite_data1 () -> None:
     print("Digite a primeira data.")

def printar_digita_data2 () -> None:
     print("Digite a segunda data")
     
def printar_instrucao_filtro() -> None:
     print('''
1-(FILTRO POR ID) CASO JÁ TENHA ESCOLHIDO OS ID'S DE-
SEJADOS, APENAS DÊ ENTER COM ESPAÇO VAZIO PARA AVANÇAR.
           
2- CASO NÃO DESEJA FILTRAR PELA OPÇÃO DADA APENAS DÊ
ENTER COM ESPAÇO VAZIO

3- NO FILTRO DE DATAS, A PRIMEIRA DATA SERÁ A DATA 
QUE O FILTRO INICIARÁ A BUSCA E A SEGUNDA DATA É ATÉ
AONDE O FILTRO IRÁ BUSCAR''')


def printar_cabecalho (mensage: str,enfeite:str,  quantidade:int) ->None:
     print(enfeite * quantidade)
     print(f"{mensage:^{quantidade}}")
     print(enfeite * quantidade)

def printar_cabecalho_solto(mesage:str=None, enfeite:str=None, quantidade:int=None) ->None:
     if mesage:
          print(f"{mesage:{enfeite}^{quantidade}}")
     else:
          print(enfeite * quantidade)
# INPUTS

def inputar_opcao_id () -> str :
     return input("Deseja filtrar apenas pelo ID?(S/N)").upper().strip()

def inputar_data () -> date | None: 
     while True:
          input_data = input("Insira a data(Obedeça o formato DD/MM/YYYY)\n->".strip())
          try:
               return datetime.strptime(input_data, "%d/%m/%Y" ).date() if input_data else None
          except:
               print("A data foi inserida no formato ERRADO | Exemplo formato certo: 31/12/2026")

def inputar_valor() -> float | None:
     while True:
          try:
               valor_escolhido = float(input("Insira o valor da transação (APENAS NÚMEROS)\n->").strip())
               return valor_escolhido if valor_escolhido else None
          except:
               print("Insira apenas números")

def inputar_id () -> int:
     while True:
          try:
               id_escolhido = input("Insira o ID escolhida (APENAS NÚMEROS)\n->").strip()
               return int(id_escolhido) if id_escolhido else None
          except Exception as e:
               print(f"Insira apenas números: {e}")

def inputar_categoria () ->int | None:
     while True:
          try:
               categoria_escolhida = input("Insira a Categoria escolhida (APENAS NÚMEROS)\n->").strip()
               return int(categoria_escolhida) if categoria_escolhida else None
          except:
               print("Insira apenas números")

def inputar_descricao () ->str:
     return input("Insira a descrição da transação\n->")


def inputar_retornar() -> str:
     return input("Aperte ENTER para retornar:")

def inputar_fazer_escolha () -> str:
     return input( "Qual ação você deseja escolher?\n->")