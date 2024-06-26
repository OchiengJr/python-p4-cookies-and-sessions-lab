import flask

from app import app

app.secret_key = b'a\xdb\xd2\x13\x93\xc1\xe9\x97\xef2\xe3\x004U\xd1Z'

class TestApp:
    """Tests for Flask API in app.py"""

    def setup_method(self, method):
        """Setup method to initialize app context for each test."""
        app.testing = True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def teardown_method(self, method):
        """Teardown method to clean up app context after each test."""
        self.app_context.pop()

    def test_show_articles_route(self):
        """Test the '/articles/<id>' route."""
        response = self.client.get('/articles/1')
        assert response.status_code == 200
        response_json = response.get_json()

        assert 'author' in response_json
        assert 'title' in response_json
        assert 'content' in response_json
        assert 'preview' in response_json
        assert 'minutes_to_read' in response_json
        assert 'date' in response_json

    def test_increments_session_page_views(self):
        """Test session['page_views'] increments correctly."""
        self.client.get('/articles/1')
        assert flask.session.get('page_views') == 1

        self.client.get('/articles/2')
        assert flask.session.get('page_views') == 2

        self.client.get('/articles/3')
        assert flask.session.get('page_views') == 3

        self.client.get('/articles/3')
        assert flask.session.get('page_views') == 4

    def test_limits_three_articles(self):
        """Test maximum three articles limit."""
        response = self.client.get('/articles/1')
        assert response.status_code == 200

        response = self.client.get('/articles/2')
        assert response.status_code == 200

        response = self.client.get('/articles/3')
        assert response.status_code == 200

        response = self.client.get('/articles/4')
        assert response.status_code == 401
        assert response.get_json().get('message') == 'Maximum pageview limit reached'
