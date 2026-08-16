import sqlite3
from models import *
from utils.hash import verifica_senha,criar_hash



class Financeiro:
   
    def __init__(self, db_name = 'finpy.db' ):
        self.db_name = db_name

    def initiate_table (self):
        with sqlite3.connect(self.db_name) as conn:
            self.create_table_usuarios(conn=conn)
            self.create_table_categorias(conn=conn)
            self.create_table_transacoes(conn=conn)
            self.create_idx_category(conn=conn)
            self.create_idx_date(conn=conn)
            self.create_idx_id_user(conn=conn) 

    def conect_db(self):
        banco = sqlite3.connect(self.db_name)
        banco.execute("PRAGMA foreign_keys = ON;")
        banco.row_factory = sqlite3.Row
        try:
            yield banco
        finally:
            banco.close() 

    def create_table_categorias(self,conn : sqlite3.Connection):
            cursor = conn.cursor()
            cursor.execute(''' CREATE TABLE IF NOT EXISTS categorias (id INTEGER NOT NULL PRIMARY KEY, nome TEXT NOT NULL UNIQUE, tipo INTEGER NOT NULL)''')
            cursor.executemany('''INSERT OR IGNORE INTO categorias (id, nome, tipo) VALUES (?,?,?)''', Categoria.lista_categorias() )
            conn.commit()

    def create_table_usuarios (self, conn : sqlite3.Connection):
                cursor = conn.cursor() 
                cursor.execute(''' CREATE TABLE IF NOT EXISTS usuarios (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                          nome TEXT UNIQUE NOT NULL,
                                                                          email TEXT UNIQUE NOT NULL,
                                                                          senha TEXT NOT NULL,
                                                                          criacao_login DATETIME DEFAULT CURRENT_TIMESTAMP)''')
                conn.commit() 
    
    def create_table_transacoes (self, conn : sqlite3.Connection):
            cursor = conn.cursor() 
            cursor.execute(''' CREATE TABLE IF NOT EXISTS transacoes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                      user_id INTEGER,
                                                                      categoria_id INTEGER,
                                                                      valor REAL NOT NULL,
                                                                      descricao TEXT NOT NULL,
                                                                      data DATE NOT NULL,
                            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
                            FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE)''')
            conn.commit() 

    def create_idx_category (self, conn : sqlite3.Connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_categoria_id ON transacoes(categoria_id)''')
        conn.commit()
        
    def create_idx_date (self, conn : sqlite3.Connection ):
        cursor = conn.cursor()
        cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data)''')
        conn.commit()

    def create_idx_id_user (self, conn : sqlite3.Connection ):
            cursor = conn.cursor()
            cursor.execute('''CREATE INDEX IF NOT EXISTS idx_transacoes_user_id ON transacoes(user_id)''')
            conn.commit()

    def create_user (self, entrada_dado : UsuarioCadastro,  conn:sqlite3.Connection):
        cursor = conn.cursor()
        dados = entrada_dado.model_dump()
        dados['senha'] = criar_hash(entrada_dado.senha)
        cursor.execute('''INSERT INTO usuarios (nome, email, senha) VALUES (:nome,:email,:senha)''', dados )
        conn.commit()
        return cursor.lastrowid

    def user_validation (self, dados : UsuarioLogin, conn : sqlite3.Connection) -> int | bool: #email e senha
        cursor = conn.cursor() 
        cursor.execute(''' SELECT id , senha FROM usuarios WHERE email = ?''', [dados.email])
        resultado = cursor.fetchone()
        if resultado is None:
            return False
        dados_validados = dict(resultado)
        id_user = dados_validados.get('id')
        senha_hash = dados_validados.get('senha')
        senha_verificada = verifica_senha (senha=dados.senha, hash=senha_hash)
        if senha_verificada is False:
            return False
        return id_user

    def search_user_by_email (self, dados : UsuarioCadastro, conn : sqlite3.Connection ):
        email = dados.email
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", [email])
        return cursor.fetchone()
    
    def search_user_by_id(self, id_: int, conn: sqlite3.Connection) -> sqlite3.Row:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", [id_])
        return cursor.fetchone()
    
            
    def adict_transaction (self, entrada_dado : CriarTransacoes, conn : sqlite3.Connection, usuario_atual: int ) -> int: #TRANSACAO ESTA SEM USER_ID
        cursor = conn.cursor()
        entrada_dado = entrada_dado.model_dump()
        entrada_dado["user_id"] = usuario_atual
        cursor.execute('''INSERT INTO transacoes (user_id, categoria_id, valor, descricao, data)
                        VALUES (:user_id, :categoria_id,:valor,:descricao,:data) ''', entrada_dado)
        conn.commit()
        return cursor.lastrowid
            
    def remove_transaction (self, id:int , conn : sqlite3.Connection, usuario_id):
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM transacoes WHERE id = ? AND user_id  = ?''', [id,usuario_id])
        conn.commit()

    def search_by_filter (self,categorias:list[int], filtro : FiltrarTransacoes , conn : sqlite3.Connection, usuario_id : int) -> list[sqlite3.Row] | None:
        cursor = conn.cursor()
        dados = filtro.model_dump()
        print("DEBUG filtro recebido:", dados)
        data_i = dados.get('d_inicio')
        data_f = dados.get('d_fim') 
        query = '''SELECT transacoes.*, categorias.nome FROM transacoes
                           INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                           WHERE transacoes.user_id = ?'''
        parametros = [usuario_id]
        if categorias:
            place_holders = ', '.join(['?'] * len(categorias))
            query += f" AND categorias.id IN ({place_holders})"
            parametros.extend(categorias)
        if data_i and data_f:
            query += f" AND transacoes.data BETWEEN ? AND ?"
            parametros.extend([data_i, data_f])
        elif data_i:
            query += " AND transacoes.data >= ?"
            parametros.append(data_i)
        elif data_f:
            query += " AND transacoes.data <= ?"
            parametros.append(data_f)
        cursor.execute(query,parametros)
        dados_banco = cursor.fetchall()
        return dados_banco
    
  
    

    def search_by_id (self, id_: int , conn : sqlite3.Connection, usuario_id : int):
        cursor = conn.cursor()
        cursor.execute('''SELECT transacoes.*  FROM transacoes
                           WHERE transacoes.id = ? AND transacoes.user_id = ?''', [id_, usuario_id] )
        dado = cursor.fetchone()
        return dado
    
    
    def all_cat_values (self , conn : sqlite3.Connection, usuario_id: int) -> list[sqlite3.Row]:
        cursor = conn.cursor() 
        cursor.execute('''SELECT SUM(transacoes.valor) AS total_valores, categorias.nome AS nome_categoria
                              FROM transacoes INNER JOIN categorias ON transacoes.categoria_id = categorias.id WHERE transacoes.user_id = ?
                              GROUP BY categorias.nome''', [usuario_id])
        dados = cursor.fetchall()
        return dados
    
    def get_balance_and_expense (self , conn : sqlite3.Connection, usuario_id) -> sqlite3.Row | None:
        cursor = conn.cursor()
        cursor.execute('''SELECT COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) AS saldo_total,
                            COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS despesa_total, 
                           COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) - 
                            COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS total_liquido
                            FROM transacoes
                            INNER JOIN categorias ON transacoes.categoria_id = categorias.id WHERE transacoes.user_id = ?
                           ''', [usuario_id])
        dados = cursor.fetchone()
        return dados
    
        
 
    def correct_transaction (self, id_, dados : CorrigirTransacoes ,conn : sqlite3.Connection, usuario_id : int ):
        dados_dict = {chave:valor for chave,valor in  dados.model_dump().items() if valor is not None}
        place_holder = ", ".join([f'{chave} = ?' for chave in  dados_dict.keys()])
        parametros = []
        parametros.extend(list(dados_dict.values()))
        parametros.append(id_)
        parametros.append(usuario_id)
        query = f"UPDATE transacoes SET {place_holder} WHERE id = ? AND user_id = ?"
        cursor = conn.cursor()
        cursor.execute(query,parametros)
        conn.commit()
        return True
        

    
    


     

    