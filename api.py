from fastapi import FastAPI, Query
from services import Financeiro
from utils import capturar_transacao, passar_financeiro_pro_json,json_para_datetime
from models import Transacao
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
financeiro = Financeiro ()
app = FastAPI()

class Transacoes (BaseModel):
    valor: float
    categoria: int
    descricao: str
    data: str

@app.get("/")
def home ():
    return {"status_code": "Está rodando!"}

@app.get("/transacoes")
def transacoes ( categoria : Optional[list[int]] = Query(None,alias= "cat", title = "categoria", description = "Passa os números das categorias para filtrar, apenas números", example = [1,3,4]) ,data_1 : Optional[str] = None, data_2:Optional[str] = None):
    d1, d2 = json_para_datetime(data_1,data_2)
    financeiro.carregar_arquivo()
    lista_transacoes = financeiro.lista_filtro_api(categoria,d1,d2)
    if lista_transacoes:
        return passar_financeiro_pro_json(lista_transacoes)
    else:
        return {"mensage" : "Não achou a transação com essas características."}

@app.get("/transacoes/{id_}")
def transacoes (id_:str):
    financeiro.carregar_arquivo()
    lista_transacoes = financeiro.procurar_id(int(id_)) 
    if lista_transacoes:
        return passar_financeiro_pro_json([lista_transacoes])
    else:
        return {"mensage" : "Não achou a transacão com esse ID."}


@app.post("/transacoes/new")
def criar_transacao (transacoes: Transacoes):
    date_obj = datetime.strptime(transacoes.data, "%d/%m/%Y").date()
    t = Transacao(descricao=transacoes.descricao, valor=transacoes.valor, data=date_obj)
    t.categoria = transacoes.categoria
    financeiro.adicionar_transacao(t)
    financeiro.salvar_arquivo()
    return {"status_code": "Transação criada com sucesso!"}

@app.delete("/transacoes/{id_}")
def deletar_transacoes (id_:str):
    financeiro.carregar_arquivo()
    confirmacao = financeiro.remover_transacao(int(id_))
    if confirmacao:
        financeiro.salvar_arquivo()
        return {"mensage" : "Transação removida."}
    else:
        return {"mensage" : "Não achou a transacão com esse ID."}



