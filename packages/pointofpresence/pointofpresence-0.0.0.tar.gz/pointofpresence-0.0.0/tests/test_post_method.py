import pytest
from pointofpresence.post_method import APIClientPost


@pytest.fixture
def client():
    return APIClientPost(base_url="https://api.example.com")


def test_post(client):
    """Test the POST method."""
    # Implement your test logic here
    pass
