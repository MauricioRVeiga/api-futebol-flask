from flask import Blueprint, jsonify

from ..api_utils import parse_json_payload, parse_optional_int, validate_required_fields
from ..models import Jogador, Time, db

jogadores_bp = Blueprint('jogadores', __name__)


@jogadores_bp.route('/', methods=['GET'])
def get_jogadores():
    """
    Listar todos os jogadores
    ---
    responses:
      200:
        description: Lista de jogadores retornada com sucesso
    """
    jogadores = Jogador.query.all()
    return jsonify([jogador.to_dict() for jogador in jogadores])


@jogadores_bp.route('/', methods=['POST'])
def add_jogador():
    """
    Cadastrar novo jogador
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            nome: {type: string}
            posicao: {type: string}
            time_id: {type: integer}
    responses:
      201:
        description: Jogador criado com sucesso
    """
    data, error_response = parse_json_payload()
    if error_response:
        return error_response

    validation_error = validate_required_fields(data, ['nome', 'posicao'])
    if validation_error:
        return validation_error

    time_id, int_error = parse_optional_int(data, 'time_id')
    if int_error:
        return int_error

    if time_id is not None and not Time.query.get(time_id):
        return jsonify({'error': 'Time informado nao encontrado.'}), 404

    novo_jogador = Jogador(
        nome=data['nome'],
        posicao=data['posicao'],
        time_id=time_id,
    )
    db.session.add(novo_jogador)
    db.session.commit()
    return jsonify(novo_jogador.to_dict()), 201


@jogadores_bp.route('/<int:id>', methods=['PUT'])
def update_jogador(id):
    """
    Atualizar dados do jogador
    ---
    parameters:
      - name: id
        in: path
        type: integer
      - name: body
        in: body
        schema:
          properties:
            nome: {type: string}
            posicao: {type: string}
            time_id: {type: integer}
    responses:
      200:
        description: Jogador atualizado
    """
    jogador = Jogador.query.get_or_404(id)
    data, error_response = parse_json_payload()
    if error_response:
        return error_response

    jogador.nome = data.get('nome', jogador.nome)
    jogador.posicao = data.get('posicao', jogador.posicao)

    if 'time_id' in data:
        time_id, int_error = parse_optional_int(data, 'time_id')
        if int_error:
            return int_error
        if time_id is not None and not Time.query.get(time_id):
            return jsonify({'error': 'Time informado nao encontrado.'}), 404
        jogador.time_id = time_id

    db.session.commit()
    return jsonify(jogador.to_dict())


@jogadores_bp.route('/<int:id>', methods=['DELETE'])
def delete_jogador(id):
    """
    Remover jogador
    ---
    parameters:
      - name: id
        in: path
        type: integer
    responses:
      200:
        description: Jogador removido
    """
    jogador = Jogador.query.get_or_404(id)
    db.session.delete(jogador)
    db.session.commit()
    return jsonify({'message': 'Jogador removido com sucesso.'})
