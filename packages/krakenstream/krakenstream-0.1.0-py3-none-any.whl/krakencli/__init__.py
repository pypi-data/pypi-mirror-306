"""
KrakenStream Module

This module provides an interface to interact with Kraken's REST API.
It includes the KrakenApi class, which handles API requests for querying market
data, placing trades, and managing account information. Additionally, it
contains custom exceptions for handling various error scenarios and data models
to facilitate interaction with Kraken's API.

Modules included:

* krakenapi: Handles API requests to Kraken's endpoints.
* exceptions: Defines custom exceptions to handle specific error scenarios
within KrakenStream.
* models: Contains data models used throughout the KrakenStream to standardize
API interactions.

KrakenStream aims to provide an easy-to-use toolkit for developers wanting to
integrate with Kraken, enabling efficient and secure interactions with the
exchange.
"""

from .kraken_api import KrakenApi
from .exceptions import KrakenApiException
