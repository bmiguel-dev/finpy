from typing import Callable 
import sqlite3
from models import *


class Financeiro:
   
    def __init__(self, db_name = 'finpy.db' ):
        self.db_name = db_name

    def iniciate_table (self):
        with sqlite3.connect(self.db_name) as conn:
            self.create_table_category(conn=conn)
            self.create_table_transactions(conn=conn)
            self.create_idx_category(conn=conn)
            self.create_idx_date(conn=conn)

    def conect_db(self):
        banco = sqlite3.connect('finpy.db')
        banco.execute("PRAGMA foreign_keys = ON;")
        banco.row_factory = sqlite3.Row
        try:
            yield banco
        finally:
            banco.close() 

    def create_table_category(self,conn : sqlite3.Connection):
            cursor = conn.cursor()
            cursor.execute(''' CREATE TABLE IF NOT EXISTS categorias (id INTEGER NOT NULL PRIMARY KEY, nome TEXT NOT NULL UNIQUE, tipo INTEGER NOT NULL)''')
            cursor.executemany('''INSERT OR IGNORE INTO categorias (id, nome, tipo) VALUES (?,?,?)''', Categoria.lista_categorias() )
            conn.commit()
    
    def create_table_transactions(self, conn : sqlite3.Connection):
            cursor = conn.cursor() 
            cursor.execute(''' CREATE TABLE IF NOT EXISTS transacoes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                      categoria_id INTEGER,
                                                                      valor REAL NOT NULL,
                                                                      descricao TEXT NOT NULL,
                                                                      data DATE NOT NULL,
                            FOREIGN KEY (categoria_id) REFERENCES categorias(id))''')
            conn.commit() 

    def create_idx_category (self, conn : sqlite3.Connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_categoria_id ON transacoes(categoria_id)''')
        conn.commit()
        
    def create_idx_date (self, conn : sqlite3.Connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data)''')
        conn.commit()

    def adict_transaction (self, entrada_dado : CriarTransacoes, conn : sqlite3.Connection ):
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO transacoes (categoria_id, valor, descricao, data)
                        VALUES (:categoria_id,:valor,:descricao,:data) ''', entrada_dado.model_dump())
        conn.commit()
        return cursor.lastrowid
            
    def remove_transaction (self, id:int , conn : sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM transacoes WHERE id = ?''', [id])
        conn.commit()

    def search_by_filter (self,categorias:list[int], filtro : FiltrarTransacoes , conn : sqlite3.Connection):
        cursor = conn.cursor()
        dados = filtro.model_dump()
        print("DEBUG filtro recebido:", dados)
        data_i = dados.get('d_inicio')
        data_f = dados.get('d_fim') 
        query = '''SELECT transacoes.*, categorias.nome FROM transacoes
                           INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           WHERE 1=1'''
        parametros = []
        if categorias:
            place_holders = ', '.join(['?'] * len(categorias))
            query += f" AND categorias.id IN ({place_holders})"
            parametros.extend(categorias)
        if data_i and data_f:
            query += f" AND transacoes.data BETWEEN ? AND ?"
            parametros.extend([data_i, data_f])
        cursor.execute(query,parametros)
        dados_banco = cursor.fetchall()
        return dados_banco
    
  
    

    def search_by_id (self, id_: int , conn : sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute('''SELECT transacoes.*  FROM transacoes
                           WHERE transacoes.id = ?''', [id_] )
        dado = cursor.fetchone()
        return dado
    
    
    def all_cat_values (self , conn : sqlite3.Connection) -> list[sqlite3.Row]:
        cursor = conn.cursor() 
        cursor.execute('''SELECT SUM(transacoes.valor) AS total_valores, categorias.nome AS nome_categoria
                              FROM transacoes INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                              GROUP BY categorias.nome''')
        dados = cursor.fetchall()
        return dados
    
    def get_balance_and_expense (self , conn : sqlite3.Connection) -> sqlite3.Row | None:
        cursor = conn.cursor()
        cursor.execute('''SELECT COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) AS saldo_total,
                            COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS despesa_total, 
                           COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) - 
                            COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS total_liquido
                            FROM transacoes
                            INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           ''')
        dados = cursor.fetchone()
        return dados
    
        
 
    def correct_transaction (self, id_, dados : CorrigirTransacoes ,conn : sqlite3.Connection):
        dados_dict = {chave:valor for chave,valor in  dados.model_dump().items() if valor is not None}
        place_holder = ", ".join([f'{chave} = ?' for chave in  dados_dict.keys()])
        parametros = []
        parametros.extend(list(dados_dict.values()))
        parametros.append(id_)
        query = f"UPDATE transacoes SET {place_holder} WHERE transacoes.id = ?"
        cursor = conn.cursor()
        cursor.execute(query,parametros)
        conn.commit()
        return True
        

    
    


     

    