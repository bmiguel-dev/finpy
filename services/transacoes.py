from repository import RepositorioTransacoes
from utils.erros import TransacaoNaoEncontrada
from models.transacao import CategoriaTotal, Metricas, FiltrarTransacoes, CriarTransacoes,CorrigirTransacoes
from typing import Any

class ServiceTransacoes:
    def __init__ (self , repositorio : RepositorioTransacoes):
        self.repositorio = repositorio

    def verificar_transacao_id(self,id_,usuario_id) -> list[dict]  :
        dados = self.repositorio.procurar_pelo_id(id_=id_, usuario_id=usuario_id)
        if not dados:
            raise TransacaoNaoEncontrada("Transação não encontrada.")
        return dados
    
    def categorias_e_valores_totais ( self, usuario_id : int ) -> list[CategoriaTotal] :
        return [CategoriaTotal(**d) for d in self.repositorio.calcular_valores_totais_categorias(usuario_id=usuario_id)] #lista de objetos que guarda CATEGORIA e VALOR TOTAL 

    def calcular_saldo_despesa (self, usuario_id : int) -> Metricas | None   :
        return Metricas(**self.repositorio.calcular_despesa_lucro(usuario_id=usuario_id))

    def adicionar_transacoes(self, transacao : CriarTransacoes , usuario_id : int) -> dict[str,Any] :
        id_transacao = self.repositorio.adicionar_transacao(transacao,usuario_id)
        self.repositorio.conn.commit()
        return  self.repositorio.procurar_pelo_id(id_=id_transacao, usuario_id=usuario_id) 

    def remover_transacao(self,id_transacao : int,usuario_id : int) -> None:
        transacao = self.repositorio.procurar_pelo_id(id_=id_transacao,usuario_id=usuario_id)
        if not transacao:
            raise TransacaoNaoEncontrada("Transação não encontrada")
        self.repositorio.remover_transacao(id=id_transacao,usuario_id=usuario_id)
        self.repositorio.conn.commit()
        return 

    def corrigir_transacao(self,id_transacao:int ,usuario_id : dict, dados : CorrigirTransacoes ) -> dict:
        transacao = self.repositorio.procurar_pelo_id(id_=id_transacao,usuario_id=usuario_id)
        if not transacao:
            raise TransacaoNaoEncontrada("Transação não encontrada")
        self.repositorio.corrigir_transação(id_=id_transacao, dados=dados, usuario_id=usuario_id)
        self.repositorio.conn.commit()
        return self.repositorio.procurar_pelo_id(id_=id_transacao, usuario_id=usuario_id)
        
    def filtrar_transacoes_categorias (self, categorias : list[int], filtro : FiltrarTransacoes, usuario_id : int ) -> list[dict] | list:
        dados_banco = self.repositorio.procurar_transacao_filtrada(categorias,filtro,usuario_id)
        return [d for d in dados_banco] 