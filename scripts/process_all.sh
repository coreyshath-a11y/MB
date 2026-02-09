#!/usr/bin/env bash
# Process all downloaded videos: extract frames, scan barcodes, transcribe
# Run from the project root: bash scripts/process_all.sh

# Don't use set -e -- we want to continue even if one step fails
echo "=== Processing All Videos ==="

# Process each video directory
for dir in videos/playlist videos/main videos/extra; do
    if [ ! -d "$dir" ]; then
        echo "Skipping $dir (not found)"
        continue
    fi

    echo ""
    echo "--- Processing $dir ---"

    # Find all video files (mp4, mkv, webm)
    find "$dir" -maxdepth 1 \( -name "*.mp4" -o -name "*.mkv" -o -name "*.webm" \) | sort | while read -r video; do
        # Skip audio-only files (f251 suffix = audio stream)
        case "$video" in
            *.f251.*) continue ;;
        esac

        basename_noext=$(basename "$video" | sed 's/\.[^.]*$//')
        frame_dir="frames/${basename_noext}"

        echo ""
        echo "Processing: $video"

        # Extract frames at 1fps
        echo "  Extracting frames..."
        python3 scripts/extract_frames.py "$video" "$frame_dir" || echo "  WARNING: Frame extraction failed"

        # Scan for barcodes
        echo "  Scanning for barcodes..."
        python3 scripts/scan_barcodes.py "$frame_dir" || echo "  WARNING: Barcode scan failed (install zbar: brew install zbar)"

        # Transcribe audio
        echo "  Transcribing audio..."
        python3 scripts/transcribe.py "$video" || echo "  WARNING: Transcription failed"
    done
done

echo ""
echo "=== All processing complete! ==="
echo "Frames saved to: frames/"
echo "Transcripts saved alongside videos"
echo "Barcode results saved in frame directories"
