import numpy as np
from config import SMOOTHING_WINDOW


class TrailGenerator:
    def __init__(self, smoothing_window: int = SMOOTHING_WINDOW):
        self.smoothing_window = max(1, smoothing_window)

    def generate(self, pose_data: dict) -> dict:
        trails = {}

        for joint_name, raw_path in pose_data["paths"].items():
            if len(raw_path) == 0:
                continue

            valid_mask = np.array([entry is not None for entry in raw_path], dtype=bool)
            if not valid_mask.any():
                continue

            x_values = np.array(
                [(entry[0] if entry is not None else np.nan) for entry in raw_path],
                dtype=float,
            )
            y_values = np.array(
                [(entry[1] if entry is not None else np.nan) for entry in raw_path],
                dtype=float,
            )

            x_filled = self._interpolate_nans(x_values)
            y_filled = self._interpolate_nans(y_values)

            x_smooth = self._smooth(x_filled)
            y_smooth = self._smooth(y_filled)

            speed = self._compute_speed(x_smooth, y_smooth)

            trails[joint_name] = {
                "points": np.column_stack((x_smooth, y_smooth)),
                "speeds": speed,
                "valid": valid_mask,
            }

        return trails

    def _interpolate_nans(self, values: np.ndarray) -> np.ndarray:
        valid = np.isfinite(values)
        if not valid.any():
            return values

        interp_values = values.copy()
        interp_values[~valid] = np.interp(
            np.flatnonzero(~valid),
            np.flatnonzero(valid),
            interp_values[valid],
        )
        return interp_values

    def _smooth(self, values: np.ndarray) -> np.ndarray:
        if self.smoothing_window <= 1:
            return values

        kernel = np.ones(self.smoothing_window, dtype=float) / self.smoothing_window
        return np.convolve(values, kernel, mode="same")

    def _compute_speed(self, x_values: np.ndarray, y_values: np.ndarray) -> np.ndarray:
        dx = np.diff(x_values, prepend=x_values[0])
        dy = np.diff(y_values, prepend=y_values[0])
        speed = np.sqrt(dx * dx + dy * dy)
        speed[~np.isfinite(speed)] = 0.0
        return speed
