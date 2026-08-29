from fastapi.testclient import TestClient

class TestIsolamento:
    """
    Garante que um usuário nunca acessa dados de outro.
    Esses testes são os mais críticos de segurança.
    """

    def test_listar_so_proprias_transacoes(self, client : TestClient, token_breno, token_ana):
        # Breno cria transação
        client.post("/transacoes/new", headers=token_breno, json={
            "valor": 1000.0, "categoria_id": 1,
            "descricao": "Transação do Breno", "data": "2026-07-01"
        })
        # Ana cria transação
        client.post("/transacoes/new", headers=token_ana, json={
            "valor": 500.0, "categoria_id": 1,
            "descricao": "Transação da Ana", "data": "2026-07-01"
        })

        transacoes_breno = client.get("/transacoes/", headers=token_breno).json()
        transacoes_ana   = client.get("/transacoes/", headers=token_ana).json()

        assert len(transacoes_breno) == 1
        assert len(transacoes_ana) == 1
        assert transacoes_breno[0]["descricao"] == "Transação do Breno"
        assert transacoes_ana[0]["descricao"] == "Transação da Ana"

    def test_nao_acessa_transacao_alheia_por_id(self, client : TestClient , token_breno, token_ana):
        r = client.post("/transacoes/new", headers=token_breno, json={
            "valor": 1000.0, "categoria_id": 1,
            "descricao": "Só do Breno", "data": "2026-07-01"
        })
        id_breno = r.json()["id"]

        # Ana tenta acessar transação do breno
        assert client.get(f"/transacoes/{id_breno}", headers=token_ana).status_code == 404

    def test_nao_edita_transacao_alheia(self, client : TestClient, token_breno, token_ana):
        r = client.post("/transacoes/new", headers=token_breno, json={
            "valor": 1000.0, "categoria_id": 1,
            "descricao": "Só do Breno", "data": "2026-07-01"
        })
        id_breno = r.json()["id"]

        assert client.patch(
            f"/transacoes/{id_breno}", headers=token_ana,
            json={"descricao": "Tentativa de invasão"}
        ).status_code == 404

    def test_nao_deleta_transacao_alheia(self, client : TestClient , token_breno, token_ana):
        r = client.post("/transacoes/new", headers=token_breno, json={
            "valor": 1000.0, "categoria_id": 1,
            "descricao": "Só do Breno", "data": "2026-07-01"
        })
        id_breno = r.json()["id"]

        assert client.delete(f"/transacoes/{id_breno}", headers=token_ana).status_code == 404
        # confirma que ainda existe pro Breno
        assert client.get(f"/transacoes/{id_breno}", headers=token_breno).status_code == 200

    def test_metricas_isoladas(self, client : TestClient , token_breno, token_ana):
        client.post("/transacoes/new", headers=token_breno, json={
            "valor": 5000.0, "categoria_id": 1,
            "descricao": "Salário Breno", "data": "2026-07-01"
        })
        client.post("/transacoes/new", headers=token_ana, json={
            "valor": 1000.0, "categoria_id": 1,
            "descricao": "Salário Ana", "data": "2026-07-01"
        })

        m_breno = client.get("/transacoes/metricas", headers=token_breno).json()["metricas_"]
        m_ana   = client.get("/transacoes/metricas", headers=token_ana).json()["metricas_"]

        assert m_breno["saldo_total"] == 5000.0
        assert m_ana["saldo_total"] == 1000.0