from fastapi.testclient import TestClient
from httpx import Response
class TestCriar: 
    def test_criar_transacao_breno(self,client : TestClient, token_breno : dict ):
        r : Response = client.post("/transacoes/new",  json={"categoria_id": 1 , "valor" : 2000, "descricao" : "Salário Estágio" , "data" : "10/08/2026"},
                     headers= {"Authorization": f"Bearer {token_breno['token_access']}"})
        #return = json com id :int valor: float categoria_id: int descricao: str data: str(ResponseTransacoes)
        assert r.status_code == 201
        assert "id" in r.json()
        assert r.json()["valor"] == 2000

    def test_criar_transacao_ana(self,client : TestClient, token_ana : dict ):
            r : Response = client.post("/transacoes/new", json={"categoria_id": 1 , "valor" : 400, "descricao" : "mesada" , "data" : "12/08/2026"},
                                       headers={"Authorization": f"Bearer {token_ana['token_access']}"})
            
            assert r.status_code == 201
            assert "id" in r.json()
            assert r.json()["valor"] == 400


    def test_criar_valor_negativo(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers={"Authorization": f"Bearer {token_breno['token_access']}"}, json={
            "valor": -100, "categoria_id": 1,
            "descricao": "Inválido", "data": "2026-07-01"
        })
        assert r.status_code == 422

    def test_criar_valor_zero(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers={"Authorization": f"Bearer {token_breno['token_access']}"}, json={
            "valor": 0, "categoria_id": 1,
            "descricao": "Zero", "data": "2026-07-01"
        })
        assert r.status_code == 422

    def test_criar_data_futura(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers={"Authorization": f"Bearer {token_breno['token_access']}"}, json={
            "valor": 100, "categoria_id": 1,
            "descricao": "Futura", "data": "2099-01-01"
        })
        assert r.status_code == 422

    def test_criar_descricao_vazia(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers={"Authorization": f"Bearer {token_breno['token_access']}"}, json={
            "valor": 100, "categoria_id": 1,
            "descricao": "   ", "data": "2026-07-01"
        })
        assert r.status_code == 422

    def test_criar_data_formato_errado(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers={"Authorization": f"Bearer {token_breno['token_access']}"}, json={
            "valor": 100, "categoria_id": 1,
            "descricao": "Teste", "data": "15/07/2026"
        })
        assert r.status_code == 422


class TestListar:

    def test_listar_retorna_lista(self, client : TestClient, token_breno):
        r : Response = client.get("/transacoes/", headers={"Authorization": f"Bearer {token_breno['token_access']}"})
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_listar_vazio(self, client : TestClient , token_breno):
        r : Response = client.get("/transacoes/", headers={"Authorization": f"Bearer {token_breno['token_access']}"})
        assert r.status_code == 200
        assert len(r.json()) == 0

    def test_filtro_data_inicio(self,client : TestClient, token_breno, criar_transacoes_breno):
        r : Response = client.get("/transacoes/?d_inicio=2026-07-01", headers={"Authorization": f"Bearer {token_breno['token_access']}"})
        assert r.status_code == 200

    def test_filtro_data_fim(self, client : TestClient, token_breno, criar_transacoes_breno):
        r: Response  = client.get("/transacoes/?d_fim=2026-07-31", headers={"Authorization": f"Bearer {token_breno['token_access']}"})
        assert r.status_code == 200

    def test_filtro_intervalo_datas(self, client : TestClient, token_breno, criar_transacoes_breno):
        r: Response  = client.get("/transacoes/?d_inicio=2026-07-01&d_fim=2026-07-31",
                       headers={"Authorization": f"Bearer {token_breno['token_access']}"})
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_filtro_categoria(self, client : TestClient, token_breno, criar_transacoes_breno):
        r : Response  = client.get("/transacoes/?cat=1", headers={"Authorization": f"Bearer {token_breno['token_access']}"})
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_filtro_data_invalida(self, client : TestClient, token_breno):
        r : Response = client.get("/transacoes/?d_inicio=data-errada", headers={"Authorization": f"Bearer {token_breno['token_access']}"})
        assert r.status_code == 422       
        
#deletar
#corrigir
#métricas
#mostrar
#buscar por id
