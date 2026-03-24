CREATE TABLE IF NOT EXISTS times (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    estado VARCHAR(2) NOT NULL
);

CREATE TABLE IF NOT EXISTS estadios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    cidade VARCHAR(100) NOT NULL,
    capacidade INTEGER NOT NULL CHECK (capacidade > 0)
);

CREATE TABLE IF NOT EXISTS jogadores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    posicao VARCHAR(50) NOT NULL,
    time_id INTEGER NOT NULL REFERENCES times(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS partidas (
    id SERIAL PRIMARY KEY,
    time_casa_id INTEGER NOT NULL REFERENCES times(id) ON DELETE CASCADE,
    time_fora_id INTEGER NOT NULL REFERENCES times(id) ON DELETE CASCADE,
    estadio_id INTEGER NOT NULL REFERENCES estadios(id) ON DELETE CASCADE,
    placar VARCHAR(10) NOT NULL
);

INSERT INTO times (id, nome, estado)
VALUES
    (1, 'Flamengo', 'RJ'),
    (2, 'Palmeiras', 'SP'),
    (3, 'Bahia', 'BA'),
    (4, 'Gremio', 'RS')
ON CONFLICT (id) DO NOTHING;

INSERT INTO estadios (id, nome, cidade, capacidade)
VALUES
    (1, 'Maracana', 'Rio de Janeiro', 78838),
    (2, 'Allianz Parque', 'Sao Paulo', 43713),
    (3, 'Arena Fonte Nova', 'Salvador', 47915),
    (4, 'Arena do Gremio', 'Porto Alegre', 55662)
ON CONFLICT (id) DO NOTHING;

INSERT INTO jogadores (id, nome, posicao, time_id)
VALUES
    (1, 'Pedro', 'Atacante', 1),
    (2, 'Raphael Veiga', 'Meia', 2),
    (3, 'Everton Ribeiro', 'Meia', 3),
    (4, 'Cristaldo', 'Meia', 4)
ON CONFLICT (id) DO NOTHING;

INSERT INTO partidas (id, time_casa_id, time_fora_id, estadio_id, placar)
VALUES
    (1, 1, 2, 1, '2x1'),
    (2, 3, 4, 3, '1x1')
ON CONFLICT (id) DO NOTHING;
