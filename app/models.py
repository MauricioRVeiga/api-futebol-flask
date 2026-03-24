from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Time(db.Model):
    __tablename__ = 'times'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    estado = db.Column(db.String(2), nullable=False)
    jogadores = db.relationship(
        'Jogador',
        back_populates='time',
        cascade='all, delete-orphan',
        lazy=True,
    )
    partidas_casa = db.relationship(
        'Partida',
        back_populates='time_casa',
        cascade='all, delete-orphan',
        foreign_keys='Partida.time_casa_id',
        lazy=True,
    )
    partidas_fora = db.relationship(
        'Partida',
        back_populates='time_fora',
        cascade='all, delete-orphan',
        foreign_keys='Partida.time_fora_id',
        lazy=True,
    )

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'estado': self.estado,
        }


class Jogador(db.Model):
    __tablename__ = 'jogadores'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    posicao = db.Column(db.String(50), nullable=False)
    time_id = db.Column(
        db.Integer,
        db.ForeignKey('times.id', ondelete='CASCADE'),
        nullable=False,
    )
    time = db.relationship('Time', back_populates='jogadores')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'posicao': self.posicao,
            'time_id': self.time_id,
            'time_nome': self.time.nome if self.time else None,
        }


class Estadio(db.Model):
    __tablename__ = 'estadios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    cidade = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    partidas = db.relationship(
        'Partida',
        back_populates='estadio',
        cascade='all, delete-orphan',
        lazy=True,
    )

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cidade': self.cidade,
            'capacidade': self.capacidade,
        }


class Partida(db.Model):
    __tablename__ = 'partidas'

    id = db.Column(db.Integer, primary_key=True)
    time_casa_id = db.Column(
        db.Integer,
        db.ForeignKey('times.id', ondelete='CASCADE'),
        nullable=False,
    )
    time_fora_id = db.Column(
        db.Integer,
        db.ForeignKey('times.id', ondelete='CASCADE'),
        nullable=False,
    )
    estadio_id = db.Column(
        db.Integer,
        db.ForeignKey('estadios.id', ondelete='CASCADE'),
        nullable=False,
    )
    placar = db.Column(db.String(10), nullable=False)

    time_casa = db.relationship(
        'Time',
        foreign_keys=[time_casa_id],
        back_populates='partidas_casa',
    )
    time_fora = db.relationship(
        'Time',
        foreign_keys=[time_fora_id],
        back_populates='partidas_fora',
    )
    estadio = db.relationship('Estadio', back_populates='partidas')

    def to_dict(self):
        return {
            'id': self.id,
            'time_casa_id': self.time_casa_id,
            'time_casa_nome': self.time_casa.nome if self.time_casa else None,
            'time_fora_id': self.time_fora_id,
            'time_fora_nome': self.time_fora.nome if self.time_fora else None,
            'estadio_id': self.estadio_id,
            'estadio_nome': self.estadio.nome if self.estadio else None,
            'placar': self.placar,
        }
