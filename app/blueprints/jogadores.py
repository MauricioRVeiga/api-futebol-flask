from flask import Blueprint

from ..api_utils import (
    error_response,
    parse_json_payload,
    parse_optional_int,
    success_response,
    validate_non_empty_string,
    validate_required_fields,
)
from ..models import Jogador, Time, db

jogadores_bp = Blueprint('jogadores', __name__)


def _get_time_or_error(time_id):
    time = db.session.get(Time, time_id)
    if not time:
        return None, error_response('Time informado nao encontrado.', 404)
    return time, None


@jogadores_bp.route('/', methods=['GET'])
def get_jogadores():
    """
    Listar todos os jogadores
    ---
    tags:
      - Jogadores
    responses:
      200:
        description: Lista de jogadores retornada com sucesso
    """
    jogadores = Jogador.query.order_by(Jogador.id).all()
    return success_response(
        data=[jogador.to_dict() for jogador in jogadores],
        total=len(jogadores),
    )


@jogadores_bp.route('/<int:id>', methods=['GET'])
def get_jogador_by_id(id):
    """
    Buscar jogador por ID
    ---
    tags:
      - Jogadores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Jogador encontrado
      404:
        description: Jogador nao encontrado
    """
    jogador = db.get_or_404(Jogador, id)
    return success_response(data=jogador.to_dict())


@jogadores_bp.route('/', methods=['POST'])
def add_jogador():
    """
    Cadastrar novo jogador
    ---
    tags:
      - Jogadores
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome
            - posicao
            - time_id
          properties:
            nome:
              type: string
              example: Pedro
            posicao:
              type: string
              example: Atacante
            time_id:
              type: integer
              example: 1
    responses:
      201:
        description: Jogador criado com sucesso
    """
    data, error = parse_json_payload()
    if error:
        return error

    validation_error = validate_required_fields(data, ['nome', 'posicao', 'time_id'])
    if validation_error:
        return validation_error

    nome, error = validate_non_empty_string(data['nome'], 'nome', max_length=100)
    if error:
        return error

    posicao, error = validate_non_empty_string(
        data['posicao'],
        'posicao',
        max_length=50,
    )
    if error:
        return error

    time_id, error = parse_optional_int(
        data,
        'time_id',
        minimum=1,
        allow_none=False,
    )
    if error:
        return error

    _, error = _get_time_or_error(time_id)
    if error:
        return error

    novo_jogador = Jogador(nome=nome, posicao=posicao, time_id=time_id)
    db.session.add(novo_jogador)
    db.session.commit()
    return success_response(
        data=novo_jogador.to_dict(),
        message='Jogador criado com sucesso.',
        status_code=201,
    )


@jogadores_bp.route('/<int:id>', methods=['PUT'])
def update_jogador(id):
    """
    Atualizar dados do jogador
    ---
    tags:
      - Jogadores
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
            posicao:
              type: string
            time_id:
              type: integer
    responses:
      200:
        description: Jogador atualizado
    """
    jogador = db.get_or_404(Jogador, id)
    data, error = parse_json_payload()
    if error:
        return error

    if 'nome' in data:
        nome, error = validate_non_empty_string(data['nome'], 'nome', max_length=100)
        if error:
            return error
        jogador.nome = nome

    if 'posicao' in data:
        posicao, error = validate_non_empty_string(
            data['posicao'],
            'posicao',
            max_length=50,
        )
        if error:
            return error
        jogador.posicao = posicao

    if 'time_id' in data:
        time_id, error = parse_optional_int(
            data,
            'time_id',
            minimum=1,
            allow_none=False,
        )
        if error:
            return error
        _, error = _get_time_or_error(time_id)
        if error:
            return error
        jogador.time_id = time_id

    db.session.commit()
    return success_response(
        data=jogador.to_dict(),
        message='Jogador atualizado com sucesso.',
    )


@jogadores_bp.route('/<int:id>', methods=['DELETE'])
def delete_jogador(id):
    """
    Remover jogador
    ---
    tags:
      - Jogadores
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Jogador removido
    """
    jogador = db.get_or_404(Jogador, id)
    db.session.delete(jogador)
    db.session.commit()
    return success_response(message='Jogador removido com sucesso.')
