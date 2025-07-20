import os
from flask import Blueprint, redirect, url_for, session, request, jsonify
from google_auth_oauthlib.flow import Flow

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI',
                              'http://localhost:5000/auth/callback')

# OAuth 2.0 scope that this application requests
SCOPES = ['openid', 'email', 'profile']


def create_flow():
    """Create a Flow instance to manage OAuth 2.0 Authorization Grant flow."""
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise ValueError("Google OAuth credentials not configured. "
                         "Please set GOOGLE_CLIENT_ID and "
                         "GOOGLE_CLIENT_SECRET environment variables.")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [REDIRECT_URI],
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    return flow


@bp.route('/login')
def login():
    """Initiate the OAuth flow."""
    try:
        flow = create_flow()
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        # Store the state in the session for verification
        session['oauth_state'] = state
        return redirect(authorization_url)
    except ValueError as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/callback')
def callback():
    """Handle the OAuth callback."""
    try:
        # Verify the state parameter
        if ('oauth_state' not in session or
                session['oauth_state'] != request.args.get('state')):
            return jsonify({"error": "Invalid state parameter"}), 400

        flow = create_flow()

        # Use the authorization server's response to fetch the OAuth 2.0 tokens
        flow.fetch_token(authorization_response=request.url)

        # Get user info from Google
        credentials = flow.credentials

        # Verify the token
        from google.auth.transport.requests import Request
        from google.oauth2 import id_token

        # Get user info from ID token
        try:
            idinfo = id_token.verify_oauth2_token(
                credentials.id_token, Request(), GOOGLE_CLIENT_ID)

            # Store user info in session
            session['user'] = {
                'id': idinfo['sub'],
                'email': idinfo['email'],
                'name': idinfo.get('name', ''),
                'picture': idinfo.get('picture', ''),
                'verified_email': idinfo.get('email_verified', False)
            }
            session['authenticated'] = True

            # Clean up oauth state
            session.pop('oauth_state', None)

            return redirect(url_for('/.index'))

        except ValueError as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"Authentication failed: {str(e)}"}), 500


@bp.route('/logout')
def logout():
    """Clear the session and log out the user."""
    session.clear()
    return jsonify({"message": "Logged out successfully"})


@bp.route('/user')
def user():
    """Get current user information."""
    if 'authenticated' in session and session['authenticated']:
        return jsonify(session.get('user', {}))
    else:
        return jsonify({"error": "Not authenticated"}), 401
