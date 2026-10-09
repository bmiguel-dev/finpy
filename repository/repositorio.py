from psycopg2.extensions import connection
from models import *
from typing import Any
import psycopg2

class RepositorioUsuarios:
    def __init__(self, conn : connection ):
        self.conn = conn 
    
    
    def criar_usuario (self, entrada_dado : UsuarioCadastro, senha_hash : str) -> int:
        cursor = self.conn.cursor()
        dados = entrada_dado.model_dump()
        dados['senha'] = senha_hash
        cursor.execute('''INSERT INTO usuarios(nome, email, senha) VALUES (%(nome)s, %(email)s, %(senha)s) RETURNING id''', dados )
        id_novo = cursor.fetchone()[0]
        return id_novo
    
    def procurar_usuario_pelo_email (self, dados : UsuarioCadastro | UsuarioLogin ) -> dict[str,Any]:
        email = dados.email
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", [email])
        return cursor.fetchone()
        
    def procurar_usuario_pelo_id(self, id_: int) -> dict[str,Any] | None :
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", [id_])
        return cursor.fetchone()
        

class RepositorioTransacoes:
    def __init__(self, conn : connection ):
        self.conn = conn 
                
    def adicionar_transacao (self, entrada_dado : CriarTransacoes,  usuario_atual: int ) -> int: 
        cursor = self.conn.cursor()
        entrada_dado = entrada_dado.model_dump()
        entrada_dado["user_id"] = usuario_atual
        cursor.execute('''INSERT INTO transacoes (user_id, categoria_id, valor, descricao, data)
                            VALUES (%(user_id)s, %(categoria_id)s,%(valor)s,%(descricao)s,%(data)s) RETURNING id''', entrada_dado)
        id_novo = cursor.fetchone[0]
        return id_novo
                
    def remover_transacao (self, id:int ,  usuario_id : int):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM transacoes WHERE id = %s AND user_id  = %s''', [id,usuario_id])
    
    
    def procurar_transacao_filtrada (self,categorias:list[int], filtro : FiltrarTransacoes , usuario_id : int) -> list[dict[str,Any]]:
        cursor = self.conn.cursor()
        dados = filtro.model_dump()
        data_i = dados.get('d_inicio')
        data_f = dados.get('d_fim') 
        query = '''SELECT transacoes.*, categorias.nome FROM transacoes
                               INNER JOIN categorias ON transacoes.categoria_id = categorias.id
                               WHERE transacoes.user_id = %s'''
        parametros = [usuario_id]
        if categorias:
            query += " AND categorias.id =  ANY(%s::int[])"
            parametros.append(categorias)
        if data_i and data_f:
            query += " AND transacoes.data BETWEEN %s AND %s"
            parametros.extend([data_i, data_f])
        elif data_i:
            query += " AND transacoes.data >= %s"
            parametros.append(data_i)
        elif data_f:
            query += " AND transacoes.data <= %s"
            parametros.append(data_f)
        cursor.execute(query,parametros)
        dados_banco = cursor.fetchall()
        return dados_banco
        
      
        
    
    def procurar_pelo_id (self, id_: int , usuario_id : int) -> dict[str,Any]:
        cursor = self.conn.cursor()
        cursor.execute('''SELECT transacoes.*  FROM transacoes
                           WHERE transacoes.id = %s AND transacoes.user_id = %s''', [id_, usuario_id] )
        dado = cursor.fetchone()
        return dado
        
        
    def calcular_valores_totais_categorias (self , usuario_id: int) -> list[dict[str,Any]]:
            cursor = self.conn.cursor() 
            cursor.execute('''SELECT SUM(transacoes.valor) AS total_valores, categorias.nome AS nome_categoria
                                  FROM transacoes INNER JOIN categorias ON transacoes.categoria_id = categorias.id WHERE transacoes.user_id = %s
                                  GROUP BY categorias.nome''', [usuario_id])
            dados = cursor.fetchall()
            return dados
        
    def calcular_despesa_lucro (self , usuario_id) -> dict[str,Any]:
            cursor = self.conn.cursor()
            cursor.execute('''SELECT COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) AS saldo_total,
                                COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS despesa_total, 
                               COALESCE(SUM(CASE WHEN categorias.tipo = 1 THEN transacoes.valor ELSE 0 END),0) - 
                                COALESCE(SUM(CASE WHEN categorias.tipo = 2 THEN transacoes.valor ELSE 0 END),0) AS total_liquido
                                FROM transacoes
                                INNER JOIN categorias ON transacoes.categoria_id = categorias.id WHERE transacoes.user_id = %s
                               ''', [usuario_id])
            dados = cursor.fetchone()
            return dados
        
            
     
    def corrigir_transação (self, id_ : int, dados : CorrigirTransacoes , usuario_id : int ) -> bool:
        dados_dict = {chave:valor for chave,valor in  dados.model_dump().items() if valor is not None}
        place_holder = ", ".join([f'{chave} = %s' for chave in  dados_dict.keys()])
        parametros = []
        parametros.extend(list(dados_dict.values()))
        parametros.append(id_)
        parametros.append(usuario_id)
        query = f"UPDATE transacoes SET {place_holder} WHERE id = %s AND user_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query,parametros)
        return True