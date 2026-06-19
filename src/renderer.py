import os
import cv2
import numpy as np
from config import CANVAS_COLOR, GLOW_RADIUS, GAUSSIAN_BLUR_KERNEL, LINE_THICKNESS, MAX_SPEED


class Renderer:
    def __init__(
        self,
        canvas_color=CANVAS_COLOR,
        line_thickness=LINE_THICKNESS,
        glow_radius=GLOW_RADIUS,
        max_speed=MAX_SPEED,
    ):
        self.canvas_color = canvas_color
        self.line_thickness = line_thickness
        self.glow_radius = glow_radius if glow_radius % 2 == 1 else glow_radius + 1
        self.max_speed = max_speed

    def render(self, trails: dict, frame_size: tuple, output_path: str) -> None:
        width, height = frame_size
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        canvas[:] = self.canvas_color

        for trail in trails.values():
            points = trail["points"]
            speeds = trail["speeds"]
            valid = trail["valid"]

            if points.shape[0] < 2:
                continue

            for idx in range(1, points.shape[0]):
                if not valid[idx] or not valid[idx - 1]:
                    continue

                start = tuple(int(v) for v in points[idx - 1])
                end = tuple(int(v) for v in points[idx])
                speed = float(speeds[idx])
                intensity = 0.25 + 0.75 * (idx / max(1, points.shape[0] - 1))
                color = self._color_from_speed(speed, intensity)
                cv2.line(
                    canvas,
                    start,
                    end,
                    color,
                    thickness=self.line_thickness,
                    lineType=cv2.LINE_AA,
                )

        glow = cv2.GaussianBlur(canvas, GAUSSIAN_BLUR_KERNEL, 0)
        canvas = cv2.addWeighted(canvas, 1.0, glow, 0.45, 0)

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        cv2.imwrite(output_path, canvas)

    def _color_from_speed(self, speed: float, intensity: float) -> tuple[int, int, int]:
        normalized = min(max(speed / max(1e-6, self.max_speed), 0.0), 1.0)
        blue = int((0.7 + 0.3 * (1.0 - normalized)) * 255)
        green = int((0.2 + 0.8 * normalized) * 190)
        red = int((0.6 + 0.4 * normalized) * 255)

        blue = int(blue * intensity)
        green = int(green * intensity)
        red = int(red * intensity)

        return (blue, green, red)
