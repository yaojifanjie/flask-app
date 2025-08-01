def test_index(client):
    # Set up authentication in session
    with client.session_transaction() as sess:
        sess['authenticated'] = True
        sess['user'] = {'id': 'test_user', 'email': 'test@example.com'}
    
    response = client.get("/")
    data = response.get_json()
    assert "flask-app" == data["name"]
    assert "It works on my machine!" == data["message"]


def test_server_info(client):
    # Set up authentication in session
    with client.session_transaction() as sess:
        sess['authenticated'] = True
        sess['user'] = {'id': 'test_user', 'email': 'test@example.com'}
    
    response = client.get("/server_info")
    data = response.get_json()
    assert "flask-app" == data["name"]
    assert data["version"] is not None
