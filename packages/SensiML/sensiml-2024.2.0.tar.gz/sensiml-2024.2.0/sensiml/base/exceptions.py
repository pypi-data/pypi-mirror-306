class PipelineOrderException(Exception):
    pass


class DuplicateValueError(Exception):
    def __init__(self, message="Duplicate values used"):
        super(DuplicateValueError, self).__init__(message)


class CaptureUploadFailureError(Exception):
    pass
