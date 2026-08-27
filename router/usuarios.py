from fastapi import  APIRouter, HTTPException,  Depends
from models.usuarios import UsuarioCadastro, UsuarioLogin, UsuarioResponse
from models.token import RefreshToken, ResponseRefresh,ResponseLogin
import sqlite3
from utils.seguranca import  validar_token_refresh, gerar_token_acess,gerar_token_refresh
from database.database import financeiro


router = APIRouter(prefix="/usuarios", tags= ["Usuários"])



@router.post("/cadastro", status_code=201, response_model=UsuarioResponse)
def cadastro ( dados : UsuarioCadastro, conn : sqlite3.Connection = Depends(financeiro.conexao_bd)):
    email_existente = financeiro.procurar_usuario_pelo_email(dados=dados, conn=conn)
    if email_existente:
        raise HTTPException(status_code=409, detail= "Email já cadastrado.")
    usuario_cadastrado = financeiro.cria_usuario(entrada_dado=dados, conn=conn)
    retorno_usuario = financeiro.procurar_usuario_pelo_id(usuario_cadastrado, conn)
    return dict(retorno_usuario)

@router.post("/login", response_model= ResponseLogin, status_code=200)
def login (dados : UsuarioLogin, conn : sqlite3.Connection = Depends(financeiro.conexao_bd) ) -> dict:
    usuario_id  = financeiro.validacao_usuario(dados, conn)
    if not usuario_id:
        raise HTTPException(status_code=401, detail= "Os dados não coincidem com nenhuma conta do banco.") 
    token_access = gerar_token_acess({'sub' : str(usuario_id)})
    token_refresh = gerar_token_refresh({'sub': str(usuario_id)})
    return {"token_access": token_access,
            "token_refresh":token_refresh,
            "type" : "bearer"}

@router.post("/refresh", response_model= ResponseRefresh, status_code=200)
def refresh (token : RefreshToken, conn : sqlite3.Connection = Depends(financeiro.conexao_bd)):
    token_novo = validar_token_refresh(financeiro, conn,token.refresh_token)
    return {"token_access": token_novo,
            "type" : "bearer"}

  