#!/usr/bin/env bash
# Download all MrBeast puzzle videos
# Run from the project root: bash scripts/download_videos.sh

set -e

echo "=== Downloading 9-Video Puzzle Playlist ==="
yt-dlp -o "videos/playlist/%(playlist_index)s - %(title)s.%(ext)s" \
  "https://www.youtube.com/playlist?list=PLj-VLkYRjRxm5HVGFVpPP5W7jkvvzd1q7" \
  -f 'bv*[height=1080]+ba' --no-overwrites

echo ""
echo "=== Downloading Main Campaign Videos ==="
yt-dlp -o "videos/main/%(title)s.%(ext)s" -f 'bv*[height=1080]+ba' --no-overwrites \
  "https://youtu.be/fg0dpaD7Qzc" \
  "https://youtu.be/JBy1T5IykkU" \
  "https://youtu.be/OBQELGS13XA" \
  "https://youtu.be/8_aIjKi0VLM" \
  "https://youtu.be/rKg5OZNM1aU"

echo ""
echo "=== Downloading Additional Linked Videos ==="
yt-dlp -o "videos/extra/%(title)s.%(ext)s" -f 'bv*[height=1080]+ba' --no-overwrites \
  "https://youtu.be/lb6vdKGFz6Y" \
  "https://youtu.be/06fKka0PXmM" \
  "https://youtu.be/FSr5l7URZTc" \
  "https://youtu.be/vMcyCDz4I6U" \
  "https://youtu.be/vecDOdHnjXE" \
  "https://youtu.be/3FA-SIgLNL4" \
  "https://youtu.be/rULwcNtyFqw" \
  "https://youtu.be/6II_REH0O-o" \
  "https://youtu.be/GhAtk-tHfaY" \
  "https://youtu.be/lzFTf3qWMQk"

echo ""
echo "=== Downloading Unlisted Salesforce Video ==="
yt-dlp -o "videos/extra/salesforce_unlisted.%(ext)s" -f 'bv*[height=1080]+ba' --no-overwrites \
  "https://www.youtube.com/watch?v=bIFXXecjdcM"

echo ""
echo "=== All downloads complete! ==="
echo "Videos saved to: videos/playlist/, videos/main/, videos/extra/"
