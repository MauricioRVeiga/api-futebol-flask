from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Time(db.Model):
    __tablename__ = 'times'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    jogadores = db.relationship(
        'Jogador',
        back_populates='time',
        cascade='all, delete-orphan',
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
    time_id = db.Column(db.Integer, db.ForeignKey('times.id', ondelete='CASCADE'))
    time = db.relationship('Time', back_populates='jogadores')

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'posicao': self.posicao,
            'time_id': self.time_id,
        }


class Estadio(db.Model):
    __tablename__ = 'estadios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cidade': self.cidade,
        }


class Partida(db.Model):
    __tablename__ = 'partidas'

    id = db.Column(db.Integer, primary_key=True)
    time_casa = db.Column(db.String(100), nullable=False)
    time_fora = db.Column(db.String(100), nullable=False)
    placar = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'time_casa': self.time_casa,
            'time_fora': self.time_fora,
            'placar': self.placar,
        }
