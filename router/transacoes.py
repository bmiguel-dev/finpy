from fastapi import  APIRouter, HTTPException, Depends,Query
from models.transacao import CriarTransacoes, CorrigirTransacoes, FiltrarTransacoes, ResponseTransacoes,ResponseMetricas,CategoriaTotal,Metricas
import sqlite3
from utils.seguranca import  validar_token_acess
from database.database import financeiro

router = APIRouter(prefix="/transacoes",tags=['Transações'])

@router.get("/")
def listar_transacoes (categorias : list[int] = Query(default=None,title="Categorias ID", alias="cat"),
                       filtro : FiltrarTransacoes = Depends(FiltrarTransacoes), conn : sqlite3.Connection = Depends(financeiro.conexao_bd), usuario_atual : int = Depends(validar_token_acess)):
    dados = financeiro.procurar_pelo_filtro(categorias=categorias,filtro=filtro,conn=conn, usuario_id=usuario_atual)                                                    #retorna o id do usuario
    return [ResponseTransacoes(**dict(d)) for d in dados ]
    
@router.get("/metricas", status_code=200,response_model= ResponseMetricas)
def exibir_metricas(conn : sqlite3.Connection = Depends(financeiro.conexao_bd), usuario_atual : int = Depends(validar_token_acess)):
    lista_categorias = [CategoriaTotal(**dict(d)) for d in financeiro.valores_totais_categorias(conn=conn, usuario_id=usuario_atual)]
    metrica = Metricas(**dict(financeiro.calculo_despesa_lucro(conn=conn, usuario_id=usuario_atual)))
    return  ResponseMetricas(categoria_total=lista_categorias,metricas_= metrica)

@router.post("/new",status_code=201,response_model=ResponseTransacoes)
def criar_transacao (transacoes: CriarTransacoes, conn : sqlite3.Connection = Depends(financeiro.conexao_bd), usuario_atual : int = Depends(validar_token_acess)):
    transacao_adicionada  = financeiro.adiciona_transacao(transacoes,conn, usuario_atual=usuario_atual)
    response_transacao = financeiro.procurar_pelo_id(transacao_adicionada,conn,usuario_atual)
    return dict(response_transacao)

@router.get("/{id_}",  response_model=ResponseTransacoes)
def transacao_por_id (id_: int, conn : sqlite3.Connection = Depends(financeiro.conexao_bd), usuario_atual : int = Depends(validar_token_acess)):   
    dados = financeiro.procurar_pelo_id(id_=id_, conn=conn, usuario_id=usuario_atual)
    if not dados:
        raise HTTPException(status_code=404, detail= "Transação não encontrada.")
    return dict(dados)


@router.delete("/{id_}", status_code = 204)
def deletar_transacoes (id_:int , conn : sqlite3.Connection = Depends(financeiro.conexao_bd), usuario_atual : int = Depends(validar_token_acess)):
        id_confirmado = financeiro.procurar_pelo_id(id_=id_, conn=conn, usuario_id=usuario_atual)
        if not id_confirmado:
            raise HTTPException(status_code=404, detail= "Transação não encontrada.")
        financeiro.remove_transacao(id_,conn, usuario_atual)
        return 
    
@router.patch("/{id_}", status_code= 200, response_model= ResponseTransacoes)
def corrigir_transacao (id_:int, dados: CorrigirTransacoes , conn : sqlite3.Connection = Depends(financeiro.conexao_bd), usuario_atual : int = Depends(validar_token_acess)):
        id_confirmado = financeiro.procurar_pelo_id(id_=id_,conn=conn, usuario_id=usuario_atual)
        if not id_confirmado:
            raise HTTPException(status_code=404, detail= "Transação não encontrada.")
        financeiro.corrige_transação(id_=id_, dados=dados,conn=conn, usuario_id=usuario_atual)
        id_return = financeiro.procurar_pelo_id(id_=id_,conn=conn, usuario_id=usuario_atual)
        return dict(id_return)
      