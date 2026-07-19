from pathlib import Path
import redis
from app.models.job_model import VideoJob
from app.config import VIDEO_QUEUE

from app.messaging.redis_queue import RedisQueue

from app.models.event_model import VideoCompletedEvent
from app.services.event_service import EventService
from app.services.video_service import VideoService

from app.utils.logger import Logger

logger = Logger.get_logger()


class VideoWorker:

    def __init__(self):
        self.queue = RedisQueue()
        self.video_service = VideoService()
        self.event_service = EventService()

    def start(self):
        logger.info("Video Worker started.")

        while True:
            job = None                     

            try:
                logger.info("Waiting for job...")
                job = self.queue.pop(VIDEO_QUEUE)

                if job is None:
                    continue

                logger.info(f"Received job: {job}")
                self.process_job(job)

            except redis.exceptions.TimeoutError:
                continue                   

            except Exception as e:
                logger.exception(f"Video worker failed: {e}")

                if job is not None:
                    try:
                        self.event_service.publish_video_failed(
                            task_id=job["task_id"],
                            error=str(e),
                        )
                    except Exception:
                        logger.exception("Failed to publish video failure event")

    def process_job(
        self,
        job: dict,
    ):

        video_job = VideoJob(**job)

        logger.info(f"Processing task: {video_job.task_id}")
        logger.debug(f"Video job: {video_job}")

        video_path = Path(video_job.video_path)

        logger.debug(f"Video path: {video_path}")

        result = self.video_service.process(video_path)

        logger.debug(f"Processing result: {result}")

        event = VideoCompletedEvent(
            task_id=video_job.task_id,
            payload=result,
        )

        self.event_service.publish_video_completed(event)

        logger.info(f"Completed task: {video_job.task_id}")