import json
import os
from datetime import datetime,timedelta

#ESCOLHER_DATA
def escolher_data () -> tuple: 
     while True:
          opcao_data = input("A transação foi realizada hoje?(S/N)").upper().strip()
          if opcao_data == 'S':
               return datetime.now().date().isoformat()
          if opcao_data == "N":
               try:
                    input_data = input("Insira a data da transação(DD/MM/YYYY):")
                    return datetime.strptime(input_data, "%d/%m/%Y" ).date().isoformat()
               except ValueError:
                    print("Coloque a data no padrão correto (DD/MM/YYYY)")
                    loop_return()
                    continue
          print("Insira apenas S para SIM ou N para NÃO.")

#Gerador de ID
def gerador_id (lista_transacao:list[dict]) -> int:
     if len(lista_transacao) > 0:       
          maior_id = max(lista_transacao,key=lambda t:t['id']) 
          return maior_id['id'] + 1

     else:
          return 1
     
#salvar dados ()

def salvar_dados(lista_transacao:list[dict]) -> None:
     try:  
          with open("transacoes.json", "w", encoding="utf-8") as arquivo:
               json.dump(lista_transacao, arquivo, indent=4, ensure_ascii= False)    
     except Exception as e:  
          print(f"Erro:{e} ao salvar o arquivo.")       

#transacoes_load()

def transacoes_load() -> list[dict]:
     try:
          with open("transacoes.json","r", encoding="utf-8" ) as t:
               transacoes = json.load(t)
     except (FileNotFoundError, json.JSONDecodeError):
               transacoes = []
     return transacoes

#layout
def layout_opcoes () -> None:
     print('''      
              ==============================
                    FINPY SISTEMA V-01
              ==============================
               1 - CADASTRO DA TRANSAÇÃO
               2 - RELATORIO IMPRESSO
               3 - FILTRO POR CATEGORIA
               4 - VER MÉTRICAS DE SAÚDE 
               5 - RETIRAR TRANSAÇÃO 
               6 - CORRIGIR TRANSAÇÃO
               0 - SAIR DO SISTEMA
               ''')
     
def loop_return() -> None:
     input("Aperte ENTER para retornar:")

#Opção 1
def layout_cadastro () -> None:
     print(''' 
     ==============================
               CATEGORIAS
     ==============================
         GANHOS
         1- RECEITAS
         2- DESENVOLVIMENTO
         3- CONSULTORIA
         4- MANUTENÇÃO
         DESPESA
         5- INFRAESTRUTURA''')

def cadastro_valor (categoria:str) -> float:
     while True:
          try:
               if categoria == "INFRAESTRUTURA":
                    valor = float(input("Insira o valor:")) * -1
               else:
                    valor = float(input("Insira o valor:"))
          except ValueError:
               print("Insira apenas números")
          except Exception as e:
               print(f"Erro {e} ao cadastrar categoria.")
          else:
               return valor

def obter_categoria () -> str:
     while True:
          os.system('cls')
          layout_cadastro()
          try:
               categoria_numero = int(input("DIGITE O NÚMERO DA CATEGORIA:"))
               if categoria_numero == 1:
                    return 'RECEITAS' 
               elif categoria_numero == 2:
                    return 'DESENVOLVIMENTO'
               elif categoria_numero == 3:
                    return 'CONSULTORIA'
               elif categoria_numero == 4:
                    return 'MANUTENÇÃO'
               elif categoria_numero == 5:
                    return 'INFRAESTRUTURA'
               else:
                    print("ERRO: Digite o número de uma categoria válida!")
                    loop_return()
          except ValueError:
               print("ERRO: Digite apenas números")
          except Exception as e:
               print(f"Erro {e} ao cadastrar categoria.")
               loop_return()
                                  


def cadastro_transacao (lista_transacao:list[dict]) -> None:
     categoria = obter_categoria()
     descricao = input("Insira a descrição:").upper().strip()
     data = escolher_data()
     id = gerador_id(lista_transacao)
     valor = cadastro_valor(categoria)
     lista_transacao.append({'id': id, 'categoria' : categoria, 'descricao' : descricao, 'valor': valor, 'data': data })



#Opção 2

def layout_relatorio () -> None: 
     os.system('cls')
     print('''
                ==============================
                      RELATÓRIO IMPRESSO
                ==============================
                ''')


def relatorio_impresso (lista_transacao:list[dict]) -> None:
          if len(lista_transacao) > 0:
               for t in lista_transacao:
                    print(f"ID: {t['id']} | Categoria: {t['categoria']} | Descrição: {t['descricao']} | Valor: {t['valor']} | Data da Transação: {t['data']} ")
          else:
               print("ERRO: Não há transações")
               
          


#Opção 3 FILTRO
def teste(funcao):
     return funcao

