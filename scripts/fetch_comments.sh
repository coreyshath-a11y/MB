#!/usr/bin/env bash
# Fetch pinned/top comments from all 9 puzzle playlist videos
# Uses yt-dlp with limited comment count to avoid downloading all 200K+ comments

OUTPUT_DIR="youtube_metadata/comments"
mkdir -p "$OUTPUT_DIR"

# 9 puzzle playlist videos
declare -A VIDEOS
VIDEOS[1]="mwKJfNYwvm8"
VIDEOS[2]="VGvj6bj4Sog"
VIDEOS[3]="cV2gBU6hKfY"
VIDEOS[4]="Xj0Jtjg3lHQ"
VIDEOS[5]="e-If_d_bzfI"
VIDEOS[6]="U_LlX4t0A9I"
VIDEOS[7]="lOKASgtr6kU"
VIDEOS[8]="NDsO1LT_0lw"
VIDEOS[9]="yXWw0_UfSFg"

echo "=== Fetching Top Comments for 9 Puzzle Videos ==="

for num in $(seq 1 9); do
    vid="${VIDEOS[$num]}"
    echo ""
    echo "[$num/9] Fetching comments for $vid..."

    # Use --extractor-args to limit: max_comments=top_level,per_thread,total,max_parents
    # We want: 50 top-level comments, 5 replies each, sorted by top
    yt-dlp --skip-download \
        --write-info-json \
        --extractor-args "youtube:max_comments=50,5,100;comment_sort=top" \
        -o "$OUTPUT_DIR/${num}_${vid}" \
        "https://www.youtube.com/watch?v=${vid}" 2>&1 | tail -5

    # Extract just the comments from the info.json
    INFO_FILE="$OUTPUT_DIR/${num}_${vid}.info.json"
    if [ -f "$INFO_FILE" ]; then
        # Use python to extract comments into a readable format
        venv/bin/python -c "
import json, sys
with open('$INFO_FILE') as f:
    data = json.load(f)
comments = data.get('comments', [])
print(f'  Found {len(comments)} comments')

# Write readable comments file
with open('$OUTPUT_DIR/${num}_comments.txt', 'w') as out:
    out.write(f'VIDEO #{num}: {data.get(\"title\", \"Unknown\")}\\n')
    out.write(f'URL: https://www.youtube.com/watch?v=${vid}\\n')
    out.write('=' * 60 + '\\n\\n')

    pinned = [c for c in comments if c.get('is_pinned')]
    if pinned:
        out.write('*** PINNED COMMENT(S) ***\\n')
        for c in pinned:
            out.write(f'Author: {c.get(\"author\", \"?\")}\\n')
            out.write(f'Likes: {c.get(\"like_count\", 0)}\\n')
            out.write(f'Text: {c.get(\"text\", \"\")}\\n\\n')

    out.write('\\nTOP COMMENTS (by likes):\\n')
    out.write('-' * 40 + '\\n')
    sorted_comments = sorted(comments, key=lambda x: -x.get('like_count', 0))
    for i, c in enumerate(sorted_comments[:30]):
        pinned_tag = ' [PINNED]' if c.get('is_pinned') else ''
        hearted = ' [HEARTED]' if c.get('is_favorited') else ''
        out.write(f'\\n#{i+1}{pinned_tag}{hearted} ({c.get(\"like_count\", 0)} likes) - {c.get(\"author\", \"?\")}:\\n')
        out.write(f'{c.get(\"text\", \"\")}\\n')
" 2>&1
    else
        echo "  WARNING: No info.json generated"
    fi
done

echo ""
echo "=== Comment fetch complete! ==="
echo "Results in: $OUTPUT_DIR/"

# Create combined pinned comments file
echo ""
echo "Creating combined pinned comments file..."
venv/bin/python -c "
import json, glob, os

output_dir = '$OUTPUT_DIR'
combined = open(os.path.join(output_dir, 'ALL_PINNED_COMMENTS.txt'), 'w')
combined.write('PINNED COMMENTS FROM ALL 9 PUZZLE VIDEOS\n')
combined.write('=' * 60 + '\n\n')

for num in range(1, 10):
    pattern = os.path.join(output_dir, f'{num}_*.info.json')
    files = glob.glob(pattern)
    if not files:
        combined.write(f'\nVIDEO #{num}: No data\n')
        continue

    with open(files[0]) as f:
        data = json.load(f)

    title = data.get('title', 'Unknown')
    combined.write(f'\n{\"#\" * 50}\n')
    combined.write(f'VIDEO #{num}: {title}\n')
    combined.write(f'{\"#\" * 50}\n')

    comments = data.get('comments', [])
    pinned = [c for c in comments if c.get('is_pinned')]

    if pinned:
        for c in pinned:
            combined.write(f'Author: {c.get(\"author\", \"?\")}\n')
            combined.write(f'Likes: {c.get(\"like_count\", 0)}\n')
            combined.write(f'Text:\n{c.get(\"text\", \"\")}\n\n')
    else:
        combined.write('No pinned comment found\n')

    # Also note top 3 most-liked comments
    if comments:
        top = sorted(comments, key=lambda x: -x.get('like_count', 0))[:3]
        combined.write('\nTop 3 by likes:\n')
        for c in top:
            combined.write(f'  [{c.get(\"like_count\", 0)} likes] {c.get(\"author\", \"?\")}: {c.get(\"text\", \"\")[:150]}\n')

combined.close()
print('Combined pinned comments saved!')
" 2>&1
