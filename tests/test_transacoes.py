from fastapi.testclient import TestClient
from httpx import Response

class TestCriar: 
    def test_criar_transacao_breno(self,client : TestClient, token_breno : str):
        r : Response = client.post("/transacoes/new",  json={"categoria_id": 1 , "valor" : 2000, "descricao" : "Salário Estágio" , "data" : "2026-08-10"},
                     headers=token_breno)
        #return = json com id :int valor: float categoria_id: int descricao: str data: str(ResponseTransacoes)
        assert r.status_code == 201
        assert "id" in r.json()
        assert r.json()["valor"] == 2000

    def test_criar_transacao_ana(self,client : TestClient, token_ana : str):
            r : Response = client.post("/transacoes/new", json={"valor" : 400, "categoria_id": 1 , "descricao" : "mesada" , "data" : "2026-08-12"},
                                       headers=token_ana)
            
            assert r.status_code == 201
            assert "id" in r.json()
            assert r.json()["valor"] == 400


    def test_criar_valor_negativo(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers=token_breno, json={
            "valor": -100, "categoria_id": 1,
            "descricao": "Inválido", "data": "2026-07-01"
        })
        assert r.status_code == 422

    def test_criar_valor_zero(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers=token_breno, json={
            "valor": 0, "categoria_id": 1,
            "descricao": "Zero", "data": "2026-07-01"
        })
        assert r.status_code == 422

    def test_criar_data_futura(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers=token_breno, json={
            "valor": 100, "categoria_id": 1,
            "descricao": "Futura", "data": "2099-01-01"
        })
        assert r.status_code == 422

    def test_criar_descricao_vazia(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers=token_breno, json={
            "valor": 100, "categoria_id": 1,
            "descricao": "   ", "data": "2026-07-01"
        })
        assert r.status_code == 422

    def test_criar_data_formato_errado(self, client : TestClient, token_breno):
        r : Response = client.post("/transacoes/new", headers=token_breno, json={
            "valor": 100, "categoria_id": 1,
            "descricao": "Teste", "data": "15/07/2026"
        })
        assert r.status_code == 422


class TestListar:

    def test_listar_retorna_lista(self, client : TestClient, token_breno):
        r : Response = client.get("/transacoes/", headers=token_breno)
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_listar_vazio(self, client : TestClient , token_breno):
        r : Response = client.get("/transacoes/", headers=token_breno)
        assert r.status_code == 200
        assert len(r.json()) == 0

    def test_filtro_data_inicio(self,client : TestClient, token_breno, criar_transacoes_breno):
        r : Response = client.get("/transacoes/?d_inicio=2026-07-01", headers=token_breno)
        assert r.status_code == 200
        

    def test_filtro_data_fim(self, client : TestClient, token_breno, criar_transacoes_breno):
        r: Response  = client.get("/transacoes/?d_fim=2026-07-31", headers=token_breno)
        assert r.status_code == 200
        

    def test_filtro_intervalo_datas(self, client : TestClient, token_breno, criar_transacoes_breno):
        r: Response  = client.get("/transacoes/?d_inicio=2026-07-01&d_fim=2026-08-28",
                       headers=token_breno)
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_filtro_categoria(self, client : TestClient, token_breno, criar_transacoes_breno):
        r : Response  = client.get("/transacoes/?cat=1", headers=token_breno)
        assert r.status_code == 200
        assert len(r.json()) == 1

    def test_filtro_data_invalida(self, client : TestClient, token_breno, criar_transacoes_breno):
        r : Response = client.get("/transacoes/?d_inicio=data-errada", headers=token_breno)
        assert r.status_code == 422       
        
#deletar
class TestDeletar:

    def test_delete_sucesso(self, client : TestClient, token_breno, criar_transacoes_breno):
        id_ = criar_transacoes_breno["id"]
        assert client.delete(f"/transacoes/{id_}", headers=token_breno).status_code == 204
        assert client.get(f"/transacoes/{id_}", headers=token_breno).status_code == 404

    def test_delete_inexistente(self, client:TestClient, token_breno):
        assert client.delete("/transacoes/99999", headers=token_breno).status_code == 404


#corrigir
class TestCorrigir:

    def test_patch_descricao(self, client : TestClient, token_breno,criar_transacoes_breno):
        id_ = criar_transacoes_breno["id"]
        r = client.patch(f"/transacoes/{id_}", headers=token_breno, json={
            "descricao": "Descrição atualizada"
        })
        assert r.status_code == 200
        assert r.json()["descricao"] == "Descrição atualizada"

    def test_patch_valor(self, client : TestClient, token_breno, criar_transacoes_breno):
        id_ = criar_transacoes_breno["id"]
        r = client.patch(f"/transacoes/{id_}", headers=token_breno, json={
            "valor": 9999.0
        })
        assert r.status_code == 200
        assert r.json()["valor"] == 9999.0

    def test_patch_inexistente(self, client : TestClient, token_breno):
        r = client.patch("/transacoes/99999", headers=token_breno, json={
            "descricao": "Não existe"
        })
        assert r.status_code == 404

    def test_patch_valor_negativo(self, client : TestClient , token_breno,criar_transacoes_breno):
        id_ = criar_transacoes_breno["id"]
        r = client.patch(f"/transacoes/{id_}", headers=token_breno, json={
            "valor": -50
        })
        assert r.status_code == 422
#métricas
class TestMetricas:

    def test_metricas_retorna_estrutura(self, client:TestClient, token_breno):
        r = client.get("/transacoes/metricas", headers=token_breno)
        assert r.status_code == 200
        assert "categoria_total" in r.json()
        assert "metricas_" in r.json()

    def test_metricas_calculo_correto(self, client : TestClient, token_breno):
        # receita
        client.post("/transacoes/new", headers=token_breno, json={
            "valor": 3000.0, "categoria_id": 1,
            "descricao": "Salário", "data": "2026-07-01"
        })
        # despesa
        client.post("/transacoes/new", headers=token_breno, json={
            "valor": 500.0, "categoria_id": 5,
            "descricao": "Lazer", "data": "2026-07-10"
        })

        r = client.get("/transacoes/metricas", headers=token_breno)
        m = r.json()["metricas_"]

        assert m["saldo_total"] == 3000.0
        assert m["despesa_total"] == 500.0
        assert m["total_liquido"] == 2500.0

