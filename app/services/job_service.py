

from app.messaging.redis_queue import RedisQueue

from app.config import VIDEO_QUEUE

from app.models.job_model import VideoJob

from app.utils.logger import Logger

logger = Logger.get_logger()


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