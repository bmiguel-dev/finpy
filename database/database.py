import psycopg2
from psycopg2.extras import RealDictConnection
from psycopg2.extensions import connection
import os
from enums import Categoria
from typing import Generator

DATABASE_URL = os.getenv("DATABASE_URL")

class DataBase:

    def __init__(self, link = DATABASE_URL):
            self.db_link = link

    def initiate_table (self):
        with psycopg2.connect(self.db_link) as conn:
            self.cria_tabela_usuarios(conn=conn)
            self.cria_tabela_categorias(conn=conn)
            self.cria_tabela_transacoes(conn=conn)
            self.cria_idx_category(conn=conn)
            self.cria_idx_date(conn=conn)
            self.cria_idx_id_user(conn=conn) 
    
    def conexao_bd(self) -> Generator[RealDictConnection,None , None ]:
        conn = psycopg2.connect(self.db_link, connection_factory=RealDictConnection) 
        try:
            yield conn
        finally:
            conn.close() 
    
    def cria_tabela_categorias(self,conn : connection):
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS categorias (id INTEGER NOT NULL PRIMARY KEY, nome TEXT NOT NULL UNIQUE, tipo INTEGER NOT NULL)''')
        cursor.executemany(''' INSERT INTO categorias (id, nome, tipo) VALUES (%s ,%s,%s)  ON CONFLICT (id) DO NOTHING  ''', Categoria.lista_categorias() )
        conn.commit()
    
    def cria_tabela_usuarios (self, conn : connection ):
        cursor = conn.cursor() 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY ,
                                                                                nome TEXT UNIQUE NOT NULL,
                                                                                email TEXT UNIQUE NOT NULL,
                                                                                senha TEXT NOT NULL,
                                                                                criacao_login TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit() 
        
    def cria_tabela_transacoes (self, conn : connection):
        cursor = conn.cursor() 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS transacoes (id SERIAL PRIMARY KEY,
                                                                            user_id INTEGER,
                                                                            categoria_id INTEGER,
                                                                            valor NUMERIC(10,2) NOT NULL,
                                                                            descricao TEXT NOT NULL,
                                                                            data DATE NOT NULL,
                                FOREIGN KEY (categoria_id) REFERENCES categorias(id),
                                FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE)''')
        conn.commit() 
    
    def cria_idx_category (self, conn : connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_categoria_id ON transacoes(categoria_id)''')
        conn.commit()
            
    def cria_idx_date (self, conn : connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data)''')
        conn.commit()
    
    def cria_idx_id_user (self, conn : connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_user_id ON transacoes(user_id)''')
        conn.commit() 

database = DataBase()