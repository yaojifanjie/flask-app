from flask import Blueprint
from flask import jsonify

bp = Blueprint('probe', __name__, url_prefix='/probe')


@bp.route('/live', methods=['GET'])
def live():
    return jsonify({"message": "I'm alive!"})


@bp.route('/ready', methods=['GET'])
def ready():
    return jsonify({"message": "I'm ready!"})
