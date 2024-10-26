import logging
import json
from pathlib import Path
import av  # PyAV for video processing

def parse_configs(configs_path: str) -> dict:
    try:
        with open(configs_path, "r") as file:
            configs = json.load(file)
            logger.info(f"Configs: {configs}")
            return configs
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {configs_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON file: {e}")
        raise

CONFIGS_PATH = "configs.json"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

try:
    configs = parse_configs(CONFIGS_PATH)
except Exception as e:
    logger.error(f"Failed to parse configs: {e}")
    exit(1)

PROJECT_DIR = Path(f"{configs['project_dir']}/{configs['project_name']}")
VIDEO_PATH = PROJECT_DIR / "video.mp4"

# Read video using PyAV
try:
    container = av.open(str(VIDEO_PATH))
    logger.info(f"Video opened: {VIDEO_PATH}")
    frame_count = 0

    for frame in container.decode(video=0):
        frame_count += 1
        # You can process the frame here
        # For example, saving the frame as an image
        frame.to_image().save(PROJECT_DIR / f'output_frame_{frame_count:04d}.png')
        logger.info(f"Saved frame {frame_count}")

except FileNotFoundError:
    logger.error(f"Video file not found: {VIDEO_PATH}")
    exit(1)
except Exception as e:
    logger.error(f"Error loading video file: {e}")
    exit(1)

logger.info(f"Processed {frame_count} frames.")
