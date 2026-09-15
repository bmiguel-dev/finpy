from repository import RepositorioTransacoes
from erros import TransacaoNaoEncontrada

class ServiceTransacoes:
    def __init__ (self , repositorio : RepositorioTransacoes):
        self.repositorio = repositorio

    def verificar_id_transacao(self,id_,usuario_id):
        dados = self.repositorio.procurar_pelo_id(id_=id_, usuario_id=usuario_id)
        if not dados:
            raise TransacaoNaoEncontrada("Transação não encontrada.")
        return dict(dados) #devolve a transação em formato de dict
   