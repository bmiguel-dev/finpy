from typing import Callable 
import sqlite3
from models import *

class Financeiro:
   
    def __init__(self,conexão_banco : Callable[[],sqlite3.Connection] ):
        self.conectar_banco = conexão_banco

    def iniciate_table (self):
        self.create_table_category()
        self.create_table_transactions()
        self.create_idx_category()
        self.create_idx_date()
        
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

    def create_idx_category (self):
        with self.conectar_banco() as banco:
            cursor = banco.cursor()
            cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_categoria_id ON transacoes(categoria_id)''')
            banco.commit()
        
    def create_idx_date (self):
        with self.conectar_banco() as banco:
            cursor = banco.cursor()
            cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data)''')
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
                           WHERE transacoes.id = ?''', [id_] )
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
            cursor.execute('''SELECT COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) AS saldo_total,
                            COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS despesa_total, 
                           (COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) - 
                            COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS total_liquido
                            FROM transacoes
                            INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           ''')
            dados = cursor.fetchone()
            return dados
    
        
 
    def correct_transaction (self, id_, dados : CorrigirTransacoes):
        dados_dict = {chave:valor for chave,valor in  dados.model_dump().items() if valor is not None}
        place_holder = ", ".join([f'{chave} = ?' for chave in  dados_dict.keys()])
        parametros = []
        parametros.extend(list(dados_dict.values()))
        parametros.append(id_)
        query = f"UPDATE transacoes SET {place_holder} WHERE transacoes.id = ?"
        with self.conectar_banco() as banco: 
            cursor = banco.cursor()
            cursor.execute(query,parametros)
            banco.commit()
            return True
        
    
    
    
    


     

    