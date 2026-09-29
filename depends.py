from database.database import database, DataBase
from fastapi import Depends
from services.transacoes import ServiceTransacoes
from services.usuarios import ServiceUsuarios
from repository import RepositorioTransacoes,RepositorioUsuarios
import sqlite3
from utils.seguranca import validar_token_acess


def get_service_transacao (conn : DataBase = Depends(database.conexao_bd)) -> ServiceTransacoes:
    repositorio_conn = RepositorioTransacoes(conn=conn)
    return ServiceTransacoes(repositorio_conn)

def get_service_usuario(conn : sqlite3.Connection = Depends(database.conexao_bd)) -> ServiceUsuarios: # vai passar a conexao pro repositorio e passar o repositorio pro service
    repositorio = RepositorioUsuarios(conn=conn) 
    return ServiceUsuarios(repositorio=repositorio)

def get_usuario_atual (usuario_id : int = Depends(validar_token_acess), service_usuario : ServiceUsuarios = Depends(get_service_usuario) ) -> int: #faz a verificacao do id do usuario, precisa do service de usuarios para funcionar
    service_usuario.verificar_usuario_id(usuario_id)
    return  usuario_id