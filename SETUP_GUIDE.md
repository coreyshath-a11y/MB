# MrBeast Puzzle - Local Setup Guide

## Prerequisites

- Python 3.9+
- Node.js 18+ (for Claude Code)
- pip (Python package manager)

## 1. Install Dependencies

```bash
# Video processing tools
pip install yt-dlp opencv-python pyzbar Pillow numpy

# Audio transcription
pip install openai-whisper
# OR for GPU acceleration:
pip install faster-whisper

# Barcode scanning library
# Mac:
brew install zbar
# Linux:
sudo apt install libzbar0
```

## 2. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

## 3. Download Videos

```bash
cd ~/MB  # or wherever your project root is
bash scripts/download_videos.sh
```

## 4. Process Videos (extract frames, scan barcodes, transcribe)

```bash
bash scripts/process_all.sh
```

## 5. Launch Claude Code for Analysis

```bash
cd ~/MB
claude
```

Then paste the prompt from `CLAUDE_PROMPT.md` to start the analysis session.

## Individual Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/download_videos.sh` | Download all puzzle videos | `bash scripts/download_videos.sh` |
| `scripts/extract_frames.py` | Extract frames at 1fps | `python scripts/extract_frames.py <video> <output_dir>` |
| `scripts/scan_barcodes.py` | Scan images for barcodes/QR | `python scripts/scan_barcodes.py <image_dir>` |
| `scripts/transcribe.py` | Transcribe audio with Whisper | `python scripts/transcribe.py <video> [model_size]` |
| `scripts/solve_lifechange.py` | Solve LIFECHANG Sudoku | `python scripts/solve_lifechange.py <puzzle.txt>` |
| `scripts/process_all.sh` | Run all processing steps | `bash scripts/process_all.sh` |

## Project Structure

```
MB/
├── scripts/           # Analysis toolkit
├── videos/
│   ├── playlist/      # The 9 puzzle-linked videos
│   ├── main/          # Campaign videos (Super Bowl ad + teasers)
│   └── extra/         # Additional linked videos
├── frames/            # Extracted video frames
├── audio/             # Extracted audio files
├── transcripts/       # Whisper transcriptions
├── puzzles/           # Downloaded puzzle grids and solutions
├── barcodes/          # Barcode scan results
├── analysis/          # Analysis notes and findings
├── screenshots/       # Your screenshot clues
├── CLUE_TRACKER.md    # Master clue database
├── CLAUDE_PROMPT.md   # Ready-to-paste Claude Code prompt
└── SETUP_GUIDE.md     # This file
```
