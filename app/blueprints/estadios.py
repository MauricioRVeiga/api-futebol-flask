from flask import Blueprint, jsonify

from ..api_utils import parse_json_payload, validate_required_fields
from ..models import Estadio, db

estadios_bp = Blueprint('estadios', __name__)


@estadios_bp.route('/', methods=['GET'])
def get_estadios():
    """
    Listar todos os estadios
    ---
    responses:
      200:
        description: Lista de estadios retornada
    """
    estadios = Estadio.query.all()
    return jsonify([estadio.to_dict() for estadio in estadios])


@estadios_bp.route('/', methods=['POST'])
def add_estadio():
    """
    Cadastrar novo estadio
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            nome: {type: string}
            cidade: {type: string}
    responses:
      201:
        description: Estadio criado
    """
    data, error_response = parse_json_payload()
    if error_response:
        return error_response

    validation_error = validate_required_fields(data, ['nome', 'cidade'])
    if validation_error:
        return validation_error

    novo_estadio = Estadio(nome=data['nome'], cidade=data['cidade'])
    db.session.add(novo_estadio)
    db.session.commit()
    return jsonify(novo_estadio.to_dict()), 201


@estadios_bp.route('/<int:id>', methods=['PUT'])
def update_estadio(id):
    """
    Atualizar estadio
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
            cidade: {type: string}
    responses:
      200:
        description: Estadio atualizado
    """
    estadio = Estadio.query.get_or_404(id)
    data, error_response = parse_json_payload()
    if error_response:
        return error_response

    estadio.nome = data.get('nome', estadio.nome)
    estadio.cidade = data.get('cidade', estadio.cidade)
    db.session.commit()
    return jsonify(estadio.to_dict())


@estadios_bp.route('/<int:id>', methods=['DELETE'])
def delete_estadio(id):
    """
    Remover estadio
    ---
    parameters:
      - name: id
        in: path
        type: integer
    responses:
      200:
        description: Estadio removido
    """
    estadio = Estadio.query.get_or_404(id)
    db.session.delete(estadio)
    db.session.commit()
    return jsonify({'message': 'Estadio removido com sucesso.'})
