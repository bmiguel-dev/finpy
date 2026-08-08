# FinPy 💰

> API REST de controle e gestão financeira pessoal, desenvolvida em Python com **FastAPI**, **SQLite** e autenticação segura via **JWT** (Access & Refresh Tokens).

---

##  Sobre o projeto

Me chamo **Breno Miguel**, tenho 18 anos e sou estudante de **Sistemas de Informação no IFES** — início no segundo semestre de 2026.

Este projeto é fruto do meu estudo autodidata contínuo em desenvolvimento backend. Comecei do zero e fui evoluindo a mesma aplicação conforme dominava novos conceitos: desde estruturas básicas e POO até arquitetura em camadas, banco de dados relacional e segurança com JWT.

---

##  Evolução da arquitetura

| Versão | Descrição |
|--------|-----------|
| **v1** | CLI monolítico em arquivo único, sem POO, dados em dicionários na memória |
| **v2** | Refatoração para POO, arquitetura MVC e persistência em JSON |
| **v3 (atual)** | API REST com FastAPI, SQLite com índices de performance, hashing de senhas e autenticação stateless com JWT (Access + Refresh Token) |

---

##  Funcionalidades

### Autenticação e segurança
- Cadastro e login de usuários com hashing de senha via `pwdlib` + `bcrypt`
- Autenticação stateless com JWT — **Access Token** (15 min) e **Refresh Token** (7 dias)
- Isolamento por usuário — cada usuário acessa apenas suas próprias transações e métricas

###  Gestão de transações
- **CRUD completo** — criação, listagem, atualização e remoção
- **Filtros dinâmicos** — por intervalo de datas e múltiplas categorias simultaneamente
- **Métricas financeiras** — saldo total, despesas, saldo líquido e totais por categoria (calculados via `COALESCE` e `CASE WHEN` diretamente no SQL)

---

## Tech Stack

| Tecnologia | Uso |
|------------|-----|
| Python 3.13+ | Linguagem principal |
| FastAPI | Framework web e definição de rotas |
| Pydantic v2 | Validação de schemas e dados de entrada |
| SQLite3 | Banco de dados com índices de performance |
| PyJWT | Geração e validação de tokens JWT |
| pwdlib + bcrypt | Hashing seguro de senhas |
| Uvicorn | Servidor ASGI |

---

##  Estrutura do projeto

```
finpy/
├── main.py              # Entrypoint e definição das rotas
├── database/
│   └── database.py      # Instância do Financeiro
├── models/              # Schemas Pydantic de entrada e saída
│   ├── transacao.py
│   ├── usuarios.py
│   └── token.py
├── services/
│   └── financeiro.py    # Regras de negócio e queries SQL
├── utils/
│   ├── hash.py          # Hashing e verificação de senha
│   └── seguranca.py     # Geração e validação de tokens JWT
└── enums/
    └── categoria.py     # Categorias e tipos de transação
```

---

##  Endpoints

| Método | Rota | Descrição | Auth |
|--------|------|-----------|:----:|
| `POST` | `/cadastro` | Cadastro de novo usuário | ❌ |
| `POST` | `/login` | Login e geração de tokens | ❌ |
| `POST` | `/refresh` | Renovação do access token | ❌ |
| `GET` | `/transacoes` | Lista transações com filtros | ✅ |
| `GET` | `/transacoes/{id}` | Busca transação por ID | ✅ |
| `GET` | `/transacoes/metricas` | Métricas financeiras | ✅ |
| `POST` | `/transacoes/new` | Cria nova transação | ✅ |
| `PATCH` | `/transacoes/{id}` | Atualiza transação | ✅ |
| `DELETE` | `/transacoes/{id}` | Remove transação | ✅ |

---

##  Como rodar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/bmiguel-dev/finpy.git
cd finpy
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY_ACESS=sua-chave-secreta-de-acesso
SECRET_KEY_REFRESH=sua-chave-secreta-de-refresh
```

### 5. Inicie o servidor
```bash
uvicorn main:app --reload
```

### 6. Acesse a documentação interativa

Abra no navegador: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

##  Próximos passos

- [x] Substituir JSON por banco de dados SQLite
- [x] Expor como API REST com FastAPI e Swagger
- [x] Implementar autenticação JWT com Access e Refresh Token
- [ ] Suíte de testes automatizados com pytest
- [ ] Containerização com Docker
- [ ] Deploy em nuvem (Render / Railway)
- [ ] Migração para PostgreSQL em produção