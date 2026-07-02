from datetime import datetime, date
from enums import Categoria
from pydantic import BaseModel, field_validator
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
        if novo_valor is not None:
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
    
    def fazer_dict (self) -> tuple[int,dict]:
        data_formatada = datetime.strftime(self.data, "%d/%m/%Y")
        id = self._id
        return id ,{ 'categoria':self._categoria.name, 'descricao':self.descricao,'valor':self.valor,'data':data_formatada}

    @classmethod
    def fazer_classe ( cls, transacao:tuple[str,dict]) -> 'Transacao':
        id_ = transacao[0]
        data_obj = datetime.strptime(transacao[1]['data'], "%d/%m/%Y").date()
        categoria_validada = Categoria[transacao[1].get('categoria')]

        return cls(id_transacao=int(id_),
        categoria_value=categoria_validada,
        descricao=transacao[1].get('descricao'),
        valor=transacao[1].get('valor'),
        data=data_obj)
    
    def __str__(self) -> str:
        return f"ID: {self.id:>3} | CATEGORIA: {self._categoria.name:<16} | DESCRIÇÃO: {self.descricao:<35} | VALOR: R${self.valor:>11.2f} | DATA: {self.data.strftime("%d/%m/%Y")}"
    
class ResponseTransacoes (BaseModel): 
    id :int
    valor: float
    categoria_id: int
    descricao: str
    data: str

class CriarTransacoes (BaseModel):
    valor: float
    categoria_id: int
    descricao: str
    data: str

    @field_validator("valor")
    def valor_validado (cls,vlr):
        if vlr <= 0:
            raise ValueError("Valor não pode ser negativo, e nem zero.")
        return vlr
    
    @field_validator("categoria_id")
    def categoria_validada (cls, ct):
        if ct <= 0:
            raise ValueError("Valor não pode ser negativo, e nem zero.")
        return ct
    
    @field_validator("data")
    def data_validada (cls,dt:str):
        hoje = datetime.now().date() 
        try:
            dt_obj = datetime.strptime(dt, "%Y-%m-%d").date() 
        except:
            raise ValueError("Coloque a data no formato correto (YYYY-MM-DD)")
        if dt_obj > hoje:
            raise ValueError("A data não pode ser futura.")
        return dt
        
    
    @field_validator("descricao")
    def descricao_validada(cls,dsc:str):
        if not dsc or not dsc.strip():
            raise ValueError("É necessário uma descrição.")
        return dsc
        
    


class CorrigirTransacoes (BaseModel):
    valor: float | None = None
    categoria_id: int | None = None
    descricao: str | None = None 
    data: str | None = None

    @field_validator("valor")
    def valor_validado (cls,vlr | None):
        if vlr is None:
            return vlr
        if vlr <= 0:
            raise ValueError("Valor não pode ser negativo, e nem zero.")
        return vlr
    
    @field_validator("categoria_id")
    def categoria_validada (cls, ct | None):
        if ct is None:
            return ct
        if ct <= 0:
            raise ValueError("Valor não pode ser negativo, e nem zero.")
        return ct
    
    @field_validator("data")
    def data_validada (cls,dt:str | None):
        if dt is None:
            return dt
        hoje = datetime.now().date() 
        try:
            dt_obj = datetime.strptime(dt, "%Y-%m-%d").date() 
        except:
            raise ValueError("Coloque a data no formato correto (YYYY-MM-DD)")
        if dt_obj > hoje:
            raise ValueError("A data não pode ser futura.")
        return dt
        
    

class FiltrarTransacoes (BaseModel):
    categoria_filtro : list[int] | None = None
    d_inicio : str | None = None
    d_fim : str | None = None

    @field_validator("categoria_filtro")
    def validar_categorias(cls,lct: list[int] | None ):
        if lct is None:
            return lct
        for x in lct:
            if x <= 0:
                raise ValueError("o ID da categoria não pode ser 0 nem negativo.")
        return lct
    
    @field_validator("d_inicio")
    def data_i_validada (cls,dt:str | None ):
        if dt is None:
            return dt
        hoje = datetime.now().date() 
        try:
            dt_obj = datetime.strptime(dt, "%Y-%m-%d").date() 
        except:
            raise ValueError("Coloque a data no formato correto (YYYY-MM-DD)")
        if dt_obj > hoje:
            raise ValueError("A data não pode ser futura.")
        return dt
    
    @field_validator("d_fim")
    def data_f_validada (cls,dt:str | None ):
        if dt is None: 
            return dt
        hoje = datetime.now().date() 
        try:
            dt_obj = datetime.strptime(dt, "%Y-%m-%d").date() 
        except:
            raise ValueError("Coloque a data no formato correto (YYYY-MM-DD)")
        if dt_obj > hoje:
            raise ValueError("A data não pode ser futura.")
        return dt

class CategoriaTotal(BaseModel):
    total_valores : int
    nome_categoria : str

class Metricas (BaseModel):
    saldo_total  : int
    despesa_total : int
    total_liquido : int

class ResponseMetricas(BaseModel):
    categoria_total : list[CategoriaTotal]
    metricas_ : Metricas
