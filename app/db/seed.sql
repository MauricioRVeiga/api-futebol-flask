CREATE TABLE IF NOT EXISTS times (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    estado VARCHAR(2) NOT NULL
);

CREATE TABLE IF NOT EXISTS estadios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS partidas (
    id SERIAL PRIMARY KEY,
    time_casa VARCHAR(100) NOT NULL,
    time_fora VARCHAR(100) NOT NULL,
    placar VARCHAR(10) NOT NULL
);

CREATE TABLE IF NOT EXISTS jogadores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    posicao VARCHAR(50) NOT NULL,
    time_id INTEGER REFERENCES times(id) ON DELETE CASCADE
);

INSERT INTO times (id, nome, estado)
VALUES
    (1, 'Flamengo', 'RJ'),
    (2, 'Palmeiras', 'SP'),
    (3, 'Bahia', 'BA')
ON CONFLICT (id) DO NOTHING;

INSERT INTO estadios (id, nome, cidade)
VALUES
    (1, 'Maracana', 'Rio de Janeiro'),
    (2, 'Allianz Parque', 'Sao Paulo'),
    (3, 'Arena Fonte Nova', 'Salvador')
ON CONFLICT (id) DO NOTHING;

INSERT INTO partidas (id, time_casa, time_fora, placar)
VALUES
    (1, 'Flamengo', 'Palmeiras', '2x1'),
    (2, 'Bahia', 'Flamengo', '1x1')
ON CONFLICT (id) DO NOTHING;

INSERT INTO jogadores (id, nome, posicao, time_id)
VALUES
    (1, 'Pedro', 'Atacante', 1),
    (2, 'Veiga', 'Meia', 2),
    (3, 'Everton Ribeiro', 'Meia', 3)
ON CONFLICT (id) DO NOTHING;
