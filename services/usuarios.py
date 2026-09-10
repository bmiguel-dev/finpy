import sqlite3
from models import *
from utils.hash import verifica_senha,criar_hash
from repository import RepositorioUsuarios



class ServiceUsuarios:
    def __init__ (self , repositorio : RepositorioUsuarios):
        self.repositorio = repositorio

    def cadastro (self, dados : UsuarioCadastro):
        email_existente =self.repositorio.procurar_usuario_pelo_email(dados=dados)
        if email_existente:
            raise #erro de email existente 
        senha = criar_hash(dados.senha)
        usuario_cadastrado = self.repositorio.cria_usuario(entrada_dado=dados, hash=senha)
        return self.repositorio.procurar_usuario_pelo_id(usuario_cadastrado) #UsuarioResponse aqui

    def validacao_usuario_login (self, dados : UsuarioLogin) -> int : 
        dados = self.repositorio.procurar_usuario_pelo_email(dados)
        if dados is None:
            raise False # erro email nao bate
        dados_validados = dict(dados)
        id_user = dados_validados.get('id')
        senha_hash = dados_validados.get('senha')
        senha_verificada = verifica_senha (senha=dados.senha, hash=senha_hash)
        if senha_verificada is False:
            raise False # erro senha nao bate
        return self.repositorio.procurar_usuario_pelo_id(id=id_user) #UsuarioResponse aqui






