from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from database.database import financeiro
import sqlite3
from pydantic import ValidationError
from contextlib import asynccontextmanager
from router.usuarios import router as router_usuarios
from router.transacoes import router as router_transacoes


@asynccontextmanager
async def lifespan (app : FastAPI):
    financeiro.initiate_table()
    yield 

app = FastAPI(lifespan=lifespan)

@app.exception_handler(sqlite3.Error)
def erro_banco (requisicao : Request, erro : sqlite3.Error ):
    return JSONResponse(status_code=500, content= {"erro": str(erro) })

@app.exception_handler(ValidationError)
def erro_validation (requisicicao: Request, erro: ValidationError):
    return JSONResponse(status_code=422 , content={"erro": "Dados Inválidos", "detalhes": [{"campo": e["loc"][-1], "mensagem":e["msg"].replace("Value error, ", ""), "Enviado": e.get("input")} for e in erro.errors()]})

app.include_router(router=router_usuarios)
app.include_router(router=router_transacoes)


@app.get("/", tags = ['Health'])
def home ():
    return {"status_code": "Está rodando!"}


      

  