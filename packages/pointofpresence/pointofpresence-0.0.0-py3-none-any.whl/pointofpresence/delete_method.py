from .client_base import APIClientBase


class APIClientDelete(APIClientBase):
    """Extension of APIClientBase with DELETE method."""

    def delete(self, endpoint):
        """
        Perform a DELETE request.

        :param endpoint: API endpoint.
        :return: Response status code.
        """
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.status_code
