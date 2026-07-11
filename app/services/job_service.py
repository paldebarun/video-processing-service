from pathlib import Path

from messaging.redis_queue import RedisQueue

from config import VIDEO_QUEUE

from models.job_model import VideoJob

from utils.logger import logger


class JobService:

    def __init__(self):

        self.queue = RedisQueue()

    def submit(
        self,
        job: VideoJob,
    ):

        logger.info(
            f"Submitting video job: {job.task_id}"
        )

        self.queue.push(
            VIDEO_QUEUE,
            job.model_dump(),
        )

        logger.info(
            f"Video job queued: {job.task_id}"
        )