import argparse
from pose_tracker import PoseTracker
from renderer import Renderer
from trail_generator import TrailGenerator
from config import OUTPUT_IMAGE, VIDEO_INPUT


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="MotionCanvas - Convert motion from video into long-exposure artwork"
    )
    parser.add_argument(
        "--input",
        "-i",
        default=VIDEO_INPUT,
        help="Path to the input video file.",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=OUTPUT_IMAGE,
        help="Path to the output PNG file.",
    )
    parser.add_argument(
        "--skip",
        "-s",
        type=int,
        default=1,
        help="Frame skip interval for pose extraction.",
    )
    parser.add_argument(
        "--max-speed",
        type=float,
        default=None,
        help="Maximum speed used for color mapping.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    tracker = PoseTracker(frame_skip=args.skip)
    print(f"Extracting pose data from: {args.input}")
    pose_data = tracker.extract(args.input)

    generator = TrailGenerator()
    print("Generating motion trails")
    trails = generator.generate(pose_data)

    renderer = Renderer(max_speed=args.max_speed or None)
    print(f"Rendering artwork to: {args.output}")
    renderer.render(trails, pose_data["frame_size"], args.output)

    print("Done.")


if __name__ == "__main__":
    main()
