from fastapi import FastAPI

app = FastAPI()
transacao = [{'id': 1, 'categoria':2, 'descricao':"vasco",'valor':100,'data':'15/10/2007'}]
@app.get("/")
def home (id_transacao):
    return {"status_code": "Está rodando!"}