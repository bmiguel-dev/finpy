from fastapi import FastAPI, Query
from services import Financeiro
from utils import capturar_transacao, passar_financeiro_pro_json
from models import Transacao
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
financeiro = Financeiro ()
app = FastAPI()

class Transactions (BaseModel):
    value: float
    category: int
    description: str
    date: str

@app.get("/")
def home ():
    return {"status_code": "Está rodando!"}

@app.get("/transactions")
def transactions ( category : Optional[list[int]] = Query(None,alias= "cat", title = "categoria", description = "Passa os números das categorias para filtrar, apenas números", example = [1,3,4]) ,date_1 : Optional[str] = None, date_2:Optional[str] = None):
    d1 = datetime.strptime(date_1, "%d/%m/%Y").date() if date_1 else None
    d2 = datetime.strptime(date_2, "%d/%m/%Y").date() if date_2 else None
    financeiro.carregar_arquivo()
    list = financeiro.lista_filtro_api(category,d1,d2)
    if list:
        return passar_financeiro_pro_json(list)
    else:
        return {"mensage" : "deu ruim"}
    


@app.post("/transactions/new")
def create_transactions (transaction: Transactions):
    date_obj = datetime.strptime(transaction.date, "%d/%m/%Y").date()
    t = Transacao(descricao=transaction.description, valor=transaction.value, data=date_obj)
    t.categoria = transaction.category 
    financeiro.adicionar_transacao(t)
    financeiro.salvar_arquivo()
    return {"status_code": "Transação criada com sucesso!"}




