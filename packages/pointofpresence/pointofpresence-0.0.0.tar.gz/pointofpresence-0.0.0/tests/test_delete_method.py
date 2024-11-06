import pytest
from pointofpresence.delete_method import APIClientDelete


@pytest.fixture
def client():
    return APIClientDelete(base_url="https://api.example.com")


def test_delete(client):
    """Test the DELETE method."""
    # Implement your test logic here
    pass
