from models.response_models import ProcessVideoResponse
from services.audio_extractor import AudioExtractor
from services.representative_frame_extractor import RepresentativeFrameExtractor
from services.metadata_extractor import MetadataExtractor
from utils.file_utils import FileUtils
from services.scene_detector import SceneDetector
from pathlib import Path


class VideoService:

    def __init__(self):

        self.metadata_extractor = MetadataExtractor()
        self.audio_extractor = AudioExtractor()
        
        self.scene_detector = SceneDetector()
        self.representative_frame_extractor = (
         RepresentativeFrameExtractor()
    )

    def process(
        self,
        video_path: Path,
    ) -> ProcessVideoResponse:

        # video_path = FileUtils.save_upload(file)

        metadata = self.metadata_extractor.extract(
            video_path
        )

        audio_path = self.audio_extractor.extract(
            video_path
        )

        scenes = self.scene_detector.detect(video_path)

        representative_scenes = (
            self.representative_frame_extractor.extract(
                video_path,
                scenes,
            )
        )

        return ProcessVideoResponse(
            video_path=str(video_path),
            metadata=metadata,
            audio_path=str(audio_path),
            scenes=representative_scenes,
        )