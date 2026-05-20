from models import Transacao


def passar_json_pro_financeiro (lista_transacao: dict[dict]) -> list[Transacao]:
     lista_final = [Transacao.fazer_classe(t) for t in lista_transacao.items()]
     return  lista_final
     
     
def passar_financeiro_pro_json(lista_classe:list[Transacao]) -> list[dict]:
     dict_final = {}
     for t in lista_classe:
          id_, dados = t.fazer_dict()
          dict_final[id_] = dados

     return dict_final  
          