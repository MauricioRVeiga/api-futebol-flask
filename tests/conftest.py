import pytest

from app import create_app
from app.models import Estadio, Time, db


@pytest.fixture
def app():
    app = create_app(
        {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'AUTO_CREATE_TABLES': True,
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def base_data(app):
    with app.app_context():
        time_1 = Time(nome='Flamengo', estado='RJ')
        time_2 = Time(nome='Palmeiras', estado='SP')
        estadio = Estadio(
            nome='Maracana',
            cidade='Rio de Janeiro',
            capacidade=78000,
        )
        db.session.add_all([time_1, time_2, estadio])
        db.session.commit()
        return {
            'time_1_id': time_1.id,
            'time_2_id': time_2.id,
            'estadio_id': estadio.id,
        }
