def test_index(client):
    # Set up authentication in session
    with client.session_transaction() as sess:
        sess['authenticated'] = True
        sess['user'] = {'id': 'test_user', 'email': 'test@example.com'}
    
    response = client.get("/api/")
    data = response.get_json()
    assert "This is the /api endpoint" == data["message"]
