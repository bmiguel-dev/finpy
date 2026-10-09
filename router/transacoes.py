from fastapi import  APIRouter, Depends,Query
from models.transacao import CriarTransacoes, CorrigirTransacoes, FiltrarTransacoes, ResponseTransacoes,ResponseMetricas,CategoriaTotal,Metricas
from services import ServiceTransacoes
from depends import  get_service_transacao, get_usuario_atual


router = APIRouter(prefix="/transacoes",tags=['Transações'])


@router.get("/")
def listar_transacoes (categorias : list[int] = Query(default=None,title="Categorias ID", alias="cat"),
                       filtro : FiltrarTransacoes = Depends(FiltrarTransacoes), service : ServiceTransacoes = Depends(get_service_transacao), usuario_atual : int = Depends(get_usuario_atual)):
    dados = service.filtrar_transacoes_categorias(categorias=categorias,filtro=filtro,usuario_id=usuario_atual)                                    
    return [ResponseTransacoes(**dict(d)) for d in dados ]
    
@router.get("/metricas", status_code=200,response_model= ResponseMetricas)
def exibir_metricas(service  : ServiceTransacoes = Depends(get_service_transacao), usuario_atual : int = Depends(get_usuario_atual)): 
    lista_categorias = service.categorias_e_valores_totais(usuario_atual) # lista com categorias e valores totais
    metrica = service.calcular_saldo_despesa(usuario_atual) # lista com saldo despesa e lucro
    return  ResponseMetricas(categoria_total=lista_categorias,metricas_= metrica)

@router.post("/new",status_code=201,response_model=ResponseTransacoes)
def criar_transacao (transacoes: CriarTransacoes, service  : ServiceTransacoes = Depends(get_service_transacao), usuario_atual : int = Depends(get_usuario_atual)):
    transacao_adicionada  = service.adicionar_transacoes(transacoes, usuario_atual)
    return dict(transacao_adicionada)

@router.get("/{id_}",  response_model=ResponseTransacoes)
def transacao_por_id (id_: int, service : ServiceTransacoes = Depends(get_service_transacao), usuario_atual : int = Depends(get_usuario_atual)):   
    return service.verificar_transacao_id(id_=id_,usuario_id=usuario_atual)


@router.delete("/{id_}", status_code = 204)
def deletar_transacoes (id_:int , service : ServiceTransacoes = Depends(get_service_transacao) , usuario_atual : int = Depends(get_usuario_atual)):
    id_confirmado = service.verificar_transacao_id(id_=id_,usuario_id=usuario_atual)
    service.remover_transacao(id_, usuario_atual)
    return 

    
@router.patch("/{id_}", status_code= 200, response_model= ResponseTransacoes)
def corrigir_transacao (id_:int, dados: CorrigirTransacoes , service : ServiceTransacoes = Depends(get_service_transacao) , usuario_atual : int = Depends(get_usuario_atual)):
    service.verificar_transacao_id(id_=id_, usuario_id=usuario_atual)
    retornar_transacao = service.corrigir_transacao(id_=id_, dados=dados,usuario_id=usuario_atual) 
    return retornar_transacao
