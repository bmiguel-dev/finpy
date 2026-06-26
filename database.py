import sqlite3
from enums import Categoria
from typing import Callable




def conect_db():
    banco = sqlite3.connect('finpy.db')
    banco.execute("PRAGMA foreign_keys = ON;")
    banco.row_factory = sqlite3.Row
    return banco 


