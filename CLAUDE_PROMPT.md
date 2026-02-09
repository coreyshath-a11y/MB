# Claude Code Prompt - Paste This Into Claude Code

Copy everything below the line and paste as your first message in a Claude Code session.

---

I'm working on the MrBeast x Salesforce "Million Dollar Puzzle" — a $1M treasure hunt launched during Super Bowl LX (Feb 8, 2026). Designed by Lone Shark Games. First person to Slack MrBeast the correct code via mrbeast.salesforce.com wins.

STRUCTURE: 9 variety puzzles linked from a YouTube playlist, each yielding partial info. An extraction method (from campaign materials/videos) tells you which letters to pull from each solved grid. Those combine into the final code.

MY FILES:
- videos/playlist/ — The 9 puzzle-linked YouTube videos
- videos/main/ — The 4 campaign videos (Super Bowl ad + 3 teasers)
- videos/extra/ — Additional linked videos
- frames/ — Extracted video frames
- screenshots/ — My screenshot clues from the campaign
- CLUE_TRACKER.md — Master clue database

WHAT I NEED YOU TO DO (use subagents for parallel work):

**PHASE 1: Extract Everything**
1. Extract frames from ALL videos at 1fps using the extract_frames.py script
2. Transcribe all audio using the transcribe.py script
3. Scan every frame for barcodes/QR codes using scan_barcodes.py
4. OCR any text visible in frames
5. Check each video's YouTube description and pinned comments for puzzle links

**PHASE 2: Find & Solve the 9 Variety Puzzles**
Each of the 9 playlist videos has a pinned comment linking to a puzzle (likely on Reddit, posted by user BeastForce67). The known example is a Sudoku variant using LIF(E)CHANGE letters instead of numbers. Find all 9 puzzle links, download the puzzle images, and solve each grid.

**PHASE 3: Analyze Visual Clues**
Key clues identified so far:
- Tank barcode (in bank robbery video) — scan and decode
- Calendar dates circled in red: Jan 1, Feb 2, Mar 1, Mar 3 → "1,2,1,3" or "ABAC" pattern
- Check numbers: routing 650283979, account 5480234354
- "$673" from Slack message "@Accounting the elephant ate $673"
- Camera monitor: B002C004, timecode 4:11:44:18, "Look +1 cube"
- Smoke grenade labeled "{+1=?"
- Belt with colored X pattern (red/green/blue/yellow)
- Jersey numbers: 597,482,374,990,723,240,478,531,109,237,453,499,930
- Four clocks: Tokyo, London, Chicago, New York (specific times = code?)
- Chrome vs matte spheres (binary?)
- Combination lock: 020826 (Super Bowl date)
- Clipboard items first letters: O,M,P,L,R,L,V
- MrBeast GMA hint: "look for some numbers in photos I took at the Super Bowl"

**PHASE 4: Determine Extraction Method**
The key insight: solving each 9x9 grid alone isn't enough. You need ANOTHER piece of info to know WHICH letters to extract from each grid. This extraction method likely comes from the visual clues above.

**CONFIRMED RED HERRINGS:**
- "Red Herring Bank" (it's literally named that)
- The acrostic poem = "THIS MEANS NOTHING I JUST WANTED TO WASTE YOUR TIME LOL"
- The smoking device MrBeast holds and dismisses

Start with Phase 1 and report findings as you go. Flag anything that looks like a cipher, code, or hidden message immediately.
