from fastapi import FastAPI, HTTPException, Request, Depends,Query
from fastapi.responses import JSONResponse
from services import Financeiro
from models.transacao import CriarTransacoes, CorrigirTransacoes, FiltrarTransacoes, ResponseTransacoes,ResponseMetricas,CategoriaTotal,Metricas
import sqlite3
from pydantic import ValidationError
from contextlib import asynccontextmanager
financeiro = Financeiro ()

print("DEBUG: aplication working! S2")
@asynccontextmanager
async def lifespan (app : FastAPI):
    print("DEBUG: lifespan working! S2")
    financeiro.iniciate_table()
    yield print("DEBUG: API RODANDO COM LIFESPAN")

app = FastAPI(lifespan=lifespan)

@app.exception_handler(sqlite3.Error)
def erro_banco (requisicao : Request, erro : sqlite3.Error ):
    return JSONResponse(status_code=500, content= {"erro": str(erro) })

@app.exception_handler(ValidationError)
def erro_validation (requisicicao: Request, erro: ValidationError):
    return JSONResponse(status_code=422 , content={"erro": "Dados Inválidos", "detalhes": [{"campo": e["loc"][-1], "mensagem":e["msg"].replace("Value error, ", ""), "Enviado": e.get("input")} for e in erro.errors()]})

def categorias_validadas(lct:list[int] | None):
    if lct is None:
        return lct
    for x in lct:
        if x <= 0:
            raise ValueError("o ID da categoria não pode ser 0 nem negativo.")
    return lct

@app.get("/")
def home ():
    return {"status_code": "Está rodando!"}

@app.get("/transacoes")
def listar_transacoes (categorias : list[int] = Query(default=None,title="Categorias ID", alias="cat"),
                       filtro : FiltrarTransacoes = Depends(FiltrarTransacoes), conn : sqlite3.Connection = Depends(financeiro.conect_db)):
    dados = financeiro.search_by_filter(categorias=categorias,filtro=filtro,conn=conn)
    return [ResponseTransacoes(**dict(d)) for d in dados ]
    
@app.get("/transacoes/metricas", status_code=200,response_model= ResponseMetricas)
def exibir_metricas(conn : sqlite3.Connection = Depends(financeiro.conect_db)):
    lista_categorias = [CategoriaTotal(**dict(d)) for d in financeiro.all_cat_values(conn=conn)]
    metrica = Metricas(**dict(financeiro.get_balance_and_expense(conn=conn)))
    return  ResponseMetricas(categoria_total=lista_categorias,metricas_= metrica)

@app.get("/transacoes/{id_}",  response_model=ResponseTransacoes)
def transacao_por_id (id_: int, conn : sqlite3.Connection = Depends(financeiro.conect_db)):   
    dados = financeiro.search_by_id(id_=id_, conn=conn)
    if not dados:
        raise HTTPException(status_code=404, detail= "Transação não encontrada.")
    return dict(dados)

@app.post("/transacoes/new",status_code=201,response_model=ResponseTransacoes)
def criar_transacao (transacoes: CriarTransacoes, conn : sqlite3.Connection = Depends(financeiro.conect_db)):
    transacao_adicionada  = financeiro.adict_transaction(transacoes,conn)
    response_transacao = financeiro.search_by_id(transacao_adicionada,conn)
    return dict(response_transacao)

@app.delete("/transacoes/{id_}", status_code = 204)
def deletar_transacoes (id_:int , conn : sqlite3.Connection = Depends(financeiro.conect_db)):
        id_confirmado = financeiro.search_by_id(id_=id_, conn=conn)
        if not id_confirmado:
            raise HTTPException(status_code=404, detail= "Transação não encontrada.")
        financeiro.remove_transaction(id_,conn)
        return 
    
@app.patch("/transacoes/{id_}", status_code= 200, response_model= ResponseTransacoes)
def corrigir_transacao (id_:int, dados: CorrigirTransacoes , conn : sqlite3.Connection = Depends(financeiro.conect_db)):
        id_confirmado = financeiro.search_by_id(id_=id_,conn=conn)
        if not id_confirmado:
            raise HTTPException(status_code=404, detail= "Transação não encontrada.")
        financeiro.correct_transaction(id_=id_, dados=dados,conn=conn)
        id_return = financeiro.search_by_id(id_=id_,conn=conn)
        return dict(id_return)
      

  