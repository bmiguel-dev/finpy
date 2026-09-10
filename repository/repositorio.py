import sqlite3
from models import *
from database import database

class RepositorioUsuarios:
    def __init__(self, conn : sqlite3.Connection ):
        self.conn = conn 
    
    
    def cria_usuario (self, entrada_dado : UsuarioCadastro, hash : str):
        cursor = self.conn.cursor()
        dados = entrada_dado.model_dump()
        dados['senha'] = hash
        cursor.execute('''INSERT INTO usuarios (nome, email, senha) VALUES (:nome,:email,:senha)''', dados )
        self.conn.commit()
        return cursor.lastrowid
    
    
    def procurar_usuario_pelo_email (self, dados : UsuarioCadastro | UsuarioLogin ) -> sqlite3.Row:
        email = dados.email
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ?", [email])
        return cursor.fetchone()
        
    def procurar_usuario_pelo_id(self, id_: int, conn: sqlite3.Connection) -> sqlite3.Row:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", [id_])
        return cursor.fetchone()
        

class RepositorioTransacoes:
    def __init__(self, conn : sqlite3.Connection ):
        self.conn = conn 
                
    def adiciona_transacao (self, entrada_dado : CriarTransacoes,  usuario_atual: int ) -> int: 
        cursor = self.conn.cursor()
        entrada_dado = entrada_dado.model_dump()
        entrada_dado["user_id"] = usuario_atual
        cursor.execute('''INSERT INTO transacoes (user_id, categoria_id, valor, descricao, data)
                            VALUES (:user_id, :categoria_id,:valor,:descricao,:data) ''', entrada_dado)
        self.conn.commit()
        return cursor.lastrowid
                
    def remove_transacao (self, id:int ,  usuario_id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM transacoes WHERE id = ? AND user_id  = ?''', [id,usuario_id])
        self.conn.commit()
    
    def procurar_pelo_filtro (self,categorias:list[int], filtro : FiltrarTransacoes , usuario_id : int) -> list[sqlite3.Row] | None:
        cursor = self.conn.cursor()
        dados = filtro.model_dump()
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
        
      
        
    
    def procurar_pelo_id (self, id_: int , usuario_id : int) -> sqlite3.Row:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT transacoes.*  FROM transacoes
                           WHERE transacoes.id = ? AND transacoes.user_id = ?''', [id_, usuario_id] )
        dado = cursor.fetchone()
        return dado
        
        
    def valores_totais_categorias (self , usuario_id: int) -> list[sqlite3.Row]:
            cursor = self.conn.cursor() 
            cursor.execute('''SELECT SUM(transacoes.valor) AS total_valores, categorias.nome AS nome_categoria
                                  FROM transacoes INNER JOIN categorias ON transacoes.categoria_id = categorias.id WHERE transacoes.user_id = ?
                                  GROUP BY categorias.nome''', [usuario_id])
            dados = cursor.fetchall()
            return dados
        
    def calculo_despesa_lucro (self , usuario_id) -> sqlite3.Row | None:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) AS saldo_total,
                                COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS despesa_total, 
                               COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) - 
                                COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS total_liquido
                                FROM transacoes
                                INNER JOIN categorias ON transacoes.categoria_id = categorias.id WHERE transacoes.user_id = ?
                               ''', [usuario_id])
            dados = cursor.fetchone()
            return dados
        
            
     
    def corrige_transação (self, id_, dados : CorrigirTransacoes , usuario_id : int ) -> bool:
        dados_dict = {chave:valor for chave,valor in  dados.model_dump().items() if valor is not None}
        place_holder = ", ".join([f'{chave} = ?' for chave in  dados_dict.keys()])
        parametros = []
        parametros.extend(list(dados_dict.values()))
        parametros.append(id_)
        parametros.append(usuario_id)
        query = f"UPDATE transacoes SET {place_holder} WHERE id = ? AND user_id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query,parametros)
        self.conn.commit()
        return True