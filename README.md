# MotionCanvas

Transform Human Movement into Long-Exposure Digital Art
Overview

MotionCanvas is a computer vision and generative art project that converts human movement in videos into artistic long-exposure visualizations.

Instead of displaying the original video, the system tracks a person's motion over time and generates an abstract artwork composed of motion trails. The final output resembles long-exposure photography, where movement is preserved as flowing streaks of light.

Problem Statement

Traditional videos capture movement frame by frame, but they do not reveal the overall flow and rhythm of motion.

MotionCanvas aims to visualize movement itself as art by transforming human actions into motion trails that represent the path taken through space and time.

Project Goals
Detect and isolate humans from video footage.
Track body movement over time.
Extract motion trajectories from key body joints.
Generate long-exposure style artworks.
Export the generated artwork as a high-resolution image.
Version 2: Segmented Human Motion Trails
Objective

Track only the human subject and ignore background movement.

This ensures that camera shake, moving objects, and environmental noise do not affect the generated artwork.

Pipeline
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
Human Segmentation

The first step is to isolate the person from the background.

Possible Models:

YOLOv8 Segmentation
SAM (Segment Anything)
MegaSAM

Output:

Original Frame
      ↓
Person Mask
      ↓
Foreground Only

Benefits:

Removes background noise.
Focuses only on meaningful motion.
Produces cleaner motion trails.
Pose Estimation

Once the person is segmented, body joints are detected.

Possible Framework:

MediaPipe

Tracked Joints:

Head
Shoulders
Elbows
Wrists
Hips
Knees
Ankles

Each joint receives coordinates for every frame.

Example:

frame_1:
left_wrist = (320, 210)

frame_2:
left_wrist = (328, 215)

frame_3:
left_wrist = (341, 223)
Motion Path Extraction

Joint positions are stored across time.

Example:

left_wrist_path = [
 (320,210),
 (328,215),
 (341,223),
 ...
]

These paths become the foundation of the artwork.

Version 3: Long Exposure Style Renderer
Selected Style
Style 1 — Long Exposure Photography

Inspired by:

Light painting
Long shutter photography
Motion blur art
Dance motion photography
Objective

Create an image that looks like a camera shutter remained open while a person moved through the scene.

Rendering Process
Step 1

Create a blank canvas.

canvas = np.zeros((1080,1920,3))

Black background.

Step 2

Draw Motion Trails

For every tracked joint:

draw_line(
 previous_point,
 current_point
)

Example:

Frame 1
     *
      \
Frame 2
        *
          \
Frame 3
            *

Result:

*---------*---------*
Step 3

Motion Persistence

Older trails gradually fade.

Formula:

trail_opacity *= 0.98

This creates smooth motion flow.

Step 4

Color Mapping

Speed determines color intensity.

Slow Movement
     ↓
Dark Blue

Medium Movement
     ↓
Purple

Fast Movement
     ↓
Bright White

Alternative mode:

Single white trails for authentic long-exposure photography.

Step 5

Glow Effect

Apply Gaussian Blur.

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