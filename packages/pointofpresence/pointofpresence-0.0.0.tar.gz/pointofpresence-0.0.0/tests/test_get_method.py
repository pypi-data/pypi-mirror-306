import pytest
from pointofpresence.get_method import APIClientGet


@pytest.fixture
def client():
    return APIClientGet(base_url="https://api.example.com")


def test_get(client):
    """Test the GET method."""
    # Implement your test logic here
    pass
