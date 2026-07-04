import json
import subprocess
from pathlib import Path

from exceptions import MetadataExtractionException
from models.response_models import VideoMetadata


class MetadataExtractor:

    def extract(
        self,
        video_path: Path,
    ) -> VideoMetadata:

        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(video_path),
        ]

        try:

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )

            data = json.loads(result.stdout)

            video_stream = next(
                stream
                for stream in data["streams"]
                if stream["codec_type"] == "video"
            )

            numerator, denominator = map(
                int,
                video_stream["r_frame_rate"].split("/")
            )

            fps = (
                numerator / denominator
                if denominator != 0
                else 0
            )

            return VideoMetadata(
                duration=float(data["format"]["duration"]),
                fps=fps,
                width=int(video_stream["width"]),
                height=int(video_stream["height"]),
                codec=video_stream["codec_name"],
                format=data["format"]["format_name"],
                bitrate=int(data["format"].get("bit_rate", 0)),
            )

        except Exception as e:

            raise MetadataExtractionException(
                "Failed to extract metadata."
            ) from e