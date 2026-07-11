from pathlib import Path

from config import (
    VIDEO_QUEUE,
    EVENT_STREAM,
)

from messaging.redis_queue import RedisQueue
from messaging.redis_stream import RedisStream

from models.event_model import VideoCompletedEvent
from services.event_service import EventService
from services.video_service import VideoService

from utils.logger import logger


class VideoWorker:

    def __init__(self):

        self.queue = RedisQueue()

        self.stream = RedisStream()

        self.video_service = VideoService()
        self.event_service = EventService()


    def start(self):

        logger.info(
            "Video Worker started."
        )

        while True:

            job = self.queue.pop(
                VIDEO_QUEUE,
            )

            if job is None:

                continue

            try:

                self.process_job(job)

            except Exception as e:

                self.event_service.publish_video_failed(
                task_id=job["task_id"],
                error=str(e),
                 )

            

                logger.error(
                    f"Video job failed: {e}"
                )

    def process_job(
        self,
        job: dict,
    ):

        task_id = job["task_id"]

        video_path = Path(
            job["video_path"]
        )

        logger.info(
            f"Processing task: {task_id}"
        )

        result = self.video_service.process(
            video_path,
        )

        event = VideoCompletedEvent(
            task_id=task_id,
            payload=result,
        )

        self.event_service.publish_video_completed(
         event,
         )

        logger.info(
            f"Completed task: {task_id}"
        )