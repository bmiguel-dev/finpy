from models.transacao import Transacao, Categoria
from datetime import datetime
from typing import Callable, Optional

import sqlite3
from api import ResponseTransacoes, CriarTransacoes, CorrigirTransacoes, FiltrarTransacoes
class Financeiro:
   
    def __init__(self,conexão_banco : Callable[[],sqlite3.Connection] ):
        self.conectar_banco = conexão_banco

    def create_table_category(self):
        with self.conectar_banco() as banco:
            cursor = banco.cursor()
            cursor.execute(''' CREATE TABLE IF NOT EXISTS categorias (id INTEGER NOT NULL PRIMARY KEY, nome TEXT NOT NULL UNIQUE, tipo INTEGER NOT NULL)''')
            cursor.executemany('''INSERT OR IGNORE INTO categorias (id, nome, tipo) VALUES (?,?,?)''', Categoria.lista_categorias() )
            banco.commit()

    def create_table_transactions(self):
        with self.conectar_banco() as banco:
            cursor = banco.cursor() 
            cursor.execute(''' CREATE TABLE IF NOT EXISTS transacoes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                      categoria_id INTEGER,
                                                                      valor REAL NOT NULL,
                                                                      descricao TEXT NOT NULL,
                                                                      data DATE NOT NULL,
                            FOREIGN KEY (categoria_id) REFERENCES categorias(id))''')
            banco.commit() 


    def adict_transaction (self, entrada_dado : CriarTransacoes ):
        with self.conectar_banco() as banco:
            cursor = banco.cursor()
            cursor.execute('''INSERT INTO transacoes (categoria_id, valor, descricao, data)
                            VALUES (:categoria_id,:valor,:descricao,:data) ''', entrada_dado.model_dump())
            banco.commit()
            
    def remove_transaction (self, id:int):
        with self.conectar_banco() as banco:
            cursor = banco.cursor()
            cursor.execute('''DELETE FROM transacoes WHERE id = ?''', [id])
            banco.commit()

    def search_by_filter (self, filtro : FiltrarTransacoes):
        with self.conectar_banco() as banco:
            cursor = banco.cursor()
            dados = filtro.model_dump()
            categorias = dados['categoria_filtro']
            data_i = dados['d_inicio']
            data_f = dados['d_fim']
            
            query = '''SELECT transacoes.*, categorias.nome FROM transacoes
                           INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           WHERE 1=1'''
            parametros = []
            if filtro.categoria_filtro: 
                place_holders = ', '.join(['?'] * len(filtro.categoria_filtro))
                query += f" AND categoria_id IN ({place_holders})"
                parametros.extend(categorias)

            if filtro.d_inicio and filtro.d_fim:
                query += f" AND transacoes.data BETWEEN ? AND ?"
                parametros.extend([data_i, data_f])
            cursor.execute(query,parametros)
            dados_banco = cursor.fetchall()
            return dados_banco
    
  
    

    def search_by_id (self, id_: int):
        with self.conectar_banco() as banco:
            cursor = banco.cursor()
            cursor.execute('''SELECT transacoes.* , categorias.nome FROM transacoes
                           INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           WHERE transacoes.categoria_id = ?''', [id_] )
            dado = cursor.fetchone()
            return dado 
    
    
    def all_cat_values (self) -> list[sqlite3.Row]:
        with self.conectar_banco() as banco:
            cursor = banco.cursor() 
            cursor.execute('''SELECT SUM(transacoes.valor) AS total_valores, categorias.nome AS nome_categoria
                              FROM transacoes INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                              GROUP BY categorias.nome''')
            dados = cursor.fetchall()
            return dados
    
    def get_balance_and_expense (self) -> sqlite3.Row | None:
        with self.conectar_banco() as banco:  
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
        with self.conectar_banco() as banco:  
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
        with self.conectar_banco() as banco:  
            cursor = banco.cursor()
            cursor.execute('''SELECT transacoes.* , categoria.nome  FROM transacoes
                           INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           ORDER BY transacoes.data DESC''')
            dados = cursor.fetchall()
            return dados   
 
    
    
    
    


     

    