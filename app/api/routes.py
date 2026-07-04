from fastapi import APIRouter, File, HTTPException, UploadFile

from exceptions import VideoProcessingException
from services.video_service import VideoService

router = APIRouter()

video_service = VideoService()


@router.get("/")
def health():

    return {
        "status": "healthy",
        "service": "Video Processing Service",
    }


@router.post("/process")
def process_video(
    file: UploadFile = File(...),
):

    try:

        return video_service.process(file)

    except VideoProcessingException as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )