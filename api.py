from fastapi import FastAPI, Query,HTTPException, Response
from services import Financeiro
from models.transacao import CriarTransacoes, CorrigirTransacoes, FiltrarTransacoes, ResponseTransacoes,ResponseMetricas,CategoriaTotal,Metricas
from database import conect_db
from typing import Optional
app = FastAPI()

financeiro = Financeiro (conexão_banco= conect_db)
financeiro.iniciate_table()

@app.get("/")
def home ():
    return {"status_code": "Está rodando!"}

@app.get("/transacoes")
def listar_transacoes ( categoria_filtro : Optional[list[int]] = Query(None,alias="cat", title = "categoria", 
                description= " id da categoria que o usuário deseja filtrar"), d_inicio: Optional[str] = Query(None, title = "Data Inicio", 
                description= " data que irá ser o ponto de partida pro filtro"), d_fim: Optional[str] = Query(None, title = "Data Fim", 
                description= " data que irá ser o ponto de partida pro filtro")):
    filtro = FiltrarTransacoes(categoria_filtro=categoria_filtro, d_inicio=d_inicio, d_fim=d_fim)
    dados = financeiro.search_by_filter(filtro=filtro)
    return [ResponseTransacoes(**dict(d)) for d in dados ]
    

@app.get("/transacoes/{id_}")
def transacao_por_id (id_: int):
    dados = financeiro.search_by_id(id_=id_)
    return ResponseTransacoes(**dict(dados))


@app.post("/transacoes/new",status_code=201)
def criar_transacao (transacoes: CriarTransacoes):
    financeiro.adict_transaction(transacoes)
    return Response(status_code=201)

@app.delete("/transacoes/{id_}", status_code = 204)
def deletar_transacoes (id_:int):
    financeiro.remove_transaction(id_)
    return Response(status_code=204)
    
@app.patch("/transacoes/{id_}", status_code= 200)
def corrigir_transacao (id_:int, dados: CorrigirTransacoes):
    financeiro.correct_transaction(id_=id_, dados=dados)
    return Response(status_code=200)

@app.get("/transacoes/metricas", status_code=200)
def exibir_metricas():
    lista_categorias = [CategoriaTotal(**dict(d)) for d in financeiro.all_cat_values()]
    metrica = Metricas(**dict(financeiro.get_balance_and_expense()))
    return  ResponseMetricas(categoria_total=lista_categorias,metricas_= metrica)