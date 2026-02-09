#!/usr/bin/env python3
"""Transcribe video/audio files using OpenAI Whisper."""
import whisper
import sys
import json
import os


def transcribe_file(file_path, model_size="base"):
    """Transcribe an audio/video file and save the result."""
    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)

    print(f"Transcribing: {file_path}")
    result = model.transcribe(file_path, word_timestamps=True)

    # Save full JSON transcript
    base = os.path.splitext(file_path)[0]
    json_output = base + "_transcript.json"
    with open(json_output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Full transcript saved to: {json_output}")

    # Save readable text transcript
    txt_output = base + "_transcript.txt"
    with open(txt_output, "w") as f:
        for seg in result["segments"]:
            line = f"[{seg['start']:.1f}s - {seg['end']:.1f}s] {seg['text']}"
            f.write(line + "\n")
            print(line)
    print(f"Text transcript saved to: {txt_output}")

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_or_video_file> [model_size]")
        print("  model_size: tiny, base, small, medium, large (default: base)")
        sys.exit(1)

    filepath = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "base"
    transcribe_file(filepath, model)
