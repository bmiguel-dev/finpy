from fastapi import FastAPI, Query,HTTPException, Response
from services import Financeiro
from utils import capturar_transacao, passar_financeiro_pro_json,date_isoformat
from models import Transacao
from pydantic import BaseModel,field_validator

from datetime import datetime,date
from typing import Optional
from database import *



financeiro = Financeiro (conexão_banco= conect_db)
app = FastAPI()
class ResponseTransacoes (BaseModel): 
    _id :int
    valor: float
    categoria: int
    descricao: str
    data: str

class CriarTransacoes (BaseModel):
    valor: float
    categoria_id: int
    descricao: str
    data: str

class CorrigirTransacoes (BaseModel):
    valor: float | None = None
    categoria: int | None = None
    descricao: str | None = None 
    data: str | None = None

class FiltrarTransacoes (BaseModel):
    categoria_filtro : list[int] | None = None
    d_inicio : str | None = None
    d_fim : str | None = None

@app.get("/")
def home ():
    return {"status_code": "Está rodando!"}

@app.get("/transacoes")
def transacoes ( filtro : FiltrarTransacoes = Query(None, title = "Filtro", 
                    description= " Schema para receber os dados e caso esses dados forem enviados, o filtro ocorra")) :
    
    
    if lista_transacoes:
        return passar_financeiro_pro_json(lista_transacoes)
    else:
        raise HTTPException(status_code=404, detail= "Transação não encontrada.")

@app.get("/transacoes/{id_}")
def transacao_por_id (id_:int):
    financeiro.carregar_arquivo()
    lista_transacoes = financeiro.buscar_transacao(id_) 
    if not lista_transacoes:
        raise HTTPException(status_code=404, detail= "Transação não encontrada.") 
    return passar_financeiro_pro_json([lista_transacoes])
    


@app.post("/transacoes/new",status_code=201)
def criar_transacao (transacoes: CriarTransacoes):
    try:
        date_obj = datetime.strptime(transacoes.data, "%d/%m/%Y").date()
        financeiro.adicionar_transacao(t)
        financeiro.salvar_arquivo()
        return {"mensage": "Transação criada com sucesso."}
    except:
        raise HTTPException(status_code=400, detail= "Entrada inválida.")

@app.delete("/transacoes/{id_}", status_code = 204)
def deletar_transacoes (id_:int):
    financeiro.carregar_arquivo()
    confirmacao = financeiro.remover_transacao(id_)
    if not confirmacao:
        raise HTTPException(status_code=404, detail= "Transação não encontrada.")
    financeiro.salvar_arquivo()
    return Response(status_code=204)
    
@app.patch("/transacoes/{id_}", status_code= 200)
def corrigir_transacao (id_:int, dados: CorrigirTransacoes):
    financeiro.carregar_arquivo()
    id_confirmada = financeiro.buscar_transacao(id_) #retorna uma transacao
    if not id_confirmada:
        raise HTTPException(status_code= 404, detail = "Transação não encontrada.")
    dados_dict = dados.model_dump(exclude_none=True)
    if 'data' in dados_dict:
        try:
            d1, _ = json_para_datetime(dados_dict["data"])
            dados_dict['data'] = d1
        except:
            raise HTTPException(status_code= 400, detail= "Formato da data errado, o esperado: DD/MM/YYYY")
    for atributo, valor in dados_dict.items():
        setattr(id_confirmada, atributo, valor )
    financeiro.salvar_arquivo()
    return {"message": "Transação corrigida com sucesso"}

