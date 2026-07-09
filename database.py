import sqlite3





def conect_db():
    banco = sqlite3.connect('finpy.db')
    banco.execute("PRAGMA foreign_keys = ON;")
    banco.row_factory = sqlite3.Row
    return banco 


