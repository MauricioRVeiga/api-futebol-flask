from flask import Blueprint, jsonify

from ..api_utils import parse_json_payload, validate_required_fields
from ..models import Partida, db

partidas_bp = Blueprint('partidas', __name__)


@partidas_bp.route('/', methods=['GET'])
def get_partidas():
    """
    Listar todas as partidas
    ---
    responses:
      200:
        description: Lista de partidas retornada
    """
    partidas = Partida.query.all()
    return jsonify([partida.to_dict() for partida in partidas])


@partidas_bp.route('/', methods=['POST'])
def add_partida():
    """
    Registrar nova partida
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            time_casa: {type: string}
            time_fora: {type: string}
            placar: {type: string}
    responses:
      201:
        description: Partida registrada
    """
    data, error_response = parse_json_payload()
    if error_response:
        return error_response

    validation_error = validate_required_fields(
        data,
        ['time_casa', 'time_fora', 'placar'],
    )
    if validation_error:
        return validation_error

    nova_partida = Partida(
        time_casa=data['time_casa'],
        time_fora=data['time_fora'],
        placar=data['placar'],
    )
    db.session.add(nova_partida)
    db.session.commit()
    return jsonify(nova_partida.to_dict()), 201


@partidas_bp.route('/<int:id>', methods=['PUT'])
def update_partida(id):
    """
    Atualizar placar ou dados da partida
    ---
    parameters:
      - name: id
        in: path
        type: integer
      - name: body
        in: body
        schema:
          properties:
            time_casa: {type: string}
            time_fora: {type: string}
            placar: {type: string}
    responses:
      200:
        description: Partida atualizada
    """
    partida = Partida.query.get_or_404(id)
    data, error_response = parse_json_payload()
    if error_response:
        return error_response

    partida.time_casa = data.get('time_casa', partida.time_casa)
    partida.time_fora = data.get('time_fora', partida.time_fora)
    partida.placar = data.get('placar', partida.placar)
    db.session.commit()
    return jsonify(partida.to_dict())


@partidas_bp.route('/<int:id>', methods=['DELETE'])
def delete_partida(id):
    """
    Remover registro de partida
    ---
    parameters:
      - name: id
        in: path
        type: integer
    responses:
      200:
        description: Partida removida
    """
    partida = Partida.query.get_or_404(id)
    db.session.delete(partida)
    db.session.commit()
    return jsonify({'message': 'Partida removida com sucesso.'})
