"""
This module provides a Python interface to handle Kraken API exceptions.
"""

class KrakenApiException(Exception):
    """
    Custom exception for handling errors from Kraken's API.
    Provides detailed messages based on error codes returned by the API.
    """
    __code_messages: dict[str, str] = {
        "EGeneral:Permission denied":
            ("Permission denied errors are returned when the API client is "
             "attempting a task for which the API key does not have "
             "permission. For example, if an API client attempted to retrieve "
             "the account balance using an API key that was configured to "
             "allow trading access but not account management access, then "
             "the permission denied error would be returned. You can review "
             "your API keys and their settings (such as their permissions) via "
             "the Settings -> API tab of account management. You would need to "
             "make sure that the API keys being used by your third party apps "
             "have all of the settings and permissions that your apps "
             "require."),
        "EAPI:Invalid key": 
            ("This error is returned when the API key used for the call is "
             "either expired or disabled, please review the API key in your "
             "Settings -> API tab of account management or generate a new one "
             "and update your application."),
    }

    def __init__(self, code):
        """
        Initializes the KrakenApiException with an appropriate message based on the error code.

        Args:
            code (str): The error code returned by the Kraken API.

        Raises:
            ValueError: If an unknown error code is provided.
        """
        if code in KrakenApiException.__code_messages:
            super().__init__(f"{code}: {KrakenApiException.__code_messages[code]}")
        else:
            raise ValueError("Received an unknown error message from the Kraken API.")
