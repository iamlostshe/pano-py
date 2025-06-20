import cv2


def load_frames(video_path, num_frames=20):
    """Extracts a specified number of frames evenly spaced from a video file.

    Args:
        video_path (str): Path to the video file.
        num_frames (int): Number of frames to extract.

    Returns:
        list: A list of extracted frames as numpy arrays.

    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(1, total_frames // num_frames)

    frames = []
    for i in range(num_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
            print(f"Loaded frame {i+1}/{num_frames}")
        else:
            print(f"Failed to load frame {i+1}/{num_frames}")

    cap.release()
    print(f"Successfully loaded {len(frames)} frames")
    return frames

def create_panorama(frames):
    """Creates a panorama by stitching together a list of frames.

    Args:
        frames (list): A list of frames to stitch together.

    Returns:
        numpy.ndarray: The stitched panorama image, or None if stitching fails.

    """
    print("Creating panorama...")
    stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
    status, panorama = stitcher.stitch(frames)

    if status != cv2.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
        return None
    print("Panorama created successfully")
    return panorama

if __name__ == "__main__":
    video_path = "video.mp4"  # Replace with your video path
    frames = load_frames(video_path, num_frames=20)

    if frames:
        panorama = create_panorama(frames)
        if panorama is not None:
            # Save the panorama
            cv2.imwrite("panorama_result.jpg", panorama)
            print("Panorama saved as 'panorama_result.jpg'")
        else:
            print("Failed to create panorama")
    else:
        print("No frames were loaded from the video")
