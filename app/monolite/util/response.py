from flask import jsonify


def json_message(message: str, status_code: int = 200):
    response = jsonify({'message': message})
    response.status_code = status_code
    return response
