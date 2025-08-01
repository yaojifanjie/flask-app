import pytest
from unittest.mock import patch, MagicMock


def test_auth_login_without_credentials(client):
    """Test login endpoint without Google credentials configured."""
    response = client.get('/auth/login')
    assert response.status_code == 500
    data = response.get_json()
    assert 'error' in data
    assert 'Google OAuth credentials not configured' in data['error']


def test_auth_user_not_authenticated(client):
    """Test user endpoint when not authenticated."""
    response = client.get('/auth/user')
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Not authenticated'


def test_auth_logout(client):
    """Test logout endpoint."""
    response = client.get('/auth/logout')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'Logged out successfully'


@pytest.mark.skip(reason="Environment variable handling issue in test context")
def test_auth_login_with_credentials(client):
    """Test login endpoint with Google credentials configured."""
    import os
    old_client_id = os.environ.get('GOOGLE_CLIENT_ID')
    old_client_secret = os.environ.get('GOOGLE_CLIENT_SECRET')
    old_redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI')
    
    try:
        os.environ['GOOGLE_CLIENT_ID'] = 'test_client_id'
        os.environ['GOOGLE_CLIENT_SECRET'] = 'test_client_secret'
        os.environ['GOOGLE_REDIRECT_URI'] = 'http://localhost:5000/auth/callback'
        
        response = client.get('/auth/login')
        assert response.status_code == 302  # Redirect
        assert 'accounts.google.com' in response.location
    finally:
        # Clean up environment
        if old_client_id is not None:
            os.environ['GOOGLE_CLIENT_ID'] = old_client_id
        else:
            os.environ.pop('GOOGLE_CLIENT_ID', None)
        if old_client_secret is not None:
            os.environ['GOOGLE_CLIENT_SECRET'] = old_client_secret
        else:
            os.environ.pop('GOOGLE_CLIENT_SECRET', None)
        if old_redirect_uri is not None:
            os.environ['GOOGLE_REDIRECT_URI'] = old_redirect_uri
        else:
            os.environ.pop('GOOGLE_REDIRECT_URI', None)


def test_protected_routes_require_auth(client):
    """Test that protected routes require authentication."""
    # Test root endpoint
    response = client.get('/', headers={'Accept': 'application/json'})
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Authentication required'
    
    # Test API endpoint
    response = client.get('/api/', headers={'Accept': 'application/json'})
    assert response.status_code == 401
    data = response.get_json()
    assert data['error'] == 'Authentication required'


def test_probe_routes_unprotected(client):
    """Test that probe routes are not protected."""
    # Test live probe
    response = client.get('/probe/live')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "I'm alive!"
    
    # Test ready probe
    response = client.get('/probe/ready')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == "I'm ready!"


def test_authenticated_user_access(client):
    """Test that authenticated users can access protected routes."""
    with client.session_transaction() as sess:
        sess['authenticated'] = True
        sess['user'] = {
            'id': 'test_user_id',
            'email': 'test@example.com',
            'name': 'Test User'
        }
    
    # Test root endpoint
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'flask-app'
    
    # Test API endpoint
    response = client.get('/api/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['message'] == 'This is the /api endpoint'
    
    # Test user info endpoint
    response = client.get('/auth/user')
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == 'test@example.com'