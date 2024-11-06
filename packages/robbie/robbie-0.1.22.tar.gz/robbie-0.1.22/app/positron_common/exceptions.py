from requests import Response
from positron_common.cli.logging_config import logger
from positron_common.job_api.error_model import ResponseErrorModel

class RemoteCallException(Exception):
    """
    Parent exception class for Robbie package
    """
    user_friendly_message: str
    reason: str
    additional_help: str
    def __init__(self, user_friendly_message: str = "", reason: str = "", additional_help: str = ""):
        self.user_friendly_message = user_friendly_message
        self.reason = reason
        self.additional_help = additional_help

    @staticmethod
    def from_request(response: Response):
        try:
            error = ResponseErrorModel(**response.json())
            logger.debug(f"Error parsing request json: {error}")
            return RemoteCallException(
                user_friendly_message=error.userFriendlyErrorMessage,
                reason=error.message,
            )
        except Exception:
            logger.debug("Error parsing request json", exc_info=True)
            return RemoteCallException("Sorry, an error occurred! If the problem continues, reach out to our support team for help.\nEmail: support@robbie.run")
        
class RobbieException(Exception):
    """
    Parent exception class for Robbie package
    """
    pass

class SerializationException(RobbieException):
    """
    Exception raised when serialization errors occur.
    """
    pass

class DeserializationException(RobbieException):
    """
    Exception raised when deserialization errors occur.
    """
    pass

class DecoratorException(RobbieException):
    """
    Raised when decorator related errors are happening
    """
    pass

class RemoteFunctionException(Exception):
    """
    This is a wrapper exception to allow bubbling up of exceptions happening in a remote function call
    """
    rf_exception: Exception
    def __init__(self, e: Exception):
        self.rf_exception = e
