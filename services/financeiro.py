from models.transacao import Transacao, Categoria
from datetime import datetime
import json
from utils import passar_json_pro_financeiro, passar_financeiro_pro_json

class Financeiro:
    def __init__(self):
        self._lista_transacao:list[Transacao] = []
        self.carregar_arquivo()

    
    @property
    def lista_transacao(self) -> list[Transacao]:
        return self._lista_transacao
    
    def gerador_id (self) -> int:
        if self._lista_transacao:
            maior_id : Transacao = max(self._lista_transacao, key=lambda t:t._id)
            return maior_id.id + 1 
        else:
            return 1

    
    def adicionar_transacao(self, transacao:Transacao ) -> None:
        transacao._id = self.gerador_id()
        self._lista_transacao.append(transacao)
        
    
    def remover_transacao(self, id_removido) -> bool:
        for i,t in enumerate(self._lista_transacao): 
            if t.id == id_removido:
                del self._lista_transacao[i]
                return True
        return False
    
        
    
    
    def lista_filtro (self,filtro_id:list[int] | None =None, filtro_cat:list[str] | None = None, filtro_dat_1:datetime | None =None,filtro_dat_2:datetime | None =None) -> list[Transacao]:
        if filtro_id:
            return [t for t in self._lista_transacao if t.id in filtro_id ] if filtro_id else self._lista_transacao
        lista_filtrada = self._lista_transacao
        if filtro_cat:
            lista_filtrada = [t for t in lista_filtrada if t.categoria in filtro_cat]
        if filtro_dat_1 and filtro_dat_2:
            lista_filtrada = [t for t in lista_filtrada if  filtro_dat_1 <= t.data <= filtro_dat_2 ]
        return lista_filtrada

    def dados_relatorio (self,lista_filtrada=None) -> list[Transacao]:
        return self._lista_transacao if lista_filtrada is None else lista_filtrada
    
    def total_categorias (self,lista_transacao:list[Transacao]) -> list[tuple[Categoria,float]]:
        categorias_valores = {}
        for t in lista_transacao:
            categoria  = t.categoria
            valor = t.valor 
            valor_atual = categorias_valores.get(categoria, 0.0)
            categorias_valores[categoria] = valor_atual + valor
        return list(categorias_valores.items())
    
    def metrica (self, total_categorias_: dict) -> tuple[float,float,float]:
        lista_totais = total_categorias_
        saldo = sum(valor for cat,valor in lista_totais if valor > 0 )
        despesa = sum(valor for cat,valor in lista_totais if valor <= 0 )
        total = saldo + despesa

        return saldo, despesa, total
    
    def max_valor_categoria (self, total_categorias_: dict) -> tuple[Categoria | None ,Categoria | None ,float | None ]:
        lista_totais = total_categorias_      
        maior_saldo = max((i for i in lista_totais if i[1] > 0),key=lambda v:v[1], default=None) 
        maior_despesa = min((i for i in lista_totais if i[1] < 0),key=lambda v:v[1], default=None)
        total = maior_saldo[1] + maior_despesa[1]
        return maior_saldo, maior_despesa, total
    
    def max_valor_transacao (self, lista_total_categoria:list[Transacao] ) -> tuple [Transacao  | None ,Transacao | None ]:
        maior_saldo = max((i for i in lista_total_categoria if i.valor > 0),key=lambda i:i.valor, default=None) 
        maior_despesa = min((i for i in lista_total_categoria if i.valor < 0),key=lambda i:i.valor, default=None)
        return maior_saldo, maior_despesa
    
    def buscar_transacao (self,input_id) -> Transacao  | None :
        return next((t for t in self._lista_transacao if input_id == t.id), None)
    
    def salvar_arquivo (self) -> None:
        transacao_json = passar_financeiro_pro_json(self._lista_transacao)
        with open("transacoes.json", "w",encoding='utf-8') as arquivo:
            json.dump(transacao_json,arquivo, indent=4, ensure_ascii=False)

    def carregar_arquivo (self) -> None:
        try:
            with open("transacoes.json", "r", encoding='utf-8') as arquivo:
                transacoes = json.load(arquivo)

            self._lista_transacao = passar_json_pro_financeiro(transacoes)       
        except (FileNotFoundError,json.JSONDecodeError):
            self._lista_transacao = []



        

    