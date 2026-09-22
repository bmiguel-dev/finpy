from fastapi import FastAPI
from database.database import database
from contextlib import asynccontextmanager
from router.usuarios import router as router_usuarios
from router.transacoes import router as router_transacoes
from utils.erros import TransacaoNaoEncontrada, EmailJaExiste,EmailNaoEncontrado,SenhaNaoCompativel
import sqlite3
from pydantic import ValidationError
from utils.exceptions_handler import *


@asynccontextmanager
async def lifespan (app : FastAPI):
    database.initiate_table()
    yield 

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(TransacaoNaoEncontrada,erro_transacao_nao_encontrada)
app.add_exception_handler(EmailNaoEncontrado,erro_email_nao_encontrado)
app.add_exception_handler(EmailJaExiste, erro_email_existe)
app.add_exception_handler(SenhaNaoCompativel,erro_senha_errada)
app.add_exception_handler(ValidationError, erro_validation)
app.add_exception_handler(sqlite3.Error, erro_banco)
app.add_exception_handler(TokenInvalido, erro_token_invalido)
app.add_exception_handler(TokenSemIdentificacao,  erro_token_sem_sub)


app.include_router(router=router_usuarios)
app.include_router(router=router_transacoes)


@app.get("/", tags = ['Health'])
def home ():
    return {"status_code": "Está rodando!"}


      

  