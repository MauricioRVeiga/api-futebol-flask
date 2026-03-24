from flask import Blueprint, jsonify

from ..api_utils import parse_json_payload, validate_required_fields
from ..models import Time, db

times_bp = Blueprint('times', __name__)


@times_bp.route('/', methods=['GET'])
def get_times():
    """
    Listar todos os times
    ---
    responses:
      200:
        description: Sucesso
    """
    times = Time.query.all()
    return jsonify([time.to_dict() for time in times])


@times_bp.route('/', methods=['POST'])
def add_time():
    """
    Criar novo time
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            nome: {type: string}
            estado: {type: string}
    responses:
      201:
        description: Criado
    """
    data, error_response = parse_json_payload()
    if error_response:
        return error_response

    validation_error = validate_required_fields(data, ['nome', 'estado'])
    if validation_error:
        return validation_error

    novo_time = Time(nome=data['nome'], estado=data['estado'])
    db.session.add(novo_time)
    db.session.commit()
    return jsonify(novo_time.to_dict()), 201


@times_bp.route('/<int:id>', methods=['PUT'])
def update_time(id):
    """
    Atualizar time
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
            estado: {type: string}
    responses:
      200:
        description: Atualizado
    """
    time = Time.query.get_or_404(id)
    data, error_response = parse_json_payload()
    if error_response:
        return error_response

    time.nome = data.get('nome', time.nome)
    time.estado = data.get('estado', time.estado)
    db.session.commit()
    return jsonify(time.to_dict())


@times_bp.route('/<int:id>', methods=['DELETE'])
def delete_time(id):
    """
    Deletar time
    ---
    parameters:
      - name: id
        in: path
        type: integer
    responses:
      200:
        description: Deletado
    """
    time = Time.query.get_or_404(id)
    db.session.delete(time)
    db.session.commit()
    return jsonify({'message': 'Time removido com sucesso.'})
