import re

from flask import jsonify, request


PLACAR_REGEX = re.compile(r'^\d{1,2}x\d{1,2}$')


def error_response(message, status_code):
    return jsonify({'error': message}), status_code


def success_response(data=None, message=None, status_code=200, total=None):
    payload = {}
    if message:
        payload['message'] = message
    if data is not None:
        payload['data'] = data
    if total is not None:
        payload['total'] = total
    return jsonify(payload), status_code


def parse_json_payload():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, error_response('Envie um corpo JSON valido.', 400)
    return data, None


def validate_required_fields(data, required_fields):
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] in (None, '')
    ]

    if missing_fields:
        missing = ', '.join(missing_fields)
        return error_response(f'Campos obrigatorios ausentes: {missing}.', 400)

    return None


def parse_optional_int(data, field_name, *, minimum=None, allow_none=True):
    value = data.get(field_name)
    if value in (None, ''):
        if allow_none:
            return None, None
        return None, error_response(
            f'O campo {field_name} e obrigatorio e deve ser um numero inteiro.',
            400,
        )

    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None, error_response(
            f'O campo {field_name} deve ser um numero inteiro.',
            400,
        )

    if minimum is not None and parsed < minimum:
        return None, error_response(
            f'O campo {field_name} deve ser maior ou igual a {minimum}.',
            400,
        )

    return parsed, None


def validate_non_empty_string(value, field_name, *, min_length=1, max_length=None):
    if not isinstance(value, str):
        return None, error_response(f'O campo {field_name} deve ser texto.', 400)

    normalized = value.strip()
    if len(normalized) < min_length:
        return None, error_response(
            f'O campo {field_name} deve ter pelo menos {min_length} caractere(s).',
            400,
        )

    if max_length is not None and len(normalized) > max_length:
        return None, error_response(
            f'O campo {field_name} deve ter no maximo {max_length} caracteres.',
            400,
        )

    return normalized, None


def validate_estado(value):
    normalized, error = validate_non_empty_string(
        value,
        'estado',
        min_length=2,
        max_length=2,
    )
    if error:
        return None, error
    return normalized.upper(), None


def validate_placar(value):
    normalized, error = validate_non_empty_string(
        value,
        'placar',
        min_length=3,
        max_length=10,
    )
    if error:
        return None, error

    if not PLACAR_REGEX.match(normalized):
        return None, error_response(
            'O campo placar deve seguir o formato "0x0".',
            400,
        )

    return normalized, None
