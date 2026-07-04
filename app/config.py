from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE_DIR / os.environ.get(
    "UPLOAD_DIR",
    "uploads",
)

FRAME_DIR = BASE_DIR / os.environ.get(
    "FRAME_DIR",
    "frames",
)

AUDIO_DIR = BASE_DIR / os.environ.get(
    "AUDIO_DIR",
    "audio",
)

SCENE_DETECTION_THRESHOLD = float(
    os.environ.get(
        "SCENE_DETECTION_THRESHOLD",
        "27.0",
    )
)

PORT=int(os.environ.get("PORT", 7000))

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

FRAME_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

AUDIO_DIR.mkdir(
    parents=True,
    exist_ok=True,
)