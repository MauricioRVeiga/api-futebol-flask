# API Futebol Flask

API REST desenvolvida com Flask, Flask-SQLAlchemy, Flask-Migrate e Flasgger para gerenciamento de times, jogadores, estádios e partidas.

## Requisitos do trabalho

- Flask + Flasgger
- 4 Blueprints: `times`, `jogadores`, `estadios` e `partidas`
- Cada blueprint possui `GET`, `POST`, `PUT` e `DELETE`
- Seed em SQL no arquivo [seed.sql](/c:/api-futebol-flask/app/db/seed.sql)
- Docker Compose para o banco de dados PostgreSQL
- Documentação Swagger em `/apidocs/`
- Endpoints extras `GET /<recurso>/<id>` para consulta individual
- Healthcheck em `/health`
- Testes automatizados com `pytest`
- Suporte a migrations com `Flask-Migrate`

## Funcionalidades extras implementadas

- Respostas JSON padronizadas
- Validações de campos obrigatórios e formatos
- Validação de relacionamento entre entidades
- Partidas relacionadas a `times` e `estádios` por ID
- `.env.example` para facilitar configuração local
- Dependências fixadas no `requirements.txt`

## Estrutura das rotas

### Times

- `GET /times`
- `GET /times/<id>`
- `POST /times`
- `PUT /times/<id>`
- `DELETE /times/<id>`

### Jogadores

- `GET /jogadores`
- `GET /jogadores/<id>`
- `POST /jogadores`
- `PUT /jogadores/<id>`
- `DELETE /jogadores/<id>`

### Estádios

- `GET /estadios`
- `GET /estadios/<id>`
- `POST /estadios`
- `PUT /estadios/<id>`
- `DELETE /estadios/<id>`

### Partidas

- `GET /partidas`
- `GET /partidas/<id>`
- `POST /partidas`
- `PUT /partidas/<id>`
- `DELETE /partidas/<id>`

## Estrutura esperada dos dados

### Criar time

```json
{
  "nome": "Flamengo",
  "estado": "RJ"
}
```

### Criar jogador

```json
{
  "nome": "Pedro",
  "posicao": "Atacante",
  "time_id": 1
}
```

### Criar estádio

```json
{
  "nome": "Maracanã",
  "cidade": "Rio de Janeiro",
  "capacidade": 78838
}
```

### Criar partida

```json
{
  "time_casa_id": 1,
  "time_fora_id": 2,
  "estadio_id": 1,
  "placar": "2x1"
}
```

## Como rodar com Docker Compose

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd api-futebol-flask
```

2. Suba os containers:

```bash
docker compose up --build
```

3. A API ficará disponível em `http://localhost:5000`.
4. A documentação Swagger ficará em `http://localhost:5000/apidocs/`.
5. O healthcheck ficará em `http://localhost:5000/health`.
6. O PostgreSQL será iniciado com os dados do seed automaticamente na primeira subida do volume.

## Como rodar localmente

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd api-futebol-flask
```

2. Opcionalmente, copie o arquivo de exemplo de ambiente:

PowerShell:

```powershell
Copy-Item .env.example .env
```

Linux ou macOS:

```bash
cp .env.example .env
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Se quiser usar PostgreSQL, suba apenas o banco com Docker:

```bash
docker compose up db
```

5. Defina a variável `DATABASE_URL` caso queira usar o PostgreSQL.

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

6. Rode as migrations, se desejar alinhar o schema manualmente:

```bash
python -m flask --app run.py db upgrade
```

7. Execute a aplicação:

```bash
python run.py
```

Observação:
Sem `DATABASE_URL`, a aplicação usa SQLite local em `futebol.db`, o que facilita testes rápidos.

## Testes

Execute os testes automatizados com:

```bash
python -m pytest
```

## Migrations

O projeto está preparado para usar `Flask-Migrate`. Caso você altere os modelos no futuro, use:

```bash
python -m flask --app run.py db migrate -m "descricao da alteracao"
python -m flask --app run.py db upgrade
```

## Seed

O seed SQL está em [seed.sql](/c:/api-futebol-flask/app/db/seed.sql) e cria as tabelas com dados iniciais de exemplo.

Se quiser recriar o banco do zero no Docker e reaplicar o seed:

```bash
docker compose down -v
docker compose up --build
```

## Validações importantes

- `estado` deve ter exatamente 2 caracteres
- `capacidade` deve ser maior que zero
- `time_id`, `time_casa_id`, `time_fora_id` e `estadio_id` devem existir
- `placar` deve seguir o formato `0x0`
- uma partida não pode ter o mesmo time nos dois lados
