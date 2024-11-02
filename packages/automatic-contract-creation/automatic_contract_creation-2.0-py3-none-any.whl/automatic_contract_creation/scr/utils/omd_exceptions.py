class OpenmetadataException(Exception):
    pass


class OpenmetadataNotFound(OpenmetadataException):
    pass


class OpenmetadataUnauthorized(OpenmetadataException):
    pass
