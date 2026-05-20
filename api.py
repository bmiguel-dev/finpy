from fastapi import FastAPI
from services import Financeiro
from utils import passar_financeiro_pro_json

app = FastAPI()
financeiro = Financeiro ()

@app.get("/")
def home ():
    return {"status_code": "Está rodando!"}

@app.get("/transacoes")
def transacoes ():
    lista_transacao = passar_financeiro_pro_json()
    return lista_transacao

