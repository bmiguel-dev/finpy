from fastapi.testclient import TestClient
from httpx import Response

class TestCadastro:

    def test_cadastro_sucesso(self, client : TestClient):
        r = client.post("/usuarios/cadastro", json={
            "nome": "Breno Miguel",
            "email": "breno@teste.com",
            "senha": "senha123"
        })
        print(r.json())
        assert r.status_code == 201
        assert r.json()["nome"] == "Breno Miguel"
        assert r.json()["email"] == "breno@teste.com"
        

    def test_cadastro_email_duplicado(self, client : TestClient, cadastro_breno):
        r = client.post("/usuarios/cadastro", json={
            "nome": "Outro Nome",
            "email": "breno@teste.com",   # mesmo email
            "senha": "outrasenha"
        })
        assert r.status_code == 409

    def test_cadastro_nome_curto(self, client : TestClient):
        r = client.post("/usuarios/cadastro", json={
            "nome": "AB",
            "email": "ab@teste.com",
            "senha": "senha123"
        })
        assert r.status_code == 422

    def test_cadastro_email_invalido(self, client : TestClient):
        r = client.post("/usuarios/cadastro", json={
            "nome": "Teste Ok",
            "email": "isso-nao-e-email",
            "senha": "senha123"
        })
        assert r.status_code == 422

    def test_cadastro_senha_curta(self, client : TestClient):
        r = client.post("/usuarios/cadastro", json={
            "nome": "Teste Ok",
            "email": "ok@teste.com",
            "senha": "abc"
        })
        assert r.status_code == 422


class TestLogin:

    def test_login_sucesso(self, client : TestClient, cadastro_breno):
        r = client.post("/usuarios/login", json={
            "email": "breno@teste.com",
            "senha": "senha123"
        })
        assert r.status_code == 200
        assert "token_access" in r.json()
        assert "token_refresh" in r.json()
        assert r.json()["type"] == "bearer"

    def test_login_senha_errada(self, client : TestClient, cadastro_breno):
        r = client.post("/usuarios/login", json={
            "email": "breno@teste.com",
            "senha": "senhaerrada"
        })
        assert r.status_code == 401

    def test_login_email_inexistente(self, client : TestClient):
        r = client.post("/usuarios/login", json={
            "email": "naoexiste@teste.com",
            "senha": "senha123"
        })
        assert r.status_code == 401


class TestRefresh:

    def test_refresh_sucesso(self, client : TestClient, cadastro_breno):
        r_login = client.post("/usuarios/login", json={
            "email": "breno@teste.com",
            "senha": "senha123"
        })
        refresh_token = r_login.json()["token_refresh"]

        r = client.post("/usuarios/refresh", json={
            "refresh_token": refresh_token
        })
        assert r.status_code == 200
        assert "token_access" in r.json()

    def test_refresh_token_invalido(self, client : TestClient):
        r = client.post("/usuarios/refresh", json={
            "refresh_token": "token.invalido.aqui"
        })
        assert r.status_code == 401