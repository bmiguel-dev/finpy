from models.transacao import Transacao, Categoria
from datetime import datetime
import json
from utils import passar_json_pro_financeiro, passar_financeiro_pro_json
import sqlite3
from api import ResponseTransacoes, CriarTransacoes, CorrigirTransacoes
from database import conect_bd
class Financeiro:
   
    def __init__(self):
        self._lista_transacao:list[Transacao] = []
        

    
    @property
    def lista_transacao(self) -> list[Transacao]:
        return self._lista_transacao
    
    def gerador_id (self) -> int:
        if self._lista_transacao:
            maior_id : Transacao = max(self._lista_transacao, key=lambda t:t._id)
            return maior_id.id + 1 
        else:
            return 1

    
    def adict_transaction (self, entrada_dado : CriarTransacoes ):
        with conect_bd() as banco:
            cursor = banco.cursor()
            cursor.execute('''INSERT INTO transacoes (categoria_id, valor, descricao, data)
                            VALUES (:categoria_id,:valor,:descricao,:data) ''', entrada_dado.model_dump())
            banco.commit()
            
    def remove_transaction (self, id:int):
        with conect_bd() as banco:
            cursor = banco.cursor()
            cursor.execute('''DELETE FROM transacoes WHERE id = ?''', [id])
            banco.commit()

    def search_by_id (self,id:int) -> sqlite3.Row | None:
        with conect_bd() as banco:
            cursor = banco.cursor() 
            cursor.execute('''SELECT transacoes.* , categorias.nome FROM transacoes 
                            INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                            WHERE transacoes.id = ?
                            ''', [id])
            dado = cursor.fetchone()
            return dado
        
    def search_by_cat(self, categoria : int) -> list[sqlite3.Row]:
        with conect_bd() as banco:
            cursor = banco.cursor() 
            cursor.execute('''SELECT transacoes.* , categorias.nome FROM transacoes 
                            INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                            WHERE categoria_id = ?
                            ''', [categoria])
            dado = cursor.fetchall()
            return dado

    def search_by_date (self, data1, data2) ->  list[sqlite3.Row]:
        with conect_bd() as banco:
            cursor = banco.cursor() 
            cursor.execute('''SELECT transacoes.* , categorias.nome FROM transacoes 
                            INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                            WHERE transacoes.data BETWEEN ? AND ?
                            ''', (data1, data2))
            dado = cursor.fetchall()
            return dado

  
    

    
    
    def all_cat_values (self):
        with conect_bd() as banco:
            cursor = banco.cursor() 
            cursor.execute('''SELECT SUM(transacoes.valor) AS total_valores, categorias.nome AS nome_categoria
                              FROM transacoes JOIN categorias ON transacoes.categoria_id = categorias.id
                              GROUP BY categorias.nome''')
            dados = cursor.fetchall()
            return dados
    
    
    
    def metrica (self, total_categorias_: dict) -> tuple[float,float,float]:
        lista_totais = total_categorias_
        saldo = sum(valor for cat,valor in lista_totais if valor > 0 )
        despesa = sum(valor for cat,valor in lista_totais if valor <= 0 )
        total = saldo + despesa

        return saldo, despesa, total
    
    def max_valor_categoria (self, total_categorias_: dict) -> tuple[Categoria | None ,Categoria | None ,float | None ]:
        lista_totais = total_categorias_      
        maior_saldo = max((i for i in lista_totais if i[1] > 0),key=lambda v:v[1], default=None) 
        maior_despesa = min((i for i in lista_totais if i[1] < 0),key=lambda v:v[1], default=None)
        total = maior_saldo[1] + maior_despesa[1]
        return maior_saldo, maior_despesa, total
    
    def max_valor_transacao (self, lista_total_categoria:list[Transacao] ) -> tuple [Transacao  | None ,Transacao | None ]:
        maior_saldo = max((i for i in lista_total_categoria if i.valor > 0),key=lambda i:i.valor, default=None) 
        maior_despesa = min((i for i in lista_total_categoria if i.valor < 0),key=lambda i:i.valor, default=None)
        return maior_saldo, maior_despesa
    
    def buscar_transacao (self,input_id) -> Transacao  | None :
        return next((t for t in self._lista_transacao if input_id == t.id), None)
    
    def salvar_arquivo (self) -> None:
        transacao_json = passar_financeiro_pro_json(self._lista_transacao)
        with open("transacoes.json", "w",encoding='utf-8') as arquivo:
            json.dump(transacao_json,arquivo, indent=4, ensure_ascii=False)

    def carregar_arquivo (self) -> None:
        try:
            with open("transacoes.json", "r", encoding='utf-8') as arquivo:
                transacoes = json.load(arquivo)

            self._lista_transacao = passar_json_pro_financeiro(transacoes)       
        except (FileNotFoundError,json.JSONDecodeError):
            self._lista_transacao = []



     

    