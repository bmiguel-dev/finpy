import pytest 
from fastapi.testclient import TestClient
from httpx import Response
import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import RealDictConnection
from typing import Generator
from database.database import DataBase
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL_TESTE")

@pytest.fixture(scope="function")
def bd_teste () -> Generator[RealDictConnection, None, None]:

    db = DataBase(link=DATABASE_URL)
    db.initiate_table()
    
    
    conn = psycopg2.connect(DATABASE_URL, connection_factory=RealDictConnection)
    
    try:
        yield conn
    finally:
        conn.rollback()
        conn.close()

#CLIENT (tem que retornar o yield com Test Client e overrider )

@pytest.fixture(scope="function")
def client(bd_teste):
    from database.database import database as db_fin  
    from main import app
    
    def override_bd():
        yield bd_teste

    app.dependency_overrides[db_fin.conexao_bd] = override_bd # *anotar no caderno* 


    with TestClient(app) as api:
        yield api 

    app.dependency_overrides.clear()

@pytest.fixture
def cadastro_breno (client : TestClient) -> dict:
    resposta_api_cadastro : Response = client.post("/usuarios/cadastro", json={"nome" : "Breno Miguel", "email" : "breno@teste.com", "senha" : "senha123"})
    return resposta_api_cadastro.json()

@pytest.fixture
def token_breno (client : TestClient , cadastro_breno ) -> str :
    resposta_api_login : Response = client.post("/usuarios/login", json= {"email" : "breno@teste.com", "senha" : "senha123"}) #aqui vai ter o token formato {{"token_access": token_access , "token_refresh": token_refresh, "type" : "bearer"}}
    r =   resposta_api_login.json()["token_access"]  # str token
    
    return {"Authorization": f"Bearer {r}"}  

@pytest.fixture
def criar_transacoes_breno (client : TestClient, token_breno ):
    resposta_api_t1 : Response  = client.post("/transacoes/new", json={"categoria_id": 1 , "valor" : 2000, "descricao" : "Salário Estágio" , "data" : "2026-08-10"}, headers=token_breno)
    return resposta_api_t1.json()

@pytest.fixture
def cadastro_ana (client : TestClient) -> dict:
    resposta_api_cadastro : Response = client.post("/usuarios/cadastro", json={"nome" : "Ana R", "email" : "anarodrigues08@gmail.com", "senha" : "senha321"})
    return resposta_api_cadastro.json()

@pytest.fixture
def token_ana (client : TestClient, cadastro_ana ) -> str :
    resposta_api_login : Response = client.post("/usuarios/login", json= {"email" : "anarodrigues08@gmail.com", "senha" : "senha321"})#aqui vai ter o token formato {{"token_access": token_access , "token_refresh": token_refresh, "type" : "bearer"}}
    r =   resposta_api_login.json()["token_access"]   # str token
    return {"Authorization": f"Bearer {r}"} 

