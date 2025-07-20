from functools import wraps
from flask import session, jsonify, request, render_template_string

# Simple HTML template for login redirect
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login Required</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px;
               text-align: center; }
        .login-box { background: #f9f9f9; padding: 30px; border-radius: 10px;
                     display: inline-block; }
        .button { background: #4285f4; color: white; padding: 15px 30px;
                  text-decoration: none; border-radius: 5px;
                  font-size: 16px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Authentication Required</h2>
        <p>Please log in with your Google account to access this
           application.</p>
        <a href="/auth/login" class="button">Login with Google</a>
    </div>
</body>
</html>
'''


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
            # For browser requests, show login page
            else:
                return render_template_string(LOGIN_TEMPLATE), 401
        return f(*args, **kwargs)
    return decorated_function
