from fastapi import  APIRouter,  Depends
from models.usuarios import UsuarioCadastro, UsuarioLogin, UsuarioResponse
from models.token import RefreshToken, ResponseRefresh,ResponseLogin
import sqlite3
from utils.seguranca import  validar_token_refresh, gerar_token_acess,gerar_token_refresh
from database import database
from services import ServiceUsuarios
from repository import RepositorioUsuarios


router = APIRouter(prefix="/usuarios", tags= ["Usuários"])

def get_service_usuario(conn : sqlite3.Connection = Depends(database.conexao_bd)) -> ServiceUsuarios: # vai passar a conexao pro repositorio e passar o repositorio pro service
    repositorio = RepositorioUsuarios(conn=conn) 
    return ServiceUsuarios(repositorio=repositorio)


#mudar injeção de dependencias.

@router.post("/cadastro", status_code=201, response_model=UsuarioResponse)
def cadastro ( dados : UsuarioCadastro, service : ServiceUsuarios = Depends(get_service_usuario) ): 
    user = service.cadastro_service(dados)    # aqui vai criar e fazer o cadastro do usuário /  vai retornar EmailJaExistente em caso de erro | sqlite3.Row com dados do usuario cadastrado
    return dict(user)

@router.post("/login", response_model= ResponseLogin, status_code=200)
def login (dados : UsuarioLogin, service : ServiceUsuarios = Depends(get_service_usuario)  ):
    dados_dict = service.validacao_usuario_email(dados) #verifica se o email bate/ devolve EmailNaoEncontrado em caso de erro | devolve dados do usuario da tabela em formato dict
    user_id = service.verificar_senha_login(dados_dict, dados )#verifica se a senha bate / devolve SenhaNaoCompativel em caso de erro | devolve o id do usuario em str
    token_access = gerar_token_acess({'sub' : user_id})
    token_refresh = gerar_token_refresh({'sub': user_id})
    return {"token_access": token_access,
            "token_refresh":token_refresh,
            "type" : "bearer"}

@router.post("/refresh", response_model= ResponseRefresh, status_code=200)
def refresh (token : RefreshToken, service : ServiceUsuarios = Depends(get_service_usuario) ):
    usuario_id = validar_token_refresh(service,token.refresh_token) #vai realizar a validação do token e retorna o id do usuario(int)
    service.verificar_usuario_id(usuario_id) # verifica se o usuario ainda existe, e retorna um erro caso nao exista.
    token = gerar_token_acess({"sub":str(usuario_id)}) # o sub é uma convenção utilizar como uma str
    return {"token_access": token,
            "type" : "bearer"} 

  