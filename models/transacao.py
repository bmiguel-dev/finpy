from datetime import datetime, date
from enums import Categoria
class Transacao:
    def __init__(self, id_transacao=None, categoria_value:int=None, descricao:str=None, valor:float=None, data:datetime=None):
        self._id : int = id_transacao 
        self._categoria : Categoria = categoria_value
        self._descricao : str = descricao
        self._valor : float = valor 
        self._data : date = data
    @property
    def categoria (self) -> Categoria:
        return self._categoria
    @property
    def id (self) -> int:
        return self._id 
    @property
    def valor (self) -> float:
        return self._valor
     
    @property
    def data (self) -> date:
        return self._data
     
    @property
    def descricao (self) -> str:
        return self._descricao
    
    @categoria.setter
    def categoria(self,categoria1):
        if categoria1:
            self._categoria = Categoria(categoria1)
            self.categoria_utils = categoria1
        else:
            raise TypeError("Escolha uma Categoria")
            
        
    @data.setter   
    def data (self,nova_data:date):
        if nova_data:
            hoje_data = datetime.now().date()
            if nova_data > hoje_data:
                raise ValueError ("A data não pode ser futura")
            self._data : date = nova_data
        else:
            raise TypeError ("Não pode receber data vazia")
    

     
    @valor.setter
    def valor (self, novo_valor):   
        if novo_valor:
                valorabs = abs(novo_valor)
                if self._categoria.value >= 5:
                    self._valor = -valorabs 
                elif self._categoria.value > 0 and self._categoria.value < 5:
                    self._valor = valorabs  
        else:
            raise TypeError("Insira um valor.")
     
    @descricao.setter
    def descricao (self, nova_descricao):
        if not nova_descricao or len(nova_descricao) == 0:
            raise TypeError ("Coloque uma descrição")
        self._descricao = nova_descricao
    
    def fazer_dict (self):
        data_formatada = datetime.strftime(self.data, "%d/%m/%Y")
        return {'id': self._id, 'categoria':self._categoria.name, 'descricao':self.descricao,'valor':self.valor,'data':data_formatada}

    @classmethod
    def fazer_classe ( cls, transacao:dict) -> Transacao:

        data_obj = datetime.strptime(transacao['data'], "%d/%m/%Y").date()
        categoria_validada = Categoria[transacao.get('categoria')]

        return cls(id_transacao=transacao.get('id'),
        categoria_value=categoria_validada,
        descricao=transacao.get('descricao'),
        valor=transacao.get('valor'),
        data=data_obj)
    
    def __str__(self) -> str:
        return f"ID: {self.id:>3} | CATEGORIA: {self._categoria.name:<16} | DESCRIÇÃO: {self.descricao:<20} | VALOR: R${self.valor:>11.2f} | DATA: {self.data.strftime("%d/%m/%Y")}"
    
