# FinPy 💰

Sistema de controle financeiro desenvolvido em Python, com seis
opções (fluxos): cadastro, relatório impresso, filtro, métricas,
remoção e correção de transações. Persistência de dados em JSON.

---


## Sobre mim e esse projeto

Me chamo Breno Miguel, tenho 18 anos, sou estudante universitário 
de Sistemas de Informação no IFES (Instituto Federal do Espírito 
Santo) — aprovado pelo Enem, com início no segundo semestre de 2026.

Esse projeto foi desenvolvido durante meses de estudo autodidata
como forma de pôr em prática o que estou aprendendo antes mesmo
das aulas começarem. Parti do zero absoluto, sem nenhum conhecimento
de programação, e fui evoluindo o mesmo sistema conforme aprendia
novos conceitos — funções, tratamento de erros, POO, persistência
de dados e modularização.

O FinPy é o resultado desse processo e continua evoluindo conforme
meu aprendizado avança.

---

## A evolução

A v1 era um único arquivo com funções simples e dicionários no
lugar de classes. Conforme aprendi POO, modularização e boas
práticas, fui refatorando por completo o sistema até chegar
no estado atual.

**v1:** arquivo único, sem orientação a objetos, dados em dicionários
**v2:** arquitetura em camadas, POO, modularização profissional

---

## O que o sistema faz

- Cadastro de transações com categoria, valor, data e descrição
- Relatório impresso de todas as transações
- Filtro por ID, categoria e período de datas
- Métricas de saúde financeira com saldo, despesa e totais por categoria
- Remoção de transações por ID
- Correção de transações já cadastradas
- Persistência de dados em JSON

---

## Tecnologias

- Python 3.14
- JSON para persistência de dados
- Arquitetura: controllers, services, models, utils, enums

---

## Como rodar

```bash
python main.py
```

---

## Estrutura do projeto
finpy/
├── main.py
├── controllers/
│   └── fluxos.py
├── models/
│   └── transacao.py
├── services/
│   └── financeiro.py
├── utils/
│   ├── display.py
│   └── serializador.py
└── enums/
└── categoria.py

---

## Próximos passos

- [ ] Substituir JSON por banco de dados SQLite
- [ ] Expor o sistema como API REST com FastAPI
- [ ] Deploy da API no Render ou Railway
- [ ] Migração para PostgreSQL em produção
- [ ] Testes automatizados com pytest