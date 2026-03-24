from flask import Blueprint

from ..api_utils import (
    parse_json_payload,
    parse_optional_int,
    success_response,
    validate_non_empty_string,
    validate_required_fields,
)
from ..models import Estadio, db

estadios_bp = Blueprint('estadios', __name__)


@estadios_bp.route('/', methods=['GET'])
def get_estadios():
    """
    Listar todos os estadios
    ---
    tags:
      - Estadios
    responses:
      200:
        description: Lista de estadios retornada
    """
    estadios = Estadio.query.order_by(Estadio.id).all()
    return success_response(
        data=[estadio.to_dict() for estadio in estadios],
        total=len(estadios),
    )


@estadios_bp.route('/<int:id>', methods=['GET'])
def get_estadio_by_id(id):
    """
    Buscar estadio por ID
    ---
    tags:
      - Estadios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Estadio encontrado
    """
    estadio = db.get_or_404(Estadio, id)
    return success_response(data=estadio.to_dict())


@estadios_bp.route('/', methods=['POST'])
def add_estadio():
    """
    Cadastrar novo estadio
    ---
    tags:
      - Estadios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - nome
            - cidade
            - capacidade
          properties:
            nome:
              type: string
              example: Maracana
            cidade:
              type: string
              example: Rio de Janeiro
            capacidade:
              type: integer
              example: 78000
    responses:
      201:
        description: Estadio criado
    """
    data, error = parse_json_payload()
    if error:
        return error

    validation_error = validate_required_fields(data, ['nome', 'cidade', 'capacidade'])
    if validation_error:
        return validation_error

    nome, error = validate_non_empty_string(data['nome'], 'nome', max_length=100)
    if error:
        return error

    cidade, error = validate_non_empty_string(data['cidade'], 'cidade', max_length=100)
    if error:
        return error

    capacidade, error = parse_optional_int(
        data,
        'capacidade',
        minimum=1,
        allow_none=False,
    )
    if error:
        return error

    novo_estadio = Estadio(nome=nome, cidade=cidade, capacidade=capacidade)
    db.session.add(novo_estadio)
    db.session.commit()
    return success_response(
        data=novo_estadio.to_dict(),
        message='Estadio criado com sucesso.',
        status_code=201,
    )


@estadios_bp.route('/<int:id>', methods=['PUT'])
def update_estadio(id):
    """
    Atualizar estadio
    ---
    tags:
      - Estadios
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
            cidade:
              type: string
            capacidade:
              type: integer
    responses:
      200:
        description: Estadio atualizado
    """
    estadio = db.get_or_404(Estadio, id)
    data, error = parse_json_payload()
    if error:
        return error

    if 'nome' in data:
        nome, error = validate_non_empty_string(data['nome'], 'nome', max_length=100)
        if error:
            return error
        estadio.nome = nome

    if 'cidade' in data:
        cidade, error = validate_non_empty_string(
            data['cidade'],
            'cidade',
            max_length=100,
        )
        if error:
            return error
        estadio.cidade = cidade

    if 'capacidade' in data:
        capacidade, error = parse_optional_int(
            data,
            'capacidade',
            minimum=1,
            allow_none=False,
        )
        if error:
            return error
        estadio.capacidade = capacidade

    db.session.commit()
    return success_response(
        data=estadio.to_dict(),
        message='Estadio atualizado com sucesso.',
    )


@estadios_bp.route('/<int:id>', methods=['DELETE'])
def delete_estadio(id):
    """
    Remover estadio
    ---
    tags:
      - Estadios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Estadio removido
    """
    estadio = db.get_or_404(Estadio, id)
    db.session.delete(estadio)
    db.session.commit()
    return success_response(message='Estadio removido com sucesso.')
