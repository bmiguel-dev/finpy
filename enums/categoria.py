from enum import Enum

class Categoria(Enum):
    SALARIO = 1
    INVESTIMENTOS = 2
    FREELANCE = 3 
    ALIMENTACAO = 4 
    LAZER = 5 
    SAUDE =  6
    EDUCACAO = 7 
    TRANSPORTE = 8

    @classmethod
    def lista_categorias (cls):
        return [
            (cls.SALARIO.value, 'Salário', TipoTransacao.RECEITA.value),
            (cls.INVESTIMENTOS.value, 'Investimentos', TipoTransacao.RECEITA.value),
            (cls.FREELANCE.value, 'Freelance', TipoTransacao.RECEITA.value),
            (cls.ALIMENTACAO.value, 'Alimentação', TipoTransacao.DESPESA.value),
            (cls.LAZER.value, 'Lazer', TipoTransacao.DESPESA.value),
            (cls.SAUDE.value, 'Saúde', TipoTransacao.DESPESA.value),
            (cls.EDUCACAO.value, 'Educação', TipoTransacao.DESPESA.value),
            (cls.TRANSPORTE.value, 'Transporte', TipoTransacao.DESPESA.value)
        ]
            

class TipoTransacao(Enum):
    RECEITA = 1
    DESPESA = 2
