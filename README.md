# LifePlanner

LifePlanner é uma aplicação desktop desenvolvida em Python com PySide6, criada para ajudar na organização pessoal do dia a dia.

A aplicação permite gerir tarefas, eventos, notas, objetivos e consultar relatórios de progresso, num ambiente simples e moderno.

## Funcionalidades

- Registo e login de utilizador
- Login com conta Google
- Dashboard com resumo geral
- Previsão meteorológica semanal no cabeçalho
- Gestão de tarefas
- Filtros por data e categoria nas tarefas
- Calendário com eventos
- Gestão de notas
- Gestão de objetivos e etapas
- Definição de objetivo principal
- Relatórios com estatísticas
- Página de definições

## Tecnologias utilizadas

- Python
- PySide6
- SQLite
- Google OAuth
- Open-Meteo API
- Git / GitHub

## Estrutura do projeto

```text
LifePlanner/
├── app/
├── assets/
├── config/
├── data/
├── database/
├── services/
├── styles/
├── ui/
├── main.py
├── requirements.txt
└── README.md
```
## Como executar

bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt

python main.py

## Login com Google

Para o login com Google funcionar, é necessário colocar o ficheiro de credenciais OAuth nesta pasta:

config/google_oauth_client.json

Este ficheiro não está incluído no GitHub por motivos de segurança.

## Base de dados

A base de dados local é criada automaticamente na pasta:

data/

A base de dados exemplo deve ser colocada na pasta data/ para poder ser utilizada

## Autor

Rogério Ribeiro
