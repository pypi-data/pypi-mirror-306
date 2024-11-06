from .client_base import APIClientBase


class APIClientPost(APIClientBase):
    """Extension of APIClientBase with POST method."""

    def post(self, endpoint, data=None):
        """
        Perform a POST request.

        :param endpoint: API endpoint.
        :param data: Data to send in the body of the request.
        :return: Response JSON data.
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
