from app import config

def test_aws_config():
    assert config.AWS_CONFIG['ACCESS_KEY'] is not None
