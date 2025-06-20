"""360 panorama from video."""

import cv2
from loguru import logger

INPUT_VIDEO_PATH = "video.mp4"
OUTPUT_IMAGE_PATH = "panorama_result.jpg"


def load_frames(video_path: str, num_frames: int | None = 20) -> list[cv2.UMat]:
    """Extract a specified number of frames evenly spaced from a video file.

    Args:
        video_path (str): Path to the video file.
        num_frames (int): Number of frames to extract.

    Returns:
        list: A list of extracted frames as numpy arrays.

    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.debug(f"Error: Could not open video file {video_path}")
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(1, total_frames // num_frames)

    frames = []
    for i in range(num_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
            logger.debug(f"Loaded frame {i+1}/{num_frames}")
        else:
            logger.debug(f"Failed to load frame {i+1}/{num_frames}")

    cap.release()
    logger.debug(f"Successfully loaded {len(frames)} frames")
    return frames


def create_panorama(frames: list[cv2.UMat]) -> None | cv2.UMat:
    """Create a panorama by stitching together a list of frames.

    Args:
        frames (list): A list of frames to stitch together.

    Returns:
        numpy.ndarray: The stitched panorama image, or None if stitching fails.

    """
    logger.debug("Creating panorama...")
    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    status, panorama = stitcher.stitch(frames)

    if status != cv2.Stitcher_OK:
        logger.debug("Can't stitch images, error code = {}", status)
        return None
    logger.debug("Panorama created successfully")
    return panorama


if __name__ == "__main__":
    frames = load_frames(INPUT_VIDEO_PATH, num_frames=20)

    if frames:
        panorama = create_panorama(frames)
        if panorama is not None:
            # Save the panorama
            cv2.imwrite(OUTPUT_IMAGE_PATH, panorama)
            logger.debug("Panorama saved as 'panorama_result.jpg'")
        else:
            logger.debug("Failed to create panorama")
    else:
        logger.debug("No frames were loaded from the video")
