from fastapi import FastAPI
from services import Financeiro
from utils import capturar_transacao, passar_financeiro_pro_json
from models import Transacao
from pydantic import BaseModel
from datetime import datetime
financeiro = Financeiro ()
app = FastAPI()

class Transacoes(BaseModel):
    valor: float
    categoria: int
    descricao: str
    data: str

@app.get("/")
def home ():
    return {"status_code": "Está rodando!"}

@app.get("/transacoes")
def transacoes ():
    lista_transacao = passar_financeiro_pro_json(financeiro.lista_transacao)
    return lista_transacao

@app.post("/transacoes")
def criar_transacao (transacao: Transacoes):
    data_obj = datetime.strptime(transacao.data, "%d/%m/%Y").date()
    t = Transacao(descricao=transacao.descricao, valor=transacao.valor, data=data_obj)
    t.categoria = transacao.categoria 
    financeiro.adicionar_transacao(t)
    return {"status_code": "Transação criada com sucesso!"}
