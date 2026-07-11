from datetime import datetime

from pydantic import BaseModel, Field

from models.response_models import (
    ProcessVideoResponse,
)


class VideoCompletedEvent(BaseModel):

    task_id: str

    event_type: str = "video.completed"

    payload: ProcessVideoResponse

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )


class VideoFailedEvent(BaseModel):

    task_id: str

    event_type: str = "video.failed"

    error: str

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
    )