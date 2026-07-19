from app.messaging.redis_stream import RedisStream

from app.config import EVENT_STREAM

from app.models.event_model import (
    VideoCompletedEvent,
    VideoFailedEvent,
)

from app.utils.logger import Logger

logger=Logger.get_logger()


class EventService:

    def __init__(self):

        self.stream = RedisStream()

    def publish_video_completed(
        self,
        event: VideoCompletedEvent,
    ):

        self.stream.publish(
            EVENT_STREAM,
            event.model_dump(
                mode="json",
            ),
        )

        logger.info(
            f"Published video.completed for task {event.task_id}"
        )

    def publish_video_failed(
        self,
        task_id: str,
        error: str,
    ):

        event = VideoFailedEvent(
            task_id=task_id,
            error=error,
        )

        self.stream.publish(
            EVENT_STREAM,
            event.model_dump(
                mode="json",
            ),
        )

        logger.error(
            f"Published video.failed for task {task_id}"
        )
     