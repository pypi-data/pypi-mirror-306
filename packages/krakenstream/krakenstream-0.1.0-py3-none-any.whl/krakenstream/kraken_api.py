"""
This module provides a Python interface to interact with Kraken's REST API.
It includes methods for retrieving server time, and making public requests to Kraken.
The API keys are retrieved from environment variables.
"""

from typing import Optional
import http.client
import json
import os
from datetime import datetime
from krakenstream.exceptions import KrakenApiException

class KrakenApi:
    """
    A class to interact with Kraken's REST API.
    Handles requests and provides methods for retrieving data from Kraken.
    """
    def __init__(
        self: "KrakenApi"
    ):
        """
        Initializes the KrakenApi instance.
        Retrieves the API key and secret from environment variables.
        """
        self.__secret: Optional[str] = os.getenv("KRAKEN_PYTHON_API_KEY")
        self.__api_key: Optional[str] = os.getenv("KRAKEN_PYTHON_API_SECRET")

    def get_server_time(
        self: "KrakenApi"
    ) -> datetime:
        """
        Retrieves the server time from Kraken's API.

        Returns:
            datetime: The server time as a datetime object.

        Raises:
            KrakenApiException: If the API returns an error.
        """
        api_result = self.__request_public("/0/private/Balance")
        print(api_result)
        str_time = api_result["result"]["rfc1123"]
        return datetime.strptime(str_time, '%a, %d %b %y %H:%M:%S %z')

    def __request_public(
        self: "KrakenApi",
        url: str,
        payload: Optional[dict] = None
    ):
        """
        Makes a public request to Kraken's API.

        Args:
            url (str): The endpoint URL to make the request to.
            payload (Optional[dict]): The data to be sent with the request.

        Returns:
            dict: The response content from the API.

        Raises:
            KrakenApiException: If the API returns an error.
        """
        if payload is None:
            payload = {}
        headers = {'Accept': 'application/json'}
        conn = http.client.HTTPSConnection("api.kraken.com")
        conn.request("POST", url, json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read()
        content = json.loads(data)
        if len(content["error"]) > 0:
            raise KrakenApiException(content["error"][0])
        return content
