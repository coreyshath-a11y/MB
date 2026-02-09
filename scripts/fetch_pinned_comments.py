#!/usr/bin/env python3
"""Fetch pinned comments from all 9 puzzle playlist videos using yt-dlp."""
import subprocess
import json
import os

VIDEOS = [
    ("1", "mwKJfNYwvm8", "I Built 100 Wells In Africa"),
    ("2", "VGvj6bj4Sog", "Changing the Lives of 600 Strangers"),
    ("3", "cV2gBU6hKfY", "I Cleaned The World's Dirtiest Beach #TeamSeas"),
    ("4", "Xj0Jtjg3lHQ", "$1 vs $500,000 Experiences!"),
    ("5", "e-If_d_bzfI", "POKEMON GO STEREOTYPES"),
    ("6", "U_LlX4t0A9I", "$10,000 Every Day You Survive In The Wilderness"),
    ("7", "lOKASgtr6kU", "I Adopted 100 Dogs!"),
    ("8", "NDsO1LT_0lw", "I Spent 100 Hours Inside The Pyramids!"),
    ("9", "yXWw0_UfSFg", "Anything You Can Fit In The Circle I'll Pay For"),
]

OUTPUT_DIR = "youtube_metadata/comments"
os.makedirs(OUTPUT_DIR, exist_ok=True)

all_pinned = []

for num, vid_id, title in VIDEOS:
    print(f"\n[{num}/9] Fetching comments for: {title} ({vid_id})")
    outpath = os.path.join(OUTPUT_DIR, f"{num}_{vid_id}")
    info_file = outpath + ".info.json"

    # Skip if already downloaded with comments
    if os.path.exists(info_file):
        with open(info_file) as f:
            data = json.load(f)
        if data.get("comments"):
            print(f"  Already have {len(data['comments'])} comments, skipping download")
            comments = data["comments"]
        else:
            comments = None
    else:
        comments = None

    if comments is None:
        cmd = [
            "yt-dlp", "--skip-download", "--write-comments", "--write-info-json",
            "--extractor-args", "youtube:max_comments=100,100,0,0",
            "-o", outpath,
            f"https://www.youtube.com/watch?v={vid_id}"
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if os.path.exists(info_file):
                with open(info_file) as f:
                    data = json.load(f)
                comments = data.get("comments", [])
            else:
                print(f"  ERROR: No info.json generated")
                comments = []
        except subprocess.TimeoutExpired:
            print(f"  TIMEOUT")
            comments = []

    print(f"  Got {len(comments)} comments")

    # Find pinned comments
    pinned = [c for c in comments if c.get("is_pinned")]
    hearted = [c for c in comments if c.get("is_favorited") and not c.get("is_pinned")]

    if pinned:
        for c in pinned:
            print(f"  PINNED by {c['author']}: {c['text'][:200]}")
            all_pinned.append({
                "video_num": num,
                "video_id": vid_id,
                "title": title,
                "author": c["author"],
                "text": c["text"],
                "likes": c.get("like_count", 0),
            })
    else:
        print(f"  No pinned comment found!")
        # Check top comments
        top = sorted(comments, key=lambda x: -(x.get("like_count") or 0))[:3]
        for c in top:
            print(f"  Top comment ({c.get('like_count',0)} likes) {c.get('author','?')}: {c.get('text','')[:100]}")

    if hearted:
        print(f"  Also {len(hearted)} hearted comment(s)")

    # Save individual readable file
    txt_file = os.path.join(OUTPUT_DIR, f"{num}_comments.txt")
    with open(txt_file, "w") as f:
        f.write(f"VIDEO #{num}: {title}\n")
        f.write(f"URL: https://www.youtube.com/watch?v={vid_id}\n")
        f.write(f"Total comments fetched: {len(comments)}\n")
        f.write("=" * 60 + "\n\n")

        if pinned:
            f.write("*** PINNED COMMENT(S) ***\n")
            for c in pinned:
                f.write(f"Author: {c.get('author', '?')}\n")
                f.write(f"Likes: {c.get('like_count', 0)}\n")
                f.write(f"Text: {c.get('text', '')}\n\n")

        f.write("\nTOP COMMENTS (by likes):\n")
        f.write("-" * 40 + "\n")
        sorted_comments = sorted(comments, key=lambda x: -(x.get("like_count") or 0))
        for i, c in enumerate(sorted_comments[:20]):
            p = " [PINNED]" if c.get("is_pinned") else ""
            h = " [HEARTED]" if c.get("is_favorited") else ""
            f.write(f"\n#{i+1}{p}{h} ({c.get('like_count', 0)} likes) - {c.get('author', '?')}:\n")
            f.write(f"{c.get('text', '')}\n")

# Save combined pinned comments file
combined_file = os.path.join(OUTPUT_DIR, "ALL_PINNED_COMMENTS.txt")
with open(combined_file, "w") as f:
    f.write("=" * 60 + "\n")
    f.write("PINNED COMMENTS FROM ALL 9 PUZZLE VIDEOS\n")
    f.write("=" * 60 + "\n\n")
    for p in all_pinned:
        f.write(f"VIDEO #{p['video_num']}: {p['title']}\n")
        f.write(f"Author: {p['author']} ({p['likes']} likes)\n")
        f.write(f"Text: {p['text']}\n")
        f.write("-" * 40 + "\n\n")

# Save as JSON too
json_file = os.path.join(OUTPUT_DIR, "ALL_PINNED_COMMENTS.json")
with open(json_file, "w") as f:
    json.dump(all_pinned, f, indent=2)

print(f"\n=== Done! ===")
print(f"Found {len(all_pinned)} pinned comments across 9 videos")
print(f"Combined file: {combined_file}")
