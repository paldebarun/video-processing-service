import json
import subprocess
from pathlib import Path

from app.exceptions import MetadataExtractionException
from app.models.response_models import VideoMetadata
from app.utils.logger import Logger

logger = Logger.get_logger()


class MetadataExtractor:

    def extract(
        self,
        video_path: Path,
    ) -> VideoMetadata:

        logger.info("=" * 80)
        logger.info("Starting metadata extraction")
        logger.info(f"Received video path      : {video_path}")
        logger.info(f"Resolved video path      : {video_path.resolve()}")
        logger.info(f"Video exists             : {video_path.exists()}")
        logger.info(f"Is file                  : {video_path.is_file()}")

        if video_path.exists():
            logger.info(
                f"Video size               : {video_path.stat().st_size} bytes"
            )

        command = [
        "ffprobe",
        "-v",
        "info",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(video_path),
    ]

        logger.info(f"Executing command        : {' '.join(command)}")

        try:

            logger.info("Running ffprobe...")

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )

            logger.info("=" * 40)
            logger.info("FFPROBE OUTPUT")
            logger.info("=" * 40)

            logger.info(f"Return Code : {result.returncode}")
            logger.info(f"STDOUT:\n{result.stdout}")
            logger.info(f"STDERR:\n{result.stderr}")

            result.check_returncode()

            logger.info("Parsing ffprobe JSON output...")

            data = json.loads(result.stdout)

            logger.info("Successfully parsed JSON.")

            logger.info(f"Available top-level keys: {list(data.keys())}")

            streams = data.get("streams", [])

            logger.info(f"Total streams found: {len(streams)}")

            video_stream = next(
                stream
                for stream in streams
                if stream.get("codec_type") == "video"
            )

            logger.info(f"Video codec : {video_stream.get('codec_name')}")
            logger.info(f"Resolution  : {video_stream.get('width')}x{video_stream.get('height')}")
            logger.info(f"Frame Rate  : {video_stream.get('r_frame_rate')}")

            numerator, denominator = map(
                int,
                video_stream["r_frame_rate"].split("/")
            )

            fps = (
                numerator / denominator
                if denominator != 0
                else 0
            )

            metadata = VideoMetadata(
                duration=float(data["format"]["duration"]),
                fps=fps,
                width=int(video_stream["width"]),
                height=int(video_stream["height"]),
                codec=video_stream["codec_name"],
                format=data["format"]["format_name"],
                bitrate=int(data["format"].get("bit_rate", 0)),
            )

            logger.info("Metadata extracted successfully.")
            logger.info(f"Metadata: {metadata}")
            logger.info("=" * 80)

            return metadata

        except subprocess.CalledProcessError as e:

            logger.exception("ffprobe command failed")
            logger.error(f"Return code : {e.returncode}")
            logger.error(f"STDOUT:\n{e.stdout}")
            logger.error(f"STDERR:\n{e.stderr}")

            raise MetadataExtractionException(
                f"ffprobe failed: {e.stderr}"
            ) from e

        except Exception as e:

            logger.exception("Metadata extraction failed")
            logger.error(f"Exception Type : {type(e).__name__}")
            logger.error(f"Exception      : {e}")

            raise MetadataExtractionException(
                f"Failed to extract metadata: {type(e).__name__}: {e}"
            ) from e