"""Configuration values for MotionCanvas."""

TRACKED_JOINTS = [
    "LEFT_WRIST",
    "RIGHT_WRIST",
    "LEFT_ELBOW",
    "RIGHT_ELBOW",
    "LEFT_SHOULDER",
    "RIGHT_SHOULDER",
    "LEFT_HIP",
    "RIGHT_HIP",
    "LEFT_KNEE",
    "RIGHT_KNEE",
    "LEFT_ANKLE",
    "RIGHT_ANKLE",
]

VIDEO_INPUT = "data/input/video.mp4"
OUTPUT_IMAGE = "data/output/motion_canvas.png"

FRAME_SKIP = 1
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5
SMOOTHING_WINDOW = 7
GLOW_RADIUS = 21
LINE_THICKNESS = 2
MAX_SPEED = 25.0
CANVAS_COLOR = (0, 0, 0)

# If you want a higher quality render, increase this slightly.
GAUSSIAN_BLUR_KERNEL = (21, 21)
