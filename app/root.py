import io
import json

from flask import Blueprint, render_template_string
from flask import jsonify

from app.decorators import require_auth

bp = Blueprint('/', __name__, url_prefix='/')

# Simple HTML template for demo
DEMO_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Flask App with Google Auth</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .auth-info { background: #f0f0f0; padding: 20px; border-radius: 5px; }
        .button { background: #4285f4; color: white; padding: 10px 20px;
                  text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Flask App with Google Authentication</h1>
    <div class="auth-info">
        <h3>Welcome, {{ user.name }}!</h3>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>User ID:</strong> {{ user.id }}</p>
        {% if user.picture %}
        <p><img src="{{ user.picture }}" alt="Profile Picture"
                style="width: 50px; height: 50px; border-radius: 25px;"></p>
        {% endif %}
        <p><a href="/auth/logout" class="button">Logout</a></p>
    </div>
    <h3>API Endpoints:</h3>
    <ul>
        <li><a href="/api/">API Endpoint</a></li>
        <li><a href="/server_info">Server Info</a></li>
        <li><a href="/auth/user">User Info (JSON)</a></li>
        <li><a href="/probe/live">Health Check (unprotected)</a></li>
    </ul>
</body>
</html>
'''


@bp.route('/', methods=['GET'])
@require_auth
def index():
    from flask import request, session
    # If request accepts HTML, return HTML page
    if 'text/html' in request.headers.get('Accept', ''):
        user = session.get('user', {})
        return render_template_string(DEMO_TEMPLATE, user=user)
    # Otherwise return JSON
    return jsonify({"name": "flask-app", "message": "It works on my machine!"})


@bp.route('/server_info', methods=['GET'])
@require_auth
def server_info():
    info = json.loads(io.open('server_info.json').read())
    return jsonify(info)
