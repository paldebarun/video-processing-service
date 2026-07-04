class VideoProcessingException(Exception):
    """Base exception."""
    pass


class MetadataExtractionException(VideoProcessingException):
    pass


class VideoUploadException(VideoProcessingException):
    pass