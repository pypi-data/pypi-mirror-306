import pytest
from flask import Flask, json
from unittest.mock import patch, MagicMock

# Import your API function
from app.emr_job_api import start_emr_job_endpoint

@pytest.fixture
def app():
    """Create and configure a test Flask application."""
    app = Flask(__name__)
    app.route('/api/emr/start-job', methods=['POST'])(start_emr_job_endpoint)
    return app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

def test_missing_required_fields(client):
    """Test missing required fields in request."""
    # Test missing job_name
    test_data = {
        'step': 'test_step'
    }
    
    response = client.post(
        '/api/emr/start-job',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data
    assert 'details' in data

def test_empty_payload(client):
    """Test empty request payload."""
    response = client.post(
        '/api/emr/start-job',
        data=json.dumps({}),
        content_type='application/json'
    )
    
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data