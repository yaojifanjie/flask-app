# flask-app

[![Build](https://github.com/garyjyao/flask-app/actions/workflows/build.yml/badge.svg)](https://github.com/garyjyao/flask-app/actions/workflows/build.yml)

This project was generated from [flask-app-example](https://github.com/garyjyao/flask-app-example).

## Features

- Google OAuth 2.0 authentication
- Protected API endpoints
- Health check endpoints (unprotected)
- Session-based user management

## Setup

### Prerequisites

- Python 3.x
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google OAuth credentials:

Create a project in the [Google Cloud Console](https://console.cloud.google.com/) and enable the Google+ API. Then create OAuth 2.0 credentials and set the following environment variables:

```bash
export GOOGLE_CLIENT_ID="your_google_client_id"
export GOOGLE_CLIENT_SECRET="your_google_client_secret"
export GOOGLE_REDIRECT_URI="http://localhost:5000/auth/callback"  # Optional, defaults to this value
export SECRET_KEY="your_secret_key_for_sessions"  # Optional, random key generated if not set
```

### Running the Application

```bash
# Development mode
FLASK_APP=app:create_app flask run --debug

# Or using the provided script
./run-app-dev-mode.sh
```

## API Endpoints

### Protected Endpoints (require authentication)

- `GET /` - Main application endpoint
- `GET /server_info` - Server information
- `GET /api/` - API endpoint

### Authentication Endpoints

- `GET /auth/login` - Initiate Google OAuth login
- `GET /auth/callback` - Google OAuth callback (automatically handled)
- `GET /auth/logout` - Logout and clear session
- `GET /auth/user` - Get current user information

### Health Check Endpoints (unprotected)

- `GET /probe/live` - Liveness probe
- `GET /probe/ready` - Readiness probe

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run linting
flake8 app/
```

## Authentication Flow

1. User accesses a protected endpoint
2. If not authenticated, user is redirected to `/auth/login`
3. Application redirects to Google OAuth
4. User logs in with Google
5. Google redirects back to `/auth/callback`
6. Application verifies the token and creates a session
7. User is redirected to the original endpoint




