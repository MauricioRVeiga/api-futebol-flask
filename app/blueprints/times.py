from flask import Blueprint

from ..api_utils import (
    parse_json_payload,
    success_response,
    validate_estado,
    validate_non_empty_string,
    validate_required_fields,
)
from ..models import Time, db

times_bp = Blueprint('times', __name__)


@times_bp.route('/', methods=['GET'])
def get_times():
    """
    Listar todos os times
    ---
    tags:
      - Times
    responses:
      200:
        description: Lista de times retornada com sucesso
    """
    times = Time.query.order_by(Time.id).all()
    return success_response(
        data=[time.to_dict() for time in times],
        total=len(times),
    )


@times_bp.route('/<int:id>', methods=['GET'])
def get_time_by_id(id):
    """
    Buscar time por ID
    ---
    tags:
      - Times
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do time
    responses:
      200:
        description: Time encontrado
      404:
        description: Time nao encontrado
    """
    time = db.get_or_404(Time, id)
    return success_response(data=time.to_dict())


@times_bp.route('/', methods=['POST'])
def add_time():
    """
    Criar novo time
    ---
    tags:
      - Times
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome
            - estado
          properties:
            nome:
              type: string
              example: Flamengo
            estado:
              type: string
              example: RJ
    responses:
      201:
        description: Time criado
      400:
        description: Dados invalidos
    """
    data, error = parse_json_payload()
    if error:
        return error

    validation_error = validate_required_fields(data, ['nome', 'estado'])
    if validation_error:
        return validation_error

    nome, error = validate_non_empty_string(data['nome'], 'nome', max_length=100)
    if error:
        return error

    estado, error = validate_estado(data['estado'])
    if error:
        return error

    novo_time = Time(nome=nome, estado=estado)
    db.session.add(novo_time)
    db.session.commit()
    return success_response(
        data=novo_time.to_dict(),
        message='Time criado com sucesso.',
        status_code=201,
    )


@times_bp.route('/<int:id>', methods=['PUT'])
def update_time(id):
    """
    Atualizar time
    ---
    tags:
      - Times
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
            nome:
              type: string
              example: Palmeiras
            estado:
              type: string
              example: SP
    responses:
      200:
        description: Time atualizado
    """
    time = db.get_or_404(Time, id)
    data, error = parse_json_payload()
    if error:
        return error

    if 'nome' in data:
        nome, error = validate_non_empty_string(data['nome'], 'nome', max_length=100)
        if error:
            return error
        time.nome = nome

    if 'estado' in data:
        estado, error = validate_estado(data['estado'])
        if error:
            return error
        time.estado = estado

    db.session.commit()
    return success_response(
        data=time.to_dict(),
        message='Time atualizado com sucesso.',
    )


@times_bp.route('/<int:id>', methods=['DELETE'])
def delete_time(id):
    """
    Deletar time
    ---
    tags:
      - Times
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Time removido
    """
    time = db.get_or_404(Time, id)
    db.session.delete(time)
    db.session.commit()
    return success_response(message='Time removido com sucesso.')
