from pathlib import Path

from models.job_model import VideoJob
from config import (
    VIDEO_QUEUE,
    
)

from messaging.redis_queue import RedisQueue

from models.event_model import VideoCompletedEvent
from services.event_service import EventService
from services.video_service import VideoService

from utils.logger import Logger

logger = Logger.get_logger()


class VideoWorker:

    def __init__(self):

        self.queue = RedisQueue()

        

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

        video_job = VideoJob(**job)

        video_path = Path(
            video_job.video_path
        )

        logger.info(
            f"Processing task: {video_job.task_id}"
        )

        result = self.video_service.process(
            video_path,
        )

        event = VideoCompletedEvent(
            task_id=video_job.task_id,
            payload=result,
        )

        self.event_service.publish_video_completed(
         event,
         )

        logger.info(
            f"Completed task: {video_job.task_id}"
        )