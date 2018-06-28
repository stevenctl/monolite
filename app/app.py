import sys
from flask import \
    Flask, \
    request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
from monolite.models import Base
from monolite.util import Config
from monolite.controllers import ScriptController
import time

# Hack for mysql and python3
try:
    __import__('MySQLdb')
except:
    pymysql.install_as_MySQLdb()

# Load args and initialize app
argv = sys.argv
app = Flask(__name__)
config = Config(argv[1] if len(argv) > 1 else '/secrets')

# Load database config
db_driver = config.get_value('db_driver', default='mysql')
db_name = config.get_value('db_name', default='cmk_ns')

db_user = config.get_value('db_user')
db_pass = config.get_value('db_pass')

db_host = config.get_value('db_host')
db_port = ":%s" % config.get_value('db_port') if config.get_value('db_port') else ''

db_url = "%s://%s:%s@%s%s/%s" % (db_driver, db_user, db_pass, db_host, db_port, db_name)


def initialize_db(db_url, attempt=0, max_retires=10, delay=1):
    try:
        print("Connecting to %s (attempt %s)" % (db_url, attempt + 1))
        engine = create_engine(db_url)
        session_class = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        return engine, session_class
    except SQLAlchemyError as e:
        if attempt < max_retires:
            time.sleep(delay)
            initialize_db(db_url, attempt + 1, max_retires, delay)
        else:
            raise e


db_engine, Session = initialize_db(db_url)


def session_factory():
    return Session()


# Initialize controllers
script_controller = ScriptController(session_factory)


# Configure application routes

@app.route('/scripts', methods=['GET', 'POST'])
def scripts():
    return getattr(script_controller, request.method.lower())(request)

app.run(host='0.0.0.0')
