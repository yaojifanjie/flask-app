import io
import json

from flask import Blueprint
from flask import jsonify

from app.decorators import require_auth

bp = Blueprint('/', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
@require_auth
def index():
    return jsonify({"name": "flask-app", "message": "It works on my machine!"})


@bp.route('/server_info', methods=['GET'])
@require_auth
def server_info():
    info = json.loads(io.open('server_info.json').read())
    return jsonify(info)
