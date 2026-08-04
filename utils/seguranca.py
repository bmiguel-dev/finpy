import os 
from dotenv import load_dotenv
import jwt
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException, Depends
from services.financeiro import Financeiro
import sqlite3
from fastapi.security import OAuth2PasswordBearer
from database.database import financeiro

oauth2 = OAuth2PasswordBearer(tokenUrl="/login")

# token de acesso

load_dotenv()

ALGORITMO = "HS256"

SECRET_KEY_ACESS = os.getenv("SECRET_KEY_ACESS")
SECRET_KEY_REFRESH = os.getenv("SECRET_KEY_REFRESH")
VALIDADE_TOKEN_REFRESH = 7 
VALIDADE_TOKEN_ACESS = 15

def gerar_token_acess (dados:dict) -> str:
    dados_c = dados.copy()
    validade = datetime.now(timezone.utc) + timedelta(minutes=VALIDADE_TOKEN_ACESS)
    dados_c.update({'exp': validade , 'type' : 'access'})
    token_gerado = jwt.encode(dados_c, SECRET_KEY_ACESS, algorithm= ALGORITMO)
    return token_gerado

def gerar_token_refresh (dados:dict) -> str:
    dados_c = dados.copy()
    validade = datetime.now(timezone.utc) + timedelta(days=VALIDADE_TOKEN_REFRESH)
    dados_c.update({'exp': validade , 'type' : 'refresh'})
    token_gerado = jwt.encode(dados_c, SECRET_KEY_REFRESH, algorithm= ALGORITMO)
    return token_gerado

def validar_token_acess (token:str = Depends(oauth2), conn : sqlite3.Connection = Depends(financeiro.conect_db)) -> int:
    try:
        payload = jwt.decode(token,SECRET_KEY_ACESS, algorithms=[ALGORITMO])
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise HTTPException(status_code=401,detail="Não há idenficação do usuário nesse token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail= " O Token é inválido ou foi expirado")
    usuario_id = int(usuario_id)
    dados = financeiro.search_user_by_id(id_=usuario_id, conn= conn)
    if dados is None:
        raise HTTPException(status_code=404, detail= "Este usuário não existe mais.")
    return usuario_id

def validar_token_refresh (token : str , financeiro : Financeiro, conn :sqlite3.Connection) -> str:
    try:
        payload = jwt.decode(token,SECRET_KEY_REFRESH, algorithms=[ALGORITMO])
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise HTTPException(status_code=401,detail="Não há identificação do usuário nesse token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail= " O Token é inválido ou foi expirado")
    usuario_id = int(usuario_id)
    dados = financeiro.search_by_id(id_=usuario_id, conn=conn)
    if dados is None:
        raise HTTPException(status_code=404, detail= "Este usuário não existe mais.")
    token = gerar_token_acess({"sub":str(usuario_id)})
    return token
    