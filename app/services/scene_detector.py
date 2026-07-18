from pathlib import Path

from scenedetect import SceneManager, open_video
from scenedetect.detectors import ContentDetector
from app.config import SCENE_DETECTION_THRESHOLD
from app.exceptions import VideoProcessingException
from app.models.internal_models import SceneBoundary


class SceneDetector:

    def __init__(
    self,
    threshold: float = SCENE_DETECTION_THRESHOLD,
):

     self.threshold = threshold

    def detect(
        self,
        video_path: Path,
    ) -> list[SceneBoundary]:
        
        if not video_path.exists():

            raise VideoProcessingException(
                "Video file not found."
            )

        try:

            video_stream = open_video(str(video_path))

            scene_manager = SceneManager()
            detector = ContentDetector(
                threshold=self.threshold,
            )
            scene_manager.add_detector(
                detector
            )

            scene_manager.detect_scenes(video_stream)

            scenes = scene_manager.get_scene_list()

            if not scenes:

                return [
                    SceneBoundary(
                        start=0.0,
                        end=video_stream.duration.get_seconds(),
                    )
                ]

            return [
                SceneBoundary(
                    start=start.get_seconds(),
                    end=end.get_seconds(),
                )
                for start, end in scenes
            ]

        except Exception as e:

            raise VideoProcessingException(
                "Failed to detect scenes."
            ) from e