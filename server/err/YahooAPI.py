

class ServerError(Exception):
    """Base class for server exceptions"""
    pass

class ThreadError(Exception):
    """Raised when issues with multi-threading"""
    pass