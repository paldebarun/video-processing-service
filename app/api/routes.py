from fastapi import APIRouter

from app.services.job_service import JobService
from app.services.video_service import VideoService
from app.models.job_model import VideoJob

router = APIRouter()

video_service = VideoService()
job_service = JobService()


@router.get("/")
def health():

    return {
        "status": "healthy",
        "service": "Video Processing Service",
    }


@router.post("/jobs")
def submit_job(request: VideoJob):

    job_service.submit(request)

    return {
        "task_id": request.task_id,
        "status": "QUEUED",
    }