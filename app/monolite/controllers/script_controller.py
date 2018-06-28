from flask import jsonify, Request
from sqlalchemy.orm.session import Session
from typing import Callable
from ..models import CheckScript


class ScriptController:

    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def get(self, request: Request):
        page = request.args.get('page') or None
        size = request.args.get('size') or 0

        session = self.session_factory()

        query = session.query(CheckScript)

        if page:
            query = query.limit(size).offset(page * size)

        scripts = [s.to_dict() for s in query.all()]

        session.close()

        return jsonify(scripts)

    def post(self, request: Request):
        response = jsonify({'message': 'Not implemented'})
        response.status_code = 501
        return response
