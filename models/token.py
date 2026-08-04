from pydantic import BaseModel

class RefreshToken (BaseModel):
    refresh_token : str

class ResponseLogin (BaseModel):
    token_access : str
    token_refresh : str 
    type : str = "bearer"

class ResponseRefresh (BaseModel):
    token_access : str
    type : str = "bearer"