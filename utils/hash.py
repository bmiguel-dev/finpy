from pwdlib import PasswordHash



password_hash =  PasswordHash.recommended()

def criar_hash (senha:str) -> str:
    return password_hash.hash(senha)

def verifica_senha (senha:str, hash:str) -> bool:
    return password_hash.verify(senha,hash)