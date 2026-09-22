import os 
from dotenv import load_dotenv
import jwt
from datetime import timedelta, timezone, datetime
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from .erros import TokenSemIdentificacao, TokenInvalido


oauth2 = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

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

def validar_token_acess (token:str = Depends(oauth2) ) -> int:
    try:
        payload = jwt.decode(token,SECRET_KEY_ACESS, algorithms=[ALGORITMO])
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise TokenSemIdentificacao("Não há idenficação do usuário nesse token")
    except jwt.PyJWTError:
        raise TokenInvalido(" O Token é inválido ou foi expirado")
    return usuario_id
    

def validar_token_refresh (   token : str  = Depends(oauth2)) -> str:
    try:
        payload = jwt.decode(token,SECRET_KEY_REFRESH, algorithms=[ALGORITMO])
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise TokenSemIdentificacao("Não há identificação do usuário nesse token")
    except jwt.PyJWTError:
        raise TokenInvalido(" O Token é inválido ou foi expirado")
    return int(usuario_id)
    
    