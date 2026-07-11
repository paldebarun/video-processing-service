from datetime import datetime

from pydantic import BaseModel

from models.response_models import (
    ProcessVideoResponse,
)


class VideoCompletedEvent(BaseModel):

    task_id: str

    event_type: str = "video.completed"

    payload: ProcessVideoResponse


class VideoFailedEvent(BaseModel):

    task_id: str

    event_type: str = "video.failed"

    error: str