from .client_base import APIClientBase


class APIClientGet(APIClientBase):
    """Extension of APIClientBase with GET method."""

    def get(self, endpoint, params=None):
        """
        Perform a GET request.

        :param endpoint: API endpoint.
        :param params: Query parameters.
        :return: Response JSON data.
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