def layout_filtro_cat () -> None:
     print(''' 
     ==============================
               CATEGORIAS
     ==============================
     ------------GANHOS------------
         1- RECEITAS
         2- DESENVOLVIMENTO
         3- CONSULTORIA
         4- MANUTENÇÃO
     ------------DESPESA-----------
         5 - INFRAESTRUTURA
         6 - TODAS CATEGORIAS
     ------------------------------
     9 - PARA PROSSEGUIR''')
def filtro_cat () -> set:
     categorias_escolhidas = set()
     while True:
          try:
               os.system('cls')
               layout_filtro_cat()
               categoria_input = int(input("Digite o n° das categorias que deseja filtrar:"))
               if categoria_input == 1:
                    categorias_escolhidas.add('RECEITAS') 
               elif categoria_input == 2:
                    categorias_escolhidas.add('DESENVOLVIMENTO') 
               elif categoria_input == 3:
                    categorias_escolhidas.add('CONSULTORIA') 
               elif categoria_input == 4:
                    categorias_escolhidas.add('MANUTENÇÃO') 
               elif categoria_input == 5:
                    categorias_escolhidas.add('INFRAESTRUTURA') 
               elif categoria_input == 6:
                    categorias_escolhidas.add('TODAS')
                    return categorias_escolhidas
               elif categoria_input == 9:
                    if len(categorias_escolhidas) > 0:
                         return categorias_escolhidas
                    else:
                         print("Você não escolheu nenhuma categoria, escolha uma para prosseguir.")
                         loop_return()
                         continue
          except ValueError:
               print("ERRO: Digite apenas números!")
               loop_return()
               continue
def filtro_data () -> set | str:
     datas = set()
     while True:
          os.system('cls')
          try:
               decisao_data = input('''
     ==========================
     Qual data deseja filtrar?
     ==========================
     1 - Um dia Específico
     2 - Ultima Semana
     3 - Ultimo Mês
     4 - Todas transações
     ==========================
     Digite o número da sua opção
     ->''')
               hoje = datetime.now().date()
               if decisao_data == '1':
                    data_especifica = escolher_data()
                    datas.add(data_especifica)
                    return datas
               elif decisao_data == '2':
                    for d in range(7):
                         dia_calculado = hoje - timedelta(days=d)
                         datas.add(dia_calculado.isoformat())
                    return datas
               elif decisao_data == '3':
                    for d in range(30):
                         dia_calculado = hoje - timedelta(days=d)
                         datas.add(dia_calculado.isoformat())
                    return datas
               elif decisao_data == '4':
                    return 'TODAS DATAS'
          except Exception as e:
               print(f'{e}')


def filtro_transacoes (lista_transacao):
     filtro_categoria = filtro_cat()
     filtro_dat = filtro_data()
     transacoes_filtradas = [t for t in lista_transacao if (t['categoria'] in filtro_categoria or 'TODAS' in filtro_categoria ) and (t['data'] in filtro_dat or 'TODAS DATAS' in filtro_dat) ]
     try:
          return  transacoes_filtradas
          
     except Exception as e:
          print(e)
          loop_return()

     
def filtro_action (filtro:list) -> None:
     os.system('cls')
     print("=" * 111)
     for f in filtro:
           print(f"ID: {f['id']} | Categoria: {f['categoria']:<14} | Descrição: {f['descricao']:<25} | Valor: {f['valor']:>10.2f} | Data: {f['data']} ")
     print("=" * 111)
     
          

def calculo_total (filtro:list) -> list[dict]:
     lista = {'RECEITAS':0.0,
              'MANUTENÇÃO': 0.0,
              'CONSULTORIA': 0.0,
              'DESENVOLVIMENTO': 0.0,
              'INFRAESTRUTURA' : 0.0 }
     for f in filtro:
          categoria = f['categoria']
          if categoria in lista:
               lista[categoria] += float(f['valor'])
     return [{cat:val} for cat, val in lista.items()]
    
     
def print_totais (calculo_total:list[dict]) -> None:
     for t in calculo_total:
          for cat, val in t.items():
               if cat != 'INFRAESTRUTURA':
                    print(f"A RECEITA TOTAL DA CATEGORIA {cat:<20} É DE R${val:>10.2f}".replace('.',','))
                    

               else:
                    print(f"A DESPESA TOTAL DA CATEGORIA {cat:<20} É DE R${val:>10.2f}".replace('.',','))
     
def categoria_receita_max(filtro_transacoes:list[dict]) -> None:
     nova_lista = [t for t in filtro_transacoes if list(t.values())[0] > 0]
     máxima_receita = max(nova_lista, key=lambda t:list(t.values())[0])
     categoria = list(máxima_receita.keys())[0]
     valor = list(máxima_receita.values())[0]
     largura_cat  = len(categoria) + 1 
     largura_valor = len(str(valor)) + 1
     print("=" * 75 )
     print(f"A CATEGORIA COM A MAIOR RECEITA É {categoria:<{largura_cat}} COM O VALOR TOTAL DE R${valor:>{largura_valor}.2f} ".replace('.' , ','))
     

