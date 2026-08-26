from fastapi import  APIRouter, HTTPException,  Depends
from models.usuarios import UsuarioCadastro, UsuarioLogin
from models.token import RefreshToken, ResponseRefresh,ResponseLogin
import sqlite3
from utils.seguranca import  validar_token_refresh, gerar_token_acess,gerar_token_refresh
from database.database import financeiro


router = APIRouter(prefix="/usuarios", tags= ["Usuários"])



@router.post("/cadastro", status_code=201)
def cadastro ( dados : UsuarioCadastro, conn : sqlite3.Connection = Depends(financeiro.conect_db)):
    email_existente = financeiro.search_user_by_email(dados=dados, conn=conn)
    if email_existente:
        raise HTTPException(status_code=409, detail= "Email já cadastrado.")
    usuario_cadastrado = financeiro.create_user(entrada_dado=dados, conn=conn)
    retorno_usuario = financeiro.search_user_by_id(usuario_cadastrado, conn)
    return dict(retorno_usuario)

@router.post("/login", response_model= ResponseLogin, status_code=200)
def login (dados : UsuarioLogin, conn : sqlite3.Connection = Depends(financeiro.conect_db) ) -> dict:
    usuario_id  = financeiro.user_validation(dados, conn)
    if not usuario_id:
        raise HTTPException(status_code=401, detail= "Os dados não coincidem com nenhuma conta do banco.") 
    token_access = gerar_token_acess({'sub' : str(usuario_id)})
    token_refresh = gerar_token_refresh({'sub': str(usuario_id)})
    return {"token_access": token_access,
            "token_refresh":token_refresh,
            "type" : "bearer"}

@router.post("/refresh", response_model= ResponseRefresh, status_code=200)
def refresh (token : RefreshToken, conn : sqlite3.Connection = Depends(financeiro.conect_db)):
    token_novo = validar_token_refresh(financeiro, conn,token.refresh_token)
    return {"token_access": token_novo,
            "type" : "bearer"}

  