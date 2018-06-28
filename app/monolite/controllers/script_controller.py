from flask import jsonify, Request
from sqlalchemy.orm.session import Session
from typing import Callable
from ..models import CheckScript
import re
from ..util.response import json_message

cron_exp = re.compile(
    '^(\*|([0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])|\*\/([0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9])) (\*|([0-9]|1[0-9]|2[0-3])|\*\/([0-9]|1[0-9]|2[0-3])) (\*|([1-9]|1[0-9]|2[0-9]|3[0-1])|\*\/([1-9]|1[0-9]|2[0-9]|3[0-1])) (\*|([1-9]|1[0-2])|\*\/([1-9]|1[0-2])) (\*|([0-6])|\*\/([0-6]))$')


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
        script = CheckScript.from_dict(request.json)

        validation_response = self._validate_script(script)
        if validation_response:
            return validation_response

        session = self.session_factory()
        session.add(script)
        session.commit()
        session.close()

        return json_message('Script saved successfully. ')

    def _validate_script(self, script: CheckScript):
        if not script.name:
            return json_message('Script must have a name. ', 400)

        session = self.session_factory()
        if session.query(CheckScript).filter_by(name=script.name).first():
            return json_message("Script with name '%s' already exists" % script.name, 400)
        session.close()

        if not script.schedule or not cron_exp.match(script.schedule):
            return json_message('Script must have a schedule in cron format. ', 400)

        if not script.script:
            return json_message('Script must have a body. ', 400)

        return None
