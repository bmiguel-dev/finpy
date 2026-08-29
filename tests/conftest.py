import pytest 
import sqlite3 
from fastapi.testclient import TestClient
from httpx import Response

@pytest.fixture(scope="function")
def bd_teste ():
    from enums import Categoria
    conn = sqlite3.connect(":memory:",check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.executescript(''' CREATE TABLE IF NOT EXISTS usuarios (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                          nome TEXT UNIQUE NOT NULL,
                                                                          email TEXT UNIQUE NOT NULL,
                                                                          senha TEXT NOT NULL,
                                                                          criacao_login DATETIME DEFAULT CURRENT_TIMESTAMP);

                            CREATE TABLE IF NOT EXISTS categorias (id INTEGER NOT NULL PRIMARY KEY,
                                                                        nome TEXT NOT NULL UNIQUE, tipo INTEGER NOT NULL);


                            CREATE TABLE IF NOT EXISTS transacoes (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                                                        user_id INTEGER,
                                                                        categoria_id INTEGER,
                                                                        valor REAL NOT NULL,
                                                                        descricao TEXT NOT NULL,
                                                                        data DATE NOT NULL,
                                                        FOREIGN KEY (categoria_id) REFERENCES categorias(id),
                                                        FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE);

                                                        CREATE INDEX IF NOT EXISTS idx_transacoes_categoria_id ON transacoes(categoria_id);

                                                        CREATE INDEX IF NOT EXISTS idx_transacoes_data ON transacoes(data);

                                                        CREATE INDEX IF NOT EXISTS idx_transacoes_user_id ON transacoes(user_id)''')
    
    cursor.executemany('''INSERT OR IGNORE INTO categorias (id, nome, tipo) VALUES (?,?,?)''', Categoria.lista_categorias())
    conn.commit()
    try:
        yield conn
    finally:
        conn.close()

#CLIENT (tem que retornar o yield com Test Client e overrider )

@pytest.fixture(scope="function")
def client(bd_teste):
    from database.database import financeiro as db_fin
    from main import app
    
    def override_bd():
        yield bd_teste

    app.dependency_overrides[db_fin.conexao_bd] = override_bd


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

