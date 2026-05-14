from models import Transacao


def passar_json_pro_financeiro (lista_transacao: list[dict]) -> list[Transacao]:
     return  [Transacao.fazer_classe(i) for i in lista_transacao]
     
     
def passar_financeiro_pro_json(lista_classe:list[Transacao]) -> list[dict]:
     return  [i.fazer_dict() for i in lista_classe]
          