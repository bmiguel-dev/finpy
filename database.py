import sqlite3
from enums import Categoria




def conectar_banco():
    banco = sqlite3.connect('finpy.db')
    banco.row_factory = sqlite3.Row
    return banco 

def criar_tabela_categorias():
    with conectar_banco() as banco:
        cursor = banco.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS categorias (id INTEGER NOT NULL PRIMARY KEY, nome TEXT NOT NULL UNIQUE, tipo INTEGER NOT NULL)''')
        cursor.executemany('''INSERT OR IGNORE INTO categorias (id, nome, tipo) VALUES (?,?,?)''', Categoria.lista_categorias() )
        banco.commit()

def criar_tabela_transacoes():
    with conectar_banco() as banco:
        cursor = banco.cursor() 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS transacoes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                      categoria_id INTEGER,
                                                                      valor REAL NOT NULL,
                                                                      descricao TEXT NOT NULL,
                            FOREIGN KEY (categoria_id) REFERENCES categorias(id))''')
        banco.commit()