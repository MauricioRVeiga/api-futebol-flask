from flask import Blueprint

from ..api_utils import (
    error_response,
    parse_json_payload,
    parse_optional_int,
    success_response,
    validate_placar,
    validate_required_fields,
)
from ..models import Estadio, Partida, Time, db

partidas_bp = Blueprint('partidas', __name__)


def _get_related_entities(data):
    time_casa = db.session.get(Time, data['time_casa_id'])
    if not time_casa:
        return None, None, None, error_response('Time da casa nao encontrado.', 404)

    time_fora = db.session.get(Time, data['time_fora_id'])
    if not time_fora:
        return None, None, None, error_response('Time visitante nao encontrado.', 404)

    estadio = db.session.get(Estadio, data['estadio_id'])
    if not estadio:
        return None, None, None, error_response('Estadio informado nao encontrado.', 404)

    if time_casa.id == time_fora.id:
        return None, None, None, error_response(
            'Os times da partida devem ser diferentes.',
            400,
        )

    return time_casa, time_fora, estadio, None


@partidas_bp.route('/', methods=['GET'])
def get_partidas():
    """
    Listar todas as partidas
    ---
    tags:
      - Partidas
    responses:
      200:
        description: Lista de partidas retornada
    """
    partidas = Partida.query.order_by(Partida.id).all()
    return success_response(
        data=[partida.to_dict() for partida in partidas],
        total=len(partidas),
    )


@partidas_bp.route('/<int:id>', methods=['GET'])
def get_partida_by_id(id):
    """
    Buscar partida por ID
    ---
    tags:
      - Partidas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Partida encontrada
    """
    partida = db.get_or_404(Partida, id)
    return success_response(data=partida.to_dict())


@partidas_bp.route('/', methods=['POST'])
def add_partida():
    """
    Registrar nova partida
    ---
    tags:
      - Partidas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - time_casa_id
            - time_fora_id
            - estadio_id
            - placar
          properties:
            time_casa_id:
              type: integer
              example: 1
            time_fora_id:
              type: integer
              example: 2
            estadio_id:
              type: integer
              example: 1
            placar:
              type: string
              example: 2x1
    responses:
      201:
        description: Partida registrada
    """
    data, error = parse_json_payload()
    if error:
        return error

    validation_error = validate_required_fields(
        data,
        ['time_casa_id', 'time_fora_id', 'estadio_id', 'placar'],
    )
    if validation_error:
        return validation_error

    for field_name in ('time_casa_id', 'time_fora_id', 'estadio_id'):
        parsed, error = parse_optional_int(
            data,
            field_name,
            minimum=1,
            allow_none=False,
        )
        if error:
            return error
        data[field_name] = parsed

    placar, error = validate_placar(data['placar'])
    if error:
        return error

    _, _, _, error = _get_related_entities(data)
    if error:
        return error

    nova_partida = Partida(
        time_casa_id=data['time_casa_id'],
        time_fora_id=data['time_fora_id'],
        estadio_id=data['estadio_id'],
        placar=placar,
    )
    db.session.add(nova_partida)
    db.session.commit()
    return success_response(
        data=nova_partida.to_dict(),
        message='Partida criada com sucesso.',
        status_code=201,
    )


@partidas_bp.route('/<int:id>', methods=['PUT'])
def update_partida(id):
    """
    Atualizar dados da partida
    ---
    tags:
      - Partidas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          type: object
          properties:
            time_casa_id:
              type: integer
            time_fora_id:
              type: integer
            estadio_id:
              type: integer
            placar:
              type: string
    responses:
      200:
        description: Partida atualizada
    """
    partida = db.get_or_404(Partida, id)
    data, error = parse_json_payload()
    if error:
        return error

    merged_data = {
        'time_casa_id': partida.time_casa_id,
        'time_fora_id': partida.time_fora_id,
        'estadio_id': partida.estadio_id,
    }

    for field_name in ('time_casa_id', 'time_fora_id', 'estadio_id'):
        if field_name in data:
            parsed, error = parse_optional_int(
                data,
                field_name,
                minimum=1,
                allow_none=False,
            )
            if error:
                return error
            merged_data[field_name] = parsed

    if 'placar' in data:
        placar, error = validate_placar(data['placar'])
        if error:
            return error
        partida.placar = placar

    _, _, _, error = _get_related_entities(merged_data)
    if error:
        return error

    partida.time_casa_id = merged_data['time_casa_id']
    partida.time_fora_id = merged_data['time_fora_id']
    partida.estadio_id = merged_data['estadio_id']
    db.session.commit()
    return success_response(
        data=partida.to_dict(),
        message='Partida atualizada com sucesso.',
    )


@partidas_bp.route('/<int:id>', methods=['DELETE'])
def delete_partida(id):
    """
    Remover registro de partida
    ---
    tags:
      - Partidas
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Partida removida
    """
    partida = db.get_or_404(Partida, id)
    db.session.delete(partida)
    db.session.commit()
    return success_response(message='Partida removida com sucesso.')
