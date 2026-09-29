from repository import RepositorioTransacoes
from utils.erros import TransacaoNaoEncontrada
from models.transacao import CategoriaTotal, Metricas, FiltrarTransacoes, CriarTransacoes,CorrigirTransacoes
import sqlite3

class ServiceTransacoes:
    def __init__ (self , repositorio : RepositorioTransacoes):
        self.repositorio = repositorio

    def verificar_transacao_id(self,id_,usuario_id) -> list[dict]  :
        dados = self.repositorio.procurar_pelo_id(id_=id_, usuario_id=usuario_id)
        if not dados:
            raise TransacaoNaoEncontrada("Transação não encontrada.")
        return dict(dados) #devolve a transação 
    
    def categorias_e_valores_totais ( self, usuario_id : int ) -> list[CategoriaTotal] | list:
        return [CategoriaTotal(**dict(d)) for d in self.repositorio.valores_totais_categorias(usuario_id=usuario_id)] #lista de objetos que guarda CATEGORIA e VALOR TOTAL 

    def saldo_despesa (self, usuario_id : int) -> Metricas | None   :
        return Metricas(**dict(self.repositorio.calculo_despesa_lucro(usuario_id=usuario_id)))

    def adicionar_transacoes(self, transacao : CriarTransacoes , usuario_id : int) -> sqlite3.Row :
        id_transacao = self.repositorio.adiciona_transacao(transacao,usuario_id)
        return  self.repositorio.procurar_pelo_id(id_=id_transacao, usuario_id=usuario_id) #retorna um sqlite3.Row

    def remove_transacao(self,id_transacao : int,usuario_atual : int) -> None:
        self.repositorio.remove_transacao(id=id_transacao,usuario_id=usuario_atual)
        return 

    def corrigir_transacao(self,id_:dict ,usuario_id : dict, dados : CorrigirTransacoes ) -> dict:
        self.repositorio.corrige_transação(id_=id_, dados=dados, usuario_id=usuario_id)
        return dict(self.repositorio.procurar_pelo_id(id_=id_, usuario_id=usuario_id))
        
    def filtrar_transacoes_id_categorias (self, categorias : list[int], filtro : FiltrarTransacoes, usuario_id : int ) -> list[dict] | list:
        dados_banco = self.repositorio.procurar_pelo_filtro(categorias,filtro,usuario_id)
        return [dict(d) for d in dados_banco] 