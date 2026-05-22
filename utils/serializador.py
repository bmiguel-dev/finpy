from models import Transacao
from typing import Optional
from datetime import datetime, date


def passar_json_pro_financeiro (lista_transacao: dict[dict]) -> list[Transacao]:
     lista_final = [Transacao.fazer_classe(t) for t in lista_transacao.items()]
     return  lista_final
     
     
def passar_financeiro_pro_json(lista_classe:list[Transacao]) -> list[dict]:
     dict_final = {}
     for t in lista_classe:
          id_, dados = t.fazer_dict()
          dict_final[id_] = dados

     return dict_final  
          
def json_para_datetime (data_1:Optional[str] = None, data_2:Optional[str] = None) -> tuple[date,date]:
     d1 = datetime.strptime(data_1, "%d/%m/%Y").date() if data_1 else None
     d2 = datetime.strptime(data_2, "%d/%m/%Y").date() if data_2 else None
     return d1, d2