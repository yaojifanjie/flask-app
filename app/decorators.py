from functools import wraps
from flask import session, jsonify, redirect, url_for, request


def require_auth(f):
    """Decorator to require authentication for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session or not session['authenticated']:
            # For JSON API requests, return JSON error
            if (request.is_json or request.path.startswith('/api') or
                    request.headers.get('Accept', '').startswith(
                        'application/json')):
                return jsonify({"error": "Authentication required",
                                "login_url": "/auth/login"}), 401
            # For browser requests, redirect to login
            else:
                return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
