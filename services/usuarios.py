from models import *
from utils.hash import verifica_senha,criar_hash
from repository import RepositorioUsuarios
from utils.erros import SenhaNaoCompativel, EmailJaExiste, EmailNaoEncontrado,UsuarioInexistente
import sqlite3

class ServiceUsuarios:
    def __init__ (self , repositorio : RepositorioUsuarios):
        self.repositorio = repositorio

    

    def cadastro_service (self, dados : UsuarioCadastro) -> sqlite3.Row:
        email_existente =self.repositorio.procurar_usuario_pelo_email(dados=dados)
        if email_existente:
            raise EmailJaExiste("Email já cadastrado.")
        senha = criar_hash(dados.senha)
        usuario_cadastrado = self.repositorio.cria_usuario(entrada_dado=dados, hash=senha)
        return self.repositorio.procurar_usuario_pelo_id(usuario_cadastrado) #UsuarioResponse aqui

    def validacao_usuario_email (self, dados : UsuarioLogin) -> dict : 
        dados = self.repositorio.procurar_usuario_pelo_email(dados) # devolve um sqlite3.Row com  dados da tabela usuarios do usuario específico
        if dados is None:
            raise EmailNaoEncontrado("Email não encontrado.")
        return dict(dados)

    def verificar_senha_login (self, dados_validados : dict , dados : UsuarioLogin) -> str:
        id_user = dados_validados.get('id')
        senha_hash = dados_validados.get('senha')
        senha_verificada = verifica_senha(senha= dados.senha, hash=senha_hash)
        if not senha_verificada:
            raise SenhaNaoCompativel("Senha não compatível.")
        return str(id_user) 

    def verificar_usuario_id ( self, id_ : int) -> dict: 
        dados = self.repositorio.procurar_usuario_pelo_id(id_=id_)
        if dados is None:
            raise UsuarioInexistente("Este usuário não existe mais.") 
        return dict(dados)

 





