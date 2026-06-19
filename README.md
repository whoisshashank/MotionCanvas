# MotionCanvas

MotionCanvas transforms human movement from video into long-exposure digital art. The project tracks body motion, extracts motion trajectories, and renders them as abstract trails that reveal flow, rhythm, and spatial dynamics.

## Overview

MotionCanvas converts videos of people into artistic visualizations by tracking body joints and generating smooth motion trails. Instead of replaying the original frames, the project produces images that resemble long-exposure photography.

## Problem Statement

Standard video playback captures individual frames, but it does not reveal the continuous flow of motion. MotionCanvas visualizes human movement as an artistic path, making motion itself the final output.

## Project Goals

- Detect and isolate humans in video footage
- Track body movement across time
- Extract motion trajectories from key joints
- Render long-exposure style artwork
- Export high-resolution final images

## Architecture

### 1. Video Input

The process begins with a source video containing a human subject.

### 2. Human Segmentation

Segment the person from the background to remove noise and unwanted motion.

Possible models:
- YOLOv8 Segmentation
- SAM (Segment Anything)
- MegaSAM

Benefits:
- removes background motion
- isolates only the subject’s movement
- produces cleaner visual trails

### 3. Pose Estimation

Detect body joints on the segmented subject.

Common framework:
- MediaPipe

Tracked joints:
- Head
- Shoulders
- Elbows
- Wrists
- Hips
- Knees
- Ankles

Each joint receives a coordinate per frame, forming the basis for motion extraction.

### 4. Joint Tracking

Track each joint over time and convert its per-frame positions into continuous motion paths.

Example path:
```
left_wrist_path = [
  (320, 210),
  (328, 215),
  (341, 223),
  ...
]
```

### 5. Motion Path Generation

Use joint trajectories to construct motion trails. Each path represents how a joint moved through space across the video.

### 6. Artwork Rendering

Render the motion paths onto a blank canvas using long-exposure style techniques.

## Rendering Style: Long-Exposure Photography

### Objective

Create images that mimic a camera with an extended shutter, where movement appears as glowing trails.

### Rendering Steps

1. Create a blank canvas
   - Example: `canvas = np.zeros((1080, 1920, 3))`
   - Use a dark or black background

2. Draw motion trails
   - Connect joint positions frame by frame
   - For each tracked joint, draw a line from the previous point to the current point

3. Apply motion persistence
   - Fade older trails gradually
   - Example formula: `trail_opacity *= 0.98`

4. Map color to speed
   - Slow movement → darker tones
   - Medium movement → purple or mid-range hues
   - Fast movement → bright white or high-intensity colors

5. Add glow effects
   - Apply Gaussian blur or similar smoothing to enhance the long-exposure look

## Example Pipeline

```
Input Video
      │
      ▼
Human Segmentation
      │
      ▼
Pose Estimation
      │
      ▼
Joint Tracking
      │
      ▼
Motion Path Generation
      │
      ▼
Artwork Rendering
```

## Notes

- The design emphasizes robustness to camera shake and background motion.
- Segmenting the subject first improves visual quality and reduces noise.
- The result is a stylized artwork rather than a conventional video output.

## Future Enhancements

- Add multiple artistic rendering styles
- Support adjustable color palettes
- Export layered or animated visualizations
- Introduce temporal blending techniques for richer trails


cv2.GaussianBlur()

Then blend with original trails.

Result:

Core Trail
+
Glow Layer
=
Light Painting Effect
Expected Output

Input:

Person dancing

Output:

Black Background

Flowing light trails
generated from arms,
legs and torso motion

Long-exposure photography look
Technology Stack
Computer Vision
Python
OpenCV
NumPy
Human Detection
YOLOv8
Segment Anything Model
Pose Tracking
MediaPipe
Rendering
OpenCV
Pillow
Future Frontend
React
Next.js
Future Enhancements
V4

Interactive 3D Motion Sculptures

Convert trails into 3D geometry.

V5

Music-Reactive Motion Art

Motion trails react to:

BPM
Bass
Song energy
V6

Real-Time Webcam Mode

Webcam
   ↓
Pose Detection
   ↓
Trail Generation
   ↓
Live Art

Users can create artworks simply by moving in front of a camera.

MVP Deliverable

A user uploads a video containing a moving person, and the system generates a high-resolution long-exposure artwork composed of human motion trails while ignoring all background motion. This artwork can then be exported as a PNG suitable for posters, album covers, or portfolio pieces.