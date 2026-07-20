from fastapi import FastAPI, HTTPException, Request, Depends,Query
from fastapi.responses import JSONResponse
from services import Financeiro
from models.transacao import CriarTransacoes, CorrigirTransacoes, FiltrarTransacoes, ResponseTransacoes,ResponseMetricas,CategoriaTotal,Metricas
from database import conect_db
from typing import Optional
import sqlite3
from pydantic import ValidationError

app = FastAPI()

financeiro = Financeiro (conexão_banco= conect_db)
financeiro.iniciate_table()

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
                       filtro : FiltrarTransacoes = Depends(FiltrarTransacoes)):
    dados = financeiro.search_by_filter(categorias=categorias,filtro=filtro)
    return [ResponseTransacoes(**dict(d)) for d in dados ]
    
@app.get("/transacoes/metricas", status_code=200,response_model= ResponseMetricas)
def exibir_metricas():
    lista_categorias = [CategoriaTotal(**dict(d)) for d in financeiro.all_cat_values()]
    metrica = Metricas(**dict(financeiro.get_balance_and_expense()))
    return  ResponseMetricas(categoria_total=lista_categorias,metricas_= metrica)

@app.get("/transacoes/{id_}",  response_model=ResponseTransacoes)
def transacao_por_id (id_: int):   
    dados = financeiro.search_by_id(id_=id_)
    if not dados:
        raise HTTPException(status_code=404, detail= "Transação não encontrada.")
    return dict(dados)

@app.post("/transacoes/new",status_code=201,response_model=ResponseTransacoes)
def criar_transacao (transacoes: CriarTransacoes):
    transacao_adicionada  = financeiro.adict_transaction(transacoes)
    response_transacao = financeiro.search_by_id(transacao_adicionada)
    return dict(response_transacao)

@app.delete("/transacoes/{id_}", status_code = 204)
def deletar_transacoes (id_:int):
        id_confirmado = financeiro.search_by_id(id_=id_)
        if not id_confirmado:
            raise HTTPException(status_code=404, detail= "Transação não encontrada.")
        financeiro.remove_transaction(id_)
        return 
    
@app.patch("/transacoes/{id_}", status_code= 200, response_model= ResponseTransacoes)
def corrigir_transacao (id_:int, dados: CorrigirTransacoes):
        id_confirmado = financeiro.search_by_id(id_=id_)
        if not id_confirmado:
            raise HTTPException(status_code=404, detail= "Transação não encontrada.")
        financeiro.correct_transaction(id_=id_, dados=dados)
        id_return = financeiro.search_by_id(id_=id_)
        return dict(id_return)
      

  