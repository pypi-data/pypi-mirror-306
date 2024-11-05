__all__ = (
    "NextError",
    "HTTPError",
    "ServerError",
    "FeatureDisabled",
    "AutumnDisabled",
    "Forbidden",
)

class NextError(Exception):
    "Base exception for next"

class HTTPError(NextError):
    "Base exception for http errors"

class ServerError(NextError):
    "Internal server error"

class FeatureDisabled(NextError):
    "Base class for any feature disabled errors"

class AutumnDisabled(FeatureDisabled):
    "The autumn feature is disabled"

class Forbidden(HTTPError):
    "Missing permissions"
