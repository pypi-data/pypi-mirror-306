from .get_method import APIClientGet
from .post_method import APIClientPost
from .delete_method import APIClientDelete


class APIClient(APIClientGet, APIClientPost, APIClientDelete):
    """Unified API Client with GET, POST, and DELETE methods."""

    pass
