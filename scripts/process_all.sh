#!/usr/bin/env bash
# Process all downloaded videos: extract frames, scan barcodes, transcribe
# Run from the project root: bash scripts/process_all.sh
#
# Uses the venv Python if available, otherwise system python3

# Detect venv python
if [ -x "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
    echo "Using venv Python: $PYTHON"
else
    PYTHON="python3"
    echo "Using system Python: $PYTHON"
fi

echo "=== Processing All Videos ==="

# Phase 1: Extract all frames first (fast)
echo ""
echo "========== PHASE 1: FRAME EXTRACTION =========="
for dir in videos/playlist videos/main videos/extra; do
    [ ! -d "$dir" ] && continue
    echo ""
    echo "--- Extracting frames from $dir ---"

    find "$dir" -maxdepth 1 \( -name "*.mp4" -o -name "*.mkv" -o -name "*.webm" \) | sort | while read -r video; do
        case "$video" in *.f251.*|*.f140.*) continue ;; esac

        basename_noext=$(basename "$video" | sed 's/\.[^.]*$//')
        frame_dir="frames/${basename_noext}"

        # Skip if frames already extracted
        if [ -d "$frame_dir" ] && [ "$(ls "$frame_dir"/*.jpg 2>/dev/null | wc -l)" -gt 10 ]; then
            echo "  SKIP (already done): $video"
            continue
        fi

        echo "  Extracting: $video"
        $PYTHON scripts/extract_frames.py "$video" "$frame_dir" || echo "  WARNING: Frame extraction failed for $video"
    done
done

# Phase 2: Scan all frames for barcodes (fast)
echo ""
echo "========== PHASE 2: BARCODE SCANNING =========="
for frame_dir in frames/*/; do
    [ ! -d "$frame_dir" ] && continue

    # Skip if already scanned
    if [ -f "${frame_dir}barcodes_found.txt" ] || [ -f "${frame_dir}barcodes_scanned.marker" ]; then
        echo "  SKIP (already scanned): $frame_dir"
        continue
    fi

    echo "  Scanning: $frame_dir"
    $PYTHON scripts/scan_barcodes.py "$frame_dir" || echo "  WARNING: Barcode scan failed for $frame_dir"
    # Leave a marker even if no barcodes found so we don't re-scan
    touch "${frame_dir}barcodes_scanned.marker"
done

# Phase 3: Transcribe all videos (SLOW - Whisper)
echo ""
echo "========== PHASE 3: WHISPER TRANSCRIPTION =========="
for dir in videos/playlist videos/main videos/extra; do
    [ ! -d "$dir" ] && continue
    echo ""
    echo "--- Transcribing $dir ---"

    find "$dir" -maxdepth 1 \( -name "*.mp4" -o -name "*.mkv" -o -name "*.webm" \) | sort | while read -r video; do
        case "$video" in *.f251.*|*.f140.*) continue ;; esac

        base="${video%.*}"
        # Skip if already transcribed
        if [ -f "${base}_transcript.txt" ]; then
            echo "  SKIP (already transcribed): $video"
            continue
        fi

        echo "  Transcribing: $video"
        $PYTHON scripts/transcribe.py "$video" || echo "  WARNING: Transcription failed for $video"
    done
done

echo ""
echo "=== All processing complete! ==="
echo "Frames saved to: frames/"
echo "Transcripts saved alongside videos"
echo "Barcode results saved in frame directories"
