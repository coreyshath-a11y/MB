# SESSION STATE - Saved Feb 9, 2026

## WHAT THIS PROJECT IS
MrBeast x Salesforce Million Dollar Puzzle contest. User has local Claude Code CLI processing videos and data, pushing to GitHub repo `coreyshath-a11y/MB` on branch `claude/setup-github-cloud-j9k6O` so a cloud-based Claude instance can solve the puzzles.

## WHAT'S BEEN DONE
### Processing Complete
- All 9 playlist videos downloaded, frames extracted (1fps), barcodes scanned, transcribed with Whisper
- All 9 pinned comments found with puzzle image links
- All 9 puzzle images collected in `puzzles/` directory
- YouTube metadata fetched for all videos
- Barcode scan: NO puzzle-relevant barcodes found (only sponsor QR codes)
- T&C read and summarized → `analysis/TERMS_AND_CONDITIONS_SUMMARY.md`
- Gemini Deep Research read and key findings extracted → `analysis/GEMINI_RESEARCH_KEY_FINDINGS.md`
- Behind-the-scenes video transcript read → `How @MrBeast Scaled Beast Industries...txt`

### 4 Commits Pushed to GitHub
1. d5a3010 - Puzzle images, YouTube metadata, pinned comments
2. d4c7c94 - Transcripts (1-5), barcode analysis, YouTube comments
3. 2e09055 - Transcripts (6-7)
4. d09285e - Final transcripts (8-9)

### Commit 5 (7c2f3ec) - JUST PUSHED
- T&C summary, Gemini research findings, crossword PDF
- Behind-the-scenes transcript, Terms and Conditions RTF
- 28 Super Bowl ad screenshots → `screenshots/superbowl_ad/`
- 15 Instagram screenshots → `screenshots/instagram/`
- Screenshot index with visible numbers documented
- Remaining puzzle image originals and YouTube metadata JSONs
- Session state file

## WHAT NEEDS TO BE DONE NEXT
1. **Copy Instagram screenshots from ~/Desktop into the repo** (user just said they added them)
2. **Move all 28+ screenshots from repo root into `screenshots/` directory** for organization
3. **Push ALL unpushed files to GitHub** - T&C summary, Gemini findings, crossword PDF, screenshots, remaining puzzle/metadata files
4. **Search for MrBeast Super Bowl photos with hidden numbers** - MrBeast said on GMA: "look for some numbers in photos that I took at the Super Bowl"
   - Check @MrBeast on X and @mrbeast on Instagram for Feb 8-9 2026 posts
   - Look for visible numbers in photos (jerseys, signs, backgrounds, etc.)
5. **Monitor for 24hr/48hr hints** - puzzle launched Feb 8 6pm ET, so 24hr mark = Feb 9 6pm ET

## KEY PUZZLE INTEL
- **Answer = "hidden code"** submitted via Slackbot at mrbeast.salesforce.com
- **9 puzzles** from YouTube playlist pinned comments + **10th crossword puzzle** (Million-Dollar-Crossword.pdf)
- **Puzzle letters use LIFECHANG(E)** alphabet (not 1-9)
- **Lone Shark Games** designed it (Mike Selinker)
- **Confirmed red herrings:** Red Herring Bank, acrostic poem, smoke device
- **Visual clues in Super Bowl commercial:** $10^5 on monitor, spider, sine wave, elephant, bird on wire
- **"Look +1 cube"** instruction on camera monitor
- **Calendar dates:** Jan 1, Feb 2, Mar 1, Mar 3 → pattern 1,2,1,3
- **13 jersey numbers:** 597, 482, 374, 990, 723, 240, 478, 531, 109, 237, 453, 499, 930
- **Nobody is close** as of Feb 9

## TECHNICAL SETUP
- Python venv at `~/Desktop/mb/venv` with Python 3.14
- Packages: opencv-python, openai-whisper, pyzbar, yt-dlp
- zbar installed via homebrew
- Git branch: `claude/setup-github-cloud-j9k6O`
- Remote: origin → github.com/coreyshath-a11y/MB

## FILE STRUCTURE
```
/Users/coreyhathaway/Desktop/mb/
├── .claude/SESSION_STATE.md (this file)
├── .gitignore
├── CLAUDE_PROMPT.md
├── CLUE_TRACKER.md
├── PUZZLE_INDEX.md
├── SETUP_GUIDE.md
├── Million-Dollar-Crossword.pdf
├── Terms and Conditions.rtf
├── How @MrBeast Scaled Beast Industries...txt
├── Gemini Deep Research.rtfd/ (Mac rich text bundle)
├── Screenshot 2026-02-09 at *.png (28 files - NEED TO ORGANIZE)
├── analysis/
│   ├── barcode_results.txt
│   ├── TERMS_AND_CONDITIONS_SUMMARY.md
│   └── GEMINI_RESEARCH_KEY_FINDINGS.md
├── puzzles/ (9 puzzle images + originals)
├── transcripts/ (9 .txt transcript files)
├── youtube_metadata/ (JSON + summary files + comments/)
├── scripts/ (process_all.sh, extract_frames.py, scan_barcodes.py, transcribe.py, fetch_*.py)
├── frames/ (extracted video frames, gitignored)
├── videos/ (downloaded videos, gitignored)
├── audio/ (gitignored)
├── barcodes/ (gitignored)
├── docs/
└── screenshots/ (empty - need to move screenshots here)
```
