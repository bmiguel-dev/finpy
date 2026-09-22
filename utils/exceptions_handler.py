import sqlite3
from fastapi import Request, status
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from utils.erros import *

def erro_banco (requisicao : Request, erro : sqlite3.Error ):#500
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content= {"erro": str(erro) })


def erro_validation (requisicicao: Request, erro: ValidationError):#422
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT , content={"erro": "Dados Inválidos", "detalhes": [{"campo": e["loc"][-1], "mensagem":e["msg"].replace("Value error, ", ""), "Enviado": e.get("input")} for e in erro.errors()]})

def erro_transacao_nao_encontrada(requisicicao: Request, erro: TransacaoNaoEncontrada):#404
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND , content={"erro":str(erro)})


def erro_email_existe (requisicao : Request, erro : EmailJaExiste): # 400
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content= {"erro": str(erro) })


def erro_email_nao_encontrado(requisicao : Request, erro : EmailNaoEncontrado ): #404
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content= {"erro": str(erro) })


def erro_senha_errada (requisicao : Request, erro : SenhaNaoCompativel ):#400
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content= {"erro": str(erro) })

def erro_token_invalido ( requisicao : Request , erro : TokenInvalido): #401
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content= {"erro": str(erro) })

def erro_token_sem_sub (requisicao : Request, erro: TokenSemIdentificacao):#401
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content= {"erro": str(erro) })