#Opção 4


def receitas (lista_transacao:list[dict]) -> tuple[float,float,float]:
               saldo_total = sum(t['valor'] for t in lista_transacao if t['valor'] > 0)
               despesa__total = sum(t['valor'] for t in lista_transacao if t['valor'] < 0)
               total = saldo_total + despesa__total
               return saldo_total, abs(despesa__total), total 

def metrica (s:float , d:float, t:float) -> None:
     try:
          porcentagem_despesa = d * 100 / s
          margem_liquida = 100 - porcentagem_despesa
     
          print(f'''
                                       ==============================
                                              SAÚDE FINANCEIRA 
                                       ==============================
                Saldo Total: R${s} | Despesa Total: R${d} | Total Líquido: R${t}
               -----------------------------------------------------------------------
              ''')
     
          if d <= s * 80 / 100:
               print("Está tudo dentro dos conformes!")
          else:
               print("Sua margem está apertada!")
          print(f"Sua margem líquida é de:{margem_liquida}% ")
     except ZeroDivisionError:
          loop_return()

#Opcao 5

def remover_transacao(lista_transacao:list[dict]) -> None:
     try:
          id_existentes = [t['id'] for t in lista_transacao]
          id_removido = int(input("ID que você deseja remover:"))
          if id_removido in id_existentes:
               lista_transacao[:] = [t for t in lista_transacao if t['id'] != id_removido]
          else:
               print("ERRO: ID inválido!")
     except ValueError:
          print("Digite apenas Números!")
     except Exception as e:
          print(f'Deu erro "{e}" ao tentar remover transação')

#Opção 6
def correcao_transacao(lista_transacao:list[dict]) -> None:
     while True:
          try:
               os.system('cls')
               opcao_trasacao = int(input("Qual o ID da transação que você deseja modificar?(APENAS NÚMEROS)"))
               t = next((t for t in lista_transacao if t['id'] == opcao_trasacao), None)
               if t:
                    corrigir_erro = input('''
     O que você deseja corrigir na transação(DIGITE APENAS O NÚMERO)?
     ----------------
     1 - CATEGORIA
     2 - DESCRIÇÃO
     3 - VALOR
     4 - DATA 
     ---------------
     =''')
                    if corrigir_erro == '1':
                         t['categoria'] = obter_categoria()
                         if t ['categoria'] == 'INFRAESTRUTURA':
                              t['valor'] = abs(t['valor']) * -1 
                         else:
                              t['valor'] = abs(t['valor'])


                    elif corrigir_erro == '2':
                         t['descricao'] = input("Insira a descrição:").upper().strip()
                    
                    elif corrigir_erro == '3':
                         t['valor'] = cadastro_valor(t['categoria'])
                    elif corrigir_erro == '4':
                         t['data'] = escolher_data()
                    print("Modificação realizada com sucesso!")
                    loop_return()
                    return
               else:
                    decisao = input("ID inserido inválido deseja modificar outro ID?(S/N)").upper().strip()
                    if decisao == 'S':
                         continue
                    elif decisao == 'N':
                         return
          
                         
          except ValueError:
               print(" Digite apenas números!")
               loop_return()
               continue
          except Exception as e:
               print("ERRO:{e}")
               loop_return()
               continue
          



transacoes = transacoes_load() 
while True:
     os.system('cls')
     layout_opcoes()
     opcao = input( "Qual ação você deseja escolher?")
     if opcao == '1':
          os.system('cls')

          cadastro_transacao(transacoes)
          salvar_dados(transacoes)
     elif opcao == '2':
          layout_relatorio()
          relatorio_impresso(transacoes)
          loop_return()
     elif opcao == '3':
          transacoes_filtradas = filtro_transacoes(transacoes)
          filtro_action(transacoes_filtradas)
          calculo_tot = calculo_total(transacoes_filtradas)
          print_totais(calculo_tot)
          categoria_receita_max(calculo_tot)
          loop_return()
     elif opcao == '4':
          s, d, t = receitas(transacoes)
          metrica(s, d, t)
          loop_return()
     elif opcao == '5':
          remover_transacao(transacoes)
          salvar_dados(transacoes)
     elif opcao == '6': 
          correcao_transacao(transacoes)
          salvar_dados(transacoes)
     elif opcao == '9':
         transacoes_filtradas = filtro_transacoes(transacoes)
         calculo_tot = calculo_total(transacoes_filtradas)
         categoria_receita_max(calculo_tot)

         loop_return()
     elif opcao == '0':
          break