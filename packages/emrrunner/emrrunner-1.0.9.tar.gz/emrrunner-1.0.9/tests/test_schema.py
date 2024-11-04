import pytest
from marshmallow import ValidationError
from app.schema import EMRJobSchema

@pytest.fixture
def schema():
    """Create an instance of EMRJobSchema."""
    return EMRJobSchema()

def test_valid_complete_payload(schema):
    """Test schema with all valid fields."""
    data = {
        'job_name': 'test_job',
        'step': 'test_step',
        'deploy_mode': 'client'
    }
    
    result = schema.load(data)
    
    assert result['job_name'] == 'test_job'
    assert result['step'] == 'test_step'
    assert result['deploy_mode'] == 'client'

def test_valid_minimal_payload(schema):
    """Test schema with only required fields."""
    data = {
        'job_name': 'test_job',
        'step': 'test_step'
    }
    
    result = schema.load(data)
    
    assert result['job_name'] == 'test_job'
    assert result['step'] == 'test_step'
    assert result['deploy_mode'] == 'client'  # default value

def test_missing_required_fields(schema):
    """Test schema with missing required fields."""
    # Missing job_name
    data1 = {
        'step': 'test_step'
    }
    
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data1)
    assert 'job_name' in exc_info.value.messages
    
    # Missing step
    data2 = {
        'job_name': 'test_job'
    }
    
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data2)
    assert 'step' in exc_info.value.messages

def test_invalid_deploy_mode(schema):
    """Test schema with invalid deploy_mode."""
    data = {
        'job_name': 'test_job',
        'step': 'test_step',
        'deploy_mode': 'invalid_mode'
    }
    
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data)
    assert 'deploy_mode' in exc_info.value.messages

def test_empty_string_values(schema):
    """Test schema with empty string values."""
    data = {
        'job_name': '',
        'step': '',
        'deploy_mode': 'client'
    }
    
    # If you want to prevent empty strings, you should see this fail
    result = schema.load(data)
    assert result['job_name'] == ''
    assert result['step'] == ''

def test_serialization(schema):
    """Test schema serialization."""
    data = {
        'job_name': 'test_job',
        'step': 'test_step',
        'deploy_mode': 'cluster'
    }
    
    result = schema.dump(data)
    
    assert result == data

def test_serialization_default_values(schema):
    """Test schema serialization with default values."""
    data = {
        'job_name': 'test_job',
        'step': 'test_step'
    }
    
    result = schema.dump(data)
    
    assert result['job_name'] == 'test_job'
    assert result['step'] == 'test_step'
    assert result['deploy_mode'] == 'client'

def test_extra_fields(schema):
    """Test schema with extra fields."""
    data = {
        'job_name': 'test_job',
        'step': 'test_step',
        'extra_field': 'extra_value'
    }
    
    # Test that the schema raises ValidationError for unknown fields
    with pytest.raises(ValidationError) as exc_info:
        schema.load(data)
    
    # Verify that the error message is about the unknown field
    assert 'extra_field' in exc_info.value.messages
    assert 'Unknown field.' in exc_info.value.messages['extra_field']