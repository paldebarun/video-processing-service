from pydantic import BaseModel

class Scene(BaseModel):
    start: float
    end: float
    frame_path: str

class VideoMetadata(BaseModel):

    duration: float

    fps: float

    width: int
    height: int

    codec: str

    format: str

    bitrate: int | None = None


class ProcessVideoResponse(BaseModel):

    video_path: str

    metadata: VideoMetadata

    audio_path: str

    scenes: list[Scene]