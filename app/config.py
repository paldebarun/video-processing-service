from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


def resolve_path(env_name: str, default: str) -> Path:
    """
    Resolve a directory path from an environment variable.

    - Relative paths are resolved relative to BASE_DIR.
    - Absolute paths are used as-is.
    """

    path = Path(os.environ.get(env_name, default))

    if not path.is_absolute():
        path = BASE_DIR / path

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


UPLOAD_DIR = resolve_path(
    "UPLOAD_DIR",
    "uploads",
)

FRAME_DIR = resolve_path(
    "FRAME_DIR",
    "frames",
)

AUDIO_DIR = resolve_path(
    "AUDIO_DIR",
    "audio",
)

SCENE_DETECTION_THRESHOLD = float(
    os.environ.get(
        "SCENE_DETECTION_THRESHOLD",
        "27.0",
    )
)

PORT = int(
    os.environ.get(
        "PORT",
        "7000",
    )
)