from flask import jsonify, request


def parse_json_payload():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, (jsonify({'error': 'Envie um corpo JSON valido.'}), 400)
    return data, None


def validate_required_fields(data, required_fields):
    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] in (None, '')
    ]

    if missing_fields:
        missing = ', '.join(missing_fields)
        return jsonify({'error': f'Campos obrigatorios ausentes: {missing}.'}), 400

    return None


def parse_optional_int(data, field_name):
    value = data.get(field_name)
    if value in (None, ''):
        return None, None

    try:
        return int(value), None
    except (TypeError, ValueError):
        return None, (
            jsonify({'error': f'O campo {field_name} deve ser um numero inteiro.'}),
            400,
        )
