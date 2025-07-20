from flask import Blueprint
from flask import jsonify

from app.decorators import require_auth

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/', methods=['GET'])
@require_auth
def index():
    return jsonify({"message": "This is the /api endpoint"})
