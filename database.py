import sqlite3
from enums import Categoria




def conect_bd():
    banco = sqlite3.connect('finpy.db')
    banco.execute("PRAGMA foreign_keys = ON;")
    banco.row_factory = sqlite3.Row
    return banco 

def create_table_category():
    with conect_bd() as banco:
        cursor = banco.cursor()
        cursor.execute(''' CREATE TABLE IF NOT EXISTS categorias (id INTEGER NOT NULL PRIMARY KEY, nome TEXT NOT NULL UNIQUE, tipo INTEGER NOT NULL)''')
        cursor.executemany('''INSERT OR IGNORE INTO categorias (id, nome, tipo) VALUES (?,?,?)''', Categoria.lista_categorias() )
        banco.commit()

def create_table_transactions():
    with conect_bd() as banco:
        cursor = banco.cursor() 
        cursor.execute(''' CREATE TABLE IF NOT EXISTS transacoes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                      categoria_id INTEGER,
                                                                      valor REAL NOT NULL,
                                                                      descricao TEXT NOT NULL,
                                                                      data DATE NOT NULL,
                            FOREIGN KEY (categoria_id) REFERENCES categorias(id))''')
        banco.commit() 

