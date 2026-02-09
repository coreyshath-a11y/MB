#!/usr/bin/env bash
# Process all downloaded videos: extract frames, scan barcodes, transcribe
# Run from the project root: bash scripts/process_all.sh

set -e

echo "=== Processing All Videos ==="

# Process each video directory
for dir in videos/playlist videos/main videos/extra; do
    if [ ! -d "$dir" ]; then
        echo "Skipping $dir (not found)"
        continue
    fi

    echo ""
    echo "--- Processing $dir ---"

    for video in "$dir"/*.{mp4,mkv,webm} 2>/dev/null; do
        [ -f "$video" ] || continue

        basename=$(basename "$video" | sed 's/\.[^.]*$//')
        frame_dir="frames/${basename}"

        echo ""
        echo "Processing: $video"

        # Extract frames at 1fps
        echo "  Extracting frames..."
        python3 scripts/extract_frames.py "$video" "$frame_dir"

        # Scan for barcodes
        echo "  Scanning for barcodes..."
        python3 scripts/scan_barcodes.py "$frame_dir"

        # Transcribe audio
        echo "  Transcribing audio..."
        python3 scripts/transcribe.py "$video"
    done
done

echo ""
echo "=== All processing complete! ==="
echo "Frames saved to: frames/"
echo "Transcripts saved alongside videos"
echo "Barcode results saved in frame directories"
