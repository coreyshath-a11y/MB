#!/usr/bin/env python3
"""Extract frames from videos at 1fps for visual analysis."""
import cv2
import sys
import os


def extract_frames(video_path, output_dir, fps_rate=1):
    """Extract frames from a video at the specified rate (default: 1 per second)."""
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        print(f"Error: Could not read FPS from {video_path}")
        return 0

    interval = int(fps / fps_rate)
    frame_count = 0
    saved = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % interval == 0:
            cv2.imwrite(f"{output_dir}/frame_{saved:05d}.jpg", frame)
            saved += 1
        frame_count += 1

    cap.release()
    print(f"Extracted {saved} frames from {video_path} to {output_dir}")
    return saved


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_frames.py <video_path> <output_dir> [fps_rate]")
        print("  fps_rate: frames per second to extract (default: 1)")
        sys.exit(1)

    video = sys.argv[1]
    outdir = sys.argv[2]
    rate = float(sys.argv[3]) if len(sys.argv) > 3 else 1

    extract_frames(video, outdir, rate)
