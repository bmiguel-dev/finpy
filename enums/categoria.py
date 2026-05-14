from enum import Enum

class Categoria(Enum):
    RECEITAS = 1
    CONSULTORIA = 2
    MANUTEÇÃO = 3 
    DESENVOLVIMENTO = 4
    INFRAESTRUTURA = 5

    @classmethod
    def validacao_categoria(cls, categoria_input:list[int]) -> list[Categoria]:
        return [cls(c) for c in categoria_input if c in cls ]
            
