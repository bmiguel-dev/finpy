from fastapi import  APIRouter, Depends,Query
from models.transacao import CriarTransacoes, CorrigirTransacoes, FiltrarTransacoes, ResponseTransacoes,ResponseMetricas,CategoriaTotal,Metricas
from utils.seguranca import  validar_token_acess
from database.database import database, DataBase
from repository import RepositorioTransacoes
from services import ServiceTransacoes, ServiceUsuarios
from router.usuarios import get_service_usuario


router = APIRouter(prefix="/transacoes",tags=['Transações'])

#os get ... vão nos Depends preparar o ambiente para a rotar retornar o que foi requisitado
def get_service_transacao (conn : DataBase = Depends(database.conexao_bd)) -> ServiceTransacoes:
    repositorio_conn = RepositorioTransacoes(conn=conn)
    return ServiceTransacoes(repositorio_conn)

def get_usuario_atual (usuario_id : int = Depends(validar_token_acess), service_usuario : ServiceUsuarios = Depends(get_service_usuario) ) -> int: #faz a verificacao do id do usuario, precisa do service de usuarios para funcionar
    service_usuario.verificar_usuario_id(usuario_id)
    return  usuario_id

@router.get("/")
def listar_transacoes (categorias : list[int] = Query(default=None,title="Categorias ID", alias="cat"),
                       filtro : FiltrarTransacoes = Depends(FiltrarTransacoes), service : ServiceTransacoes = Depends(get_service_transacao), usuario_atual : int = Depends(get_usuario_atual)):
    dados = service.filtrar_transacoes_id_categorias(categorias=categorias,filtro=filtro,usuario_id=usuario_atual)                                    #retorna o id do usuario
    return [ResponseTransacoes(**dict(d)) for d in dados ]
    
@router.get("/metricas", status_code=200,response_model= ResponseMetricas)
def exibir_metricas(service  : ServiceTransacoes = Depends(get_service_transacao), usuario_atual : int = Depends(get_usuario_atual)): 
    lista_categorias = service.categorias_e_valores_totais(usuario_atual) # lista com categorias e valores totais
    metrica = service.saldo_despesa(usuario_atual) # lista com saldo despesa e lucro
    return  ResponseMetricas(categoria_total=lista_categorias,metricas_= metrica)

@router.post("/new",status_code=201,response_model=ResponseTransacoes)
def criar_transacao (transacoes: CriarTransacoes,service  : ServiceTransacoes = Depends(get_service_transacao), usuario_atual : int = Depends(get_usuario_atual)):
    transacao_adicionada  = service.adicionar_transacoes(transacoes, usuario_atual)
    return dict(transacao_adicionada)

@router.get("/{id_}",  response_model=ResponseTransacoes)
def transacao_por_id (id_: int, service : ServiceTransacoes = Depends(get_service_transacao), usuario_atual : int = Depends(get_usuario_atual)):   
    return service.verificar_transacao_id(id_)


@router.delete("/{id_}", status_code = 204)
def deletar_transacoes (id_:int , service : ServiceTransacoes = Depends(get_service_transacao) , usuario_atual : int = Depends(get_usuario_atual)):
    id_confirmado = service.verificar_transacao_id(id_=id_)
    service.remove_transacao(id_, usuario_atual)
    return 
    
@router.patch("/{id_}", status_code= 200, response_model= ResponseTransacoes)
def corrigir_transacao (id_:int, dados: CorrigirTransacoes , service : ServiceTransacoes = Depends(get_service_transacao) , usuario_atual : int = Depends(get_usuario_atual)):
    service.verificar_transacao_id(id_=id_, usuario_id=usuario_atual)
    retornar_transacao = service.corrigir_transacao(id_=id_, dados=dados, usuario_id=usuario_atual) 
    return retornar_transacao
      