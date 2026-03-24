def test_home_and_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json()['docs'] == '/apidocs/'

    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_times_crud(client):
    response = client.post('/times', json={'nome': 'Bahia', 'estado': 'ba'})
    assert response.status_code == 201
    payload = response.get_json()['data']
    assert payload['estado'] == 'BA'
    time_id = payload['id']

    response = client.get('/times')
    assert response.status_code == 200
    assert response.get_json()['total'] >= 1

    response = client.get(f'/times/{time_id}')
    assert response.status_code == 200
    assert response.get_json()['data']['nome'] == 'Bahia'

    response = client.put(f'/times/{time_id}', json={'estado': 'sp'})
    assert response.status_code == 200
    assert response.get_json()['data']['estado'] == 'SP'

    response = client.delete(f'/times/{time_id}')
    assert response.status_code == 200


def test_jogadores_crud(client, base_data):
    response = client.post(
        '/jogadores',
        json={
            'nome': 'Pedro',
            'posicao': 'Atacante',
            'time_id': base_data['time_1_id'],
        },
    )
    assert response.status_code == 201
    jogador_id = response.get_json()['data']['id']

    response = client.get(f'/jogadores/{jogador_id}')
    assert response.status_code == 200
    assert response.get_json()['data']['time_nome'] == 'Flamengo'

    response = client.put(
        f'/jogadores/{jogador_id}',
        json={'time_id': base_data['time_2_id'], 'posicao': 'Centroavante'},
    )
    assert response.status_code == 200
    data = response.get_json()['data']
    assert data['time_id'] == base_data['time_2_id']
    assert data['posicao'] == 'Centroavante'

    response = client.delete(f'/jogadores/{jogador_id}')
    assert response.status_code == 200


def test_estadios_crud(client):
    response = client.post(
        '/estadios',
        json={
            'nome': 'Beira-Rio',
            'cidade': 'Porto Alegre',
            'capacidade': 50000,
        },
    )
    assert response.status_code == 201
    estadio_id = response.get_json()['data']['id']

    response = client.get(f'/estadios/{estadio_id}')
    assert response.status_code == 200
    assert response.get_json()['data']['capacidade'] == 50000

    response = client.put(f'/estadios/{estadio_id}', json={'capacidade': 51000})
    assert response.status_code == 200
    assert response.get_json()['data']['capacidade'] == 51000

    response = client.delete(f'/estadios/{estadio_id}')
    assert response.status_code == 200


def test_partidas_crud(client, base_data):
    response = client.post(
        '/partidas',
        json={
            'time_casa_id': base_data['time_1_id'],
            'time_fora_id': base_data['time_2_id'],
            'estadio_id': base_data['estadio_id'],
            'placar': '1x0',
        },
    )
    assert response.status_code == 201
    partida_id = response.get_json()['data']['id']

    response = client.get(f'/partidas/{partida_id}')
    assert response.status_code == 200
    assert response.get_json()['data']['time_casa_nome'] == 'Flamengo'

    response = client.put(f'/partidas/{partida_id}', json={'placar': '2x1'})
    assert response.status_code == 200
    assert response.get_json()['data']['placar'] == '2x1'

    response = client.delete(f'/partidas/{partida_id}')
    assert response.status_code == 200


def test_validation_errors(client, base_data):
    response = client.post('/times', json={'nome': 'ABC', 'estado': 'RIO'})
    assert response.status_code == 400

    response = client.post(
        '/jogadores',
        json={'nome': 'Pedro', 'posicao': 'Atacante', 'time_id': 999},
    )
    assert response.status_code == 404

    response = client.post(
        '/estadios',
        json={'nome': 'A', 'cidade': 'B', 'capacidade': 0},
    )
    assert response.status_code == 400

    response = client.post(
        '/partidas',
        json={
            'time_casa_id': base_data['time_1_id'],
            'time_fora_id': base_data['time_1_id'],
            'estadio_id': base_data['estadio_id'],
            'placar': 'vitoria',
        },
    )
    assert response.status_code == 400
