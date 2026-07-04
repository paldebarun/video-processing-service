from pathlib import Path
import subprocess
import uuid

from config import FRAME_DIR
from exceptions import VideoProcessingException
from models.response_models import Scene
from models.internal_models import SceneBoundary

class RepresentativeFrameExtractor:

    def extract(
        self,
        video_path: Path,
        scenes: list[SceneBoundary],
    ) -> list[Scene]:

        output_folder = FRAME_DIR / str(uuid.uuid4())
        output_folder.mkdir(parents=True, exist_ok=True)

        representative_scenes = []

        try:

            for index, scene in enumerate(scenes, start=1):

                midpoint = (scene.start + scene.end) / 2
                frame_path = (
                    output_folder / f"scene_{index:04d}.jpg"
                )

                command = [
                    "ffmpeg",
                    "-loglevel",
                    "error",
                    "-y",
                    "-ss",
                    str(midpoint),
                    "-i",
                    str(video_path),
                    "-frames:v",
                    "1",
                    str(frame_path),
                ]

                subprocess.run(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True,
                )

                if not frame_path.exists():
                    raise VideoProcessingException(
                        f"Failed to generate representative frame for scene {index}."
                    )

                representative_scenes.append(
                        Scene(
                            start=scene.start,
                            end=scene.end,
                            frame_path=str(frame_path),
                        )
                    )

            return representative_scenes

        except Exception as e:

            raise VideoProcessingException(
                "Failed to extract representative frames."
            ) from e