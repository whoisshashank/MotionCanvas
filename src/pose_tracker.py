import cv2
import mediapipe as mp
from config import (
    FRAME_SKIP,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
    TRACKED_JOINTS,
)


class PoseTracker:
    def __init__(
        self,
        frame_skip: int = FRAME_SKIP,
        min_detection_confidence: float = MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence: float = MIN_TRACKING_CONFIDENCE,
    ):
        self.frame_skip = max(1, frame_skip)
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def extract(self, video_path: str) -> dict:
        capture = cv2.VideoCapture(video_path)
        if not capture.isOpened():
            raise FileNotFoundError(f"Unable to open video: {video_path}")

        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        frame_index = 0
        paths = {name: [] for name in TRACKED_JOINTS}

        while True:
            success, frame = capture.read()
            if not success:
                break

            if frame_index % self.frame_skip != 0:
                frame_index += 1
                continue

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.pose.process(image)

            if result.pose_landmarks:
                for joint_name in TRACKED_JOINTS:
                    landmark = result.pose_landmarks.landmark[
                        getattr(mp.solutions.pose.PoseLandmark, joint_name)
                    ]
                    valid = landmark.visibility > 0.5
                    if valid:
                        x = int(landmark.x * width)
                        y = int(landmark.y * height)
                        paths[joint_name].append((x, y, float(landmark.visibility)))
                    else:
                        paths[joint_name].append(None)
            else:
                for joint_name in TRACKED_JOINTS:
                    paths[joint_name].append(None)

            frame_index += 1

        capture.release()
        return {
            "frame_size": (width, height),
            "paths": paths,
            "frame_count": frame_index,
        }
