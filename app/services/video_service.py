from pathlib import Path

from app.models.response_models import ProcessVideoResponse
from app.services.audio_extractor import AudioExtractor
from app.services.metadata_extractor import MetadataExtractor
from app.services.representative_frame_extractor import (
    RepresentativeFrameExtractor,
)
from app.services.scene_detector import SceneDetector
from app.utils.logger import Logger

logger = Logger.get_logger()


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

        logger.info("=" * 80)
        logger.info("Starting video processing pipeline")
        logger.info(f"Video Path : {video_path}")

        try:

            logger.info("-" * 80)
            logger.info("STEP 1 : Metadata Extraction")

            metadata = self.metadata_extractor.extract(
                video_path
            )

            logger.info("Metadata extraction completed successfully.")
            logger.info(f"Metadata : {metadata}")

        except Exception:

            logger.exception("Metadata extraction failed.")
            raise

        try:

            logger.info("-" * 80)
            logger.info("STEP 2 : Audio Extraction")

            audio_path = self.audio_extractor.extract(
                video_path
            )

            logger.info("Audio extraction completed successfully.")
            logger.info(f"Audio Path : {audio_path}")

        except Exception:

            logger.exception("Audio extraction failed.")
            raise

        try:

            logger.info("-" * 80)
            logger.info("STEP 3 : Scene Detection")

            scenes = self.scene_detector.detect(
                video_path
            )

            logger.info(
                f"Scene detection completed. Total scenes: {len(scenes)}"
            )

        except Exception:

            logger.exception("Scene detection failed.")
            raise

        try:

            logger.info("-" * 80)
            logger.info("STEP 4 : Representative Frame Extraction")

            representative_scenes = (
                self.representative_frame_extractor.extract(
                    video_path,
                    scenes,
                )
            )

            logger.info(
                f"Representative frame extraction completed. "
                f"Frames generated: {len(representative_scenes)}"
            )

        except Exception:

            logger.exception(
                "Representative frame extraction failed."
            )
            raise

        logger.info("=" * 80)
        logger.info("Video processing completed successfully.")

        response = ProcessVideoResponse(
            video_path=str(video_path),
            metadata=metadata,
            audio_path=str(audio_path),
            scenes=representative_scenes,
        )

        logger.info(f"Final Response : {response}")
        logger.info("=" * 80)

        return response