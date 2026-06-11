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
        
    def search_by_cat(self, categoria : int) -> list[sqlite3.Row] | None:
        with conect_bd() as banco:
            cursor = banco.cursor() 
            cursor.execute('''SELECT transacoes.* , categorias.nome FROM transacoes 
                            INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                            WHERE categoria_id = ?
                            ''', [categoria])
            dado = cursor.fetchall()
            return dado

    def search_by_date (self, data1, data2) ->  list[sqlite3.Row] | None:
        with conect_bd() as banco:
            cursor = banco.cursor() 
            cursor.execute('''SELECT transacoes.* , categorias.nome FROM transacoes 
                            INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                            WHERE transacoes.data BETWEEN ? AND ?
                            ''', (data1, data2))
            dado = cursor.fetchall()
            return dado

  
    

    
    
    def all_cat_values (self) -> list[sqlite3.Row]:
        with conect_bd() as banco:
            cursor = banco.cursor() 
            cursor.execute('''SELECT SUM(transacoes.valor) AS total_valores, categorias.nome AS nome_categoria
                              FROM transacoes INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                              GROUP BY categorias.nome''')
            dados = cursor.fetchall()
            return dados
    
    def get_balance_and_expense (self) -> sqlite3.Row | None:
        with conect_bd() as banco:  
            cursor = banco.cursor()
            cursor.execute('''SELECT SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END) AS saldo_total,
                            SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END) AS despesa_total, 
                           (SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END) - 
                            SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END)) AS total_liquido
                            FROM transacoes
                            INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           ''')
            dados = cursor.fetchone()
            return dados
    
    def max_value_cat (self) -> tuple[sqlite3.Row,sqlite3.Row] | None :
        with conect_bd() as banco:  
            cursor = banco.cursor()
            cursor.execute('''SELECT transacoes.valor, categorias.nome FROM transacoes
                           INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           WHERE categorias.tipo = 1
                           ORDER BY transacoes.valor DESC
                           LIMIT 1''' )
            dados_saldo = cursor.fetchone()
            cursor.execute('''SELECT transacoes.valor, categorias.nome FROM transacoes
                           INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           WHERE categorias.tipo = 2
                           ORDER BY transacoes.valor DESC
                           LIMIT 1
                           ''')
            dados_despesa = cursor.fetchone()
            return dados_saldo, dados_despesa
        
    def get_all (self) -> list[sqlite3.Row]: 
        with conect_bd() as banco:  
            cursor = banco.cursor()
            cursor.execute('''SELECT transacoes.* , categoria.nome  FROM transacoes
                           INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           ORDER BY transacoes.data DESC''')
            dados = cursor.fetchall()
            return dados   
 
    
    
    
    


     

    