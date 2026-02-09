#!/usr/bin/env python3
"""Fetch YouTube video metadata (titles, descriptions, pinned comments, top comments) using yt-dlp."""
import subprocess
import json
import os
import sys

# The 9 puzzle playlist videos
PLAYLIST_VIDEOS = {
    "1": "mwKJfNYwvm8",
    "2": "VGvj6bj4Sog",
    "3": "cV2gBU6hKfY",
    "4": "Xj0Jtjg3lHQ",
    "5": "e-If_d_bzfI",
    "6": "U_LlX4t0A9I",
    "7": "lOKASgtr6kU",
    "8": "NDsO1LT_0lw",
    "9": "yXWw0_UfSFg",
}

# Main campaign videos
MAIN_VIDEOS = {
    "superbowl_ad": "9bqk6ZGDSmQ",
    "rewatch": "gKEHdfxe6do",
    "salesforce_talk": "LkXLfalrmNg",
    "slack_build": "LTqbSVMxMoQ",
    "first_to_find": "LuV0dDjYNUQ",
}


def fetch_metadata(video_id, output_dir, get_comments=True):
    """Fetch metadata for a single video using yt-dlp."""
    url = f"https://www.youtube.com/watch?v={video_id}"

    # Get basic metadata as JSON
    cmd = ["yt-dlp", "--dump-json", "--no-download", url]
    if get_comments:
        cmd.extend(["--extractor-args", "youtube:comment_sort=top;max_comments=100,30,30,10"])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"  Error fetching {video_id}: {result.stderr[:200]}")
            return None

        data = json.loads(result.stdout)

        # Extract the key fields we care about
        metadata = {
            "video_id": video_id,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "upload_date": data.get("upload_date", ""),
            "duration": data.get("duration", 0),
            "view_count": data.get("view_count", 0),
            "channel": data.get("channel", ""),
            "tags": data.get("tags", []),
        }

        # Extract comments
        comments = data.get("comments", [])
        if comments:
            metadata["comments"] = []
            for c in comments:
                comment_data = {
                    "author": c.get("author", ""),
                    "text": c.get("text", ""),
                    "like_count": c.get("like_count", 0),
                    "is_pinned": c.get("is_pinned", False),
                    "is_favorited": c.get("is_favorited", False),
                    "timestamp": c.get("timestamp", 0),
                }
                metadata["comments"].append(comment_data)

            # Sort: pinned first, then by likes
            metadata["comments"].sort(
                key=lambda x: (-int(x.get("is_pinned", False)), -x.get("like_count", 0))
            )

        # Save full metadata JSON
        outfile = os.path.join(output_dir, f"{video_id}_metadata.json")
        with open(outfile, "w") as f:
            json.dump(metadata, f, indent=2)

        # Save human-readable summary
        txtfile = os.path.join(output_dir, f"{video_id}_summary.txt")
        with open(txtfile, "w") as f:
            f.write(f"TITLE: {metadata['title']}\n")
            f.write(f"VIDEO ID: {video_id}\n")
            f.write(f"URL: https://www.youtube.com/watch?v={video_id}\n")
            f.write(f"UPLOAD DATE: {metadata['upload_date']}\n")
            f.write(f"DURATION: {metadata['duration']}s\n")
            f.write(f"TAGS: {', '.join(metadata.get('tags', []))}\n")
            f.write(f"\n{'='*60}\nDESCRIPTION:\n{'='*60}\n")
            f.write(metadata['description'] + "\n")

            if metadata.get("comments"):
                f.write(f"\n{'='*60}\nTOP COMMENTS ({len(metadata['comments'])} fetched):\n{'='*60}\n")
                for i, c in enumerate(metadata["comments"]):
                    pinned = " [PINNED]" if c.get("is_pinned") else ""
                    favorited = " [HEARTED]" if c.get("is_favorited") else ""
                    f.write(f"\n--- Comment #{i+1}{pinned}{favorited} ({c['like_count']} likes) ---\n")
                    f.write(f"Author: {c['author']}\n")
                    f.write(f"{c['text']}\n")

        return metadata

    except subprocess.TimeoutExpired:
        print(f"  Timeout fetching {video_id}")
        return None
    except Exception as e:
        print(f"  Exception fetching {video_id}: {e}")
        return None


def main():
    output_dir = "youtube_metadata"
    os.makedirs(output_dir, exist_ok=True)

    # Combined report
    all_metadata = {}

    print("=== Fetching YouTube Metadata for Puzzle Videos ===\n")

    # Fetch playlist videos
    for num, vid_id in sorted(PLAYLIST_VIDEOS.items()):
        print(f"[{num}/9] Fetching playlist video: {vid_id}")
        meta = fetch_metadata(vid_id, output_dir)
        if meta:
            all_metadata[f"puzzle_{num}"] = meta
            title = meta.get("title", "Unknown")
            n_comments = len(meta.get("comments", []))
            pinned = [c for c in meta.get("comments", []) if c.get("is_pinned")]
            print(f"  Title: {title}")
            print(f"  Comments: {n_comments} total, {len(pinned)} pinned")

    print("\n=== Fetching Main Campaign Videos ===\n")

    # Fetch main campaign videos
    for label, vid_id in MAIN_VIDEOS.items():
        print(f"Fetching {label}: {vid_id}")
        meta = fetch_metadata(vid_id, output_dir)
        if meta:
            all_metadata[label] = meta
            print(f"  Title: {meta.get('title', 'Unknown')}")

    # Save combined report
    combined_file = os.path.join(output_dir, "ALL_METADATA.json")
    with open(combined_file, "w") as f:
        json.dump(all_metadata, f, indent=2)

    # Create a master puzzle clues file
    clues_file = os.path.join(output_dir, "PUZZLE_CLUES_FROM_YOUTUBE.txt")
    with open(clues_file, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("PUZZLE CLUES EXTRACTED FROM YOUTUBE METADATA\n")
        f.write("=" * 70 + "\n\n")

        for num in sorted(PLAYLIST_VIDEOS.keys()):
            key = f"puzzle_{num}"
            if key in all_metadata:
                meta = all_metadata[key]
                f.write(f"\n{'#' * 60}\n")
                f.write(f"PUZZLE VIDEO #{num}: {meta['title']}\n")
                f.write(f"URL: https://www.youtube.com/watch?v={meta['video_id']}\n")
                f.write(f"{'#' * 60}\n\n")

                f.write("DESCRIPTION:\n")
                f.write(meta['description'] + "\n\n")

                pinned = [c for c in meta.get("comments", []) if c.get("is_pinned")]
                if pinned:
                    f.write("PINNED COMMENT(S):\n")
                    for c in pinned:
                        f.write(f"  Author: {c['author']}\n")
                        f.write(f"  Text: {c['text']}\n\n")

                hearted = [c for c in meta.get("comments", []) if c.get("is_favorited")]
                if hearted:
                    f.write("HEARTED/FAVORITED COMMENT(S):\n")
                    for c in hearted:
                        f.write(f"  Author: {c['author']}\n")
                        f.write(f"  Text: {c['text']}\n\n")

    print(f"\n=== Done! ===")
    print(f"Individual files: {output_dir}/<video_id>_metadata.json")
    print(f"Combined data: {combined_file}")
    print(f"Puzzle clues: {clues_file}")


if __name__ == "__main__":
    main()
