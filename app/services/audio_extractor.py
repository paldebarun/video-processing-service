from pathlib import Path
import subprocess
import uuid

from config import AUDIO_DIR
from exceptions import VideoProcessingException


class AudioExtractor:

    def extract(
        self,
        video_path: Path,
    ) -> Path:

        output_path = AUDIO_DIR / f"{uuid.uuid4()}.wav"

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            str(output_path),
        ]

        try:

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )

            return output_path

        except Exception as e:

            raise VideoProcessingException(
                "Failed to extract audio."
            ) from e