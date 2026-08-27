from pydantic import BaseModel, field_validator,EmailStr
from datetime import datetime

class UsuarioCadastro(BaseModel):
    nome : str 
    email : EmailStr 
    senha : str 

    @field_validator("nome")
    def nome_validado (cls,vlr):
        if len(vlr) < 4:
            raise ValueError("O nome precisa ter no mínimo 4 caractéres .")
        return vlr

    @field_validator("senha")
    def senha_validada (cls,vlr):
        if len(vlr) < 7:
            raise ValueError("A senha precisa ter no mínimo 7 caractéres .")
        return vlr

class UsuarioLogin (BaseModel):
    email : EmailStr
    senha : str 

class UsuarioResponse(BaseModel):
    id : int
    nome : str 
    email : EmailStr 
    criacao_login: datetime