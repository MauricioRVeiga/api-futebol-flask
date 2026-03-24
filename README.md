# API Futebol Flask

API REST desenvolvida com Flask, Flask-SQLAlchemy e Flasgger para gerenciamento de times, jogadores, estadios e partidas.

## Requisitos do trabalho atendidos

- Flask + Flasgger
- 4 Blueprints: `times`, `jogadores`, `estadios` e `partidas`
- Cada blueprint possui `GET`, `POST`, `PUT` e `DELETE`
- Seed em SQL no arquivo [app/db/seed.sql](/c:/api-futebol-flask/app/db/seed.sql)
- Docker Compose para o banco de dados PostgreSQL
- Documentacao Swagger em `/apidocs/`

## Estrutura das rotas

- `GET /times`
- `POST /times`
- `PUT /times/<id>`
- `DELETE /times/<id>`
- `GET /jogadores`
- `POST /jogadores`
- `PUT /jogadores/<id>`
- `DELETE /jogadores/<id>`
- `GET /estadios`
- `POST /estadios`
- `PUT /estadios/<id>`
- `DELETE /estadios/<id>`
- `GET /partidas`
- `POST /partidas`
- `PUT /partidas/<id>`
- `DELETE /partidas/<id>`

## Como rodar com Docker Compose

1. Suba os containers:

```bash
docker compose up --build
```

2. A API ficara disponivel em `http://localhost:5000`.
3. A documentacao Swagger ficara em `http://localhost:5000/apidocs/`.
4. O PostgreSQL sera iniciado com os dados do seed automaticamente na primeira subida do volume.

## Como rodar localmente

1. Instale as dependencias:

```bash
pip install -r requirements.txt
```

2. Se quiser usar PostgreSQL, suba apenas o banco com Docker:

```bash
docker compose up db
```

3. Defina a variavel `DATABASE_URL` caso queira usar o PostgreSQL:

PowerShell:

```powershell
$env:DATABASE_URL="postgresql://user:password@localhost:5432/futebol_db"
```

Prompt de comando do Windows:

```bat
set DATABASE_URL=postgresql://user:password@localhost:5432/futebol_db
```

Linux ou macOS:

```bash
export DATABASE_URL=postgresql://user:password@localhost:5432/futebol_db
```

4. Execute a aplicacao:

```bash
python run.py
```

Observacao:
Sem `DATABASE_URL`, a aplicacao usa SQLite local em `futebol.db`, o que facilita testes rapidos.

## Seed

O seed SQL esta em [app/db/seed.sql](/c:/api-futebol-flask/app/db/seed.sql) e cria as tabelas com dados iniciais de exemplo.

Se quiser recriar o banco do zero no Docker e reaplicar o seed:

```bash
docker compose down -v
docker compose up --build
```

## Dependencias

- Flask
- Flasgger
- Flask-SQLAlchemy
- psycopg2-binary