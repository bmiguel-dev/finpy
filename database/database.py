import sqlite3
from enums import Categoria


class DataBase:

    def __init__(self, db_name = 'finpy.db' ):
            self.db_name = db_name

    def initiate_table (self):
        with sqlite3.connect(self.db_name) as conn:
            self.cria_tabela_usuarios(conn=conn)
            self.cria_tabela_categorias(conn=conn)
            self.cria_tabela_transacoes(conn=conn)
            self.cria_idx_category(conn=conn)
            self.cria_idx_date(conn=conn)
            self.cria_idx_id_user(conn=conn) 
    
    def conexao_bd(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON;")   
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close() 
    
    def cria_tabela_categorias(self,conn : sqlite3.Connection):
        cursor = conn.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS categorias (id INTEGER NOT NULL PRIMARY KEY, nome TEXT NOT NULL UNIQUE, tipo INTEGER NOT NULL)''')
        cursor.executemany('''INSERT OR IGNORE INTO categorias (id, nome, tipo) VALUES (?,?,?)''', Categoria.lista_categorias() )
        conn.commit()
    
    def cria_tabela_usuarios (self, conn : sqlite3.Connection):
        cursor = conn.cursor() 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS usuarios (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                                nome TEXT UNIQUE NOT NULL,
                                                                                email TEXT UNIQUE NOT NULL,
                                                                                senha TEXT NOT NULL,
                                                                                criacao_login DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit() 
        
    def cria_tabela_transacoes (self, conn : sqlite3.Connection):
        cursor = conn.cursor() 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS transacoes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                            user_id INTEGER,
                                                                            categoria_id INTEGER,
                                                                            valor REAL NOT NULL,
                                                                            descricao TEXT NOT NULL,
                                                                            data DATE NOT NULL,
                                FOREIGN KEY (categoria_id) REFERENCES categorias(id),
                                FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE)''')
        conn.commit() 
    
    def cria_idx_category (self, conn : sqlite3.Connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_categoria_id ON transacoes(categoria_id)''')
        conn.commit()
            
    def cria_idx_date (self, conn : sqlite3.Connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data)''')
        conn.commit()
    
    def cria_idx_id_user (self, conn : sqlite3.Connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_user_id ON transacoes(user_id)''')
        conn.commit() 

database = DataBase()