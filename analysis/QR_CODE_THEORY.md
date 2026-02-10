# QR Code Crossword Theory
## Last Updated: Feb 10, 2026

## The Theory
Someone in the community suggested the crossword might double as a QR code. Mike Selinker (Lone Shark Games) is known for innovative crossword puzzles, and the crossword grid is **exactly 21x21** — which is the exact size of a **Version 1 QR code**.

## Key Facts

### QR Code Version 1 Structure (21x21)
- 21 x 21 modules (cells)
- 3 "finder patterns" (7x7 squares) in top-left, top-right, bottom-left corners
- Each finder pattern: black border → white border → black 3x3 center
- Alignment patterns, timing patterns between finders
- Data encoded in remaining cells

### Our Crossword
- 21 x 21 cells
- Has black cells (blocked) and white cells (letter cells)
- Black cells in standard crossword puzzles are decorative/structural
- 167 Across clue mentions "eleven hidden words" — not QR-related language

## Analysis: Does the Grid Match QR Structure?

### Against the Theory:
1. **Top-left corner**: Row 1 of the crossword starts with cells 1-7 (all white/numbered). A QR code needs a 7x7 black-bordered square in the top-left. The crossword has white cells there.
2. **Symmetry**: Standard crosswords have 180° rotational symmetry for black cells. QR codes do NOT have this symmetry.
3. **Black cell density**: QR codes have roughly 50% black/white. Crosswords typically have 15-20% black cells.
4. **Mike Selinker** — no confirmed examples of QR code crosswords found in search results, though his LiveJournal has a "QR code" tag.

### For the Theory:
1. **Perfect size match**: 21x21 is suspicious.
2. **Selinker is innovative**: He's done 10-foot crossword walls, combined puzzles with narrative games, etc.
3. **The puzzle has no clues**: Maybe the grid structure IS the message.
4. **"Behind the scenes" hint**: "Look up, down, forward, backward, and behind the scenes."

## Alternative QR-Related Theories

### Theory A: Filled Grid Forms QR
Instead of black cells = QR modules, maybe **specific letters in the filled grid** map to black modules. For example:
- Vowels = white, consonants = black
- Or: certain letters (from a key) = black

### Theory B: Circled Cells Form QR
The circled cells, when mapped, might form a mini QR code or barcode.

### Theory C: Crossword Answers Encode QR Data
The answers themselves, when read in some order, spell out data that can be encoded as a QR code leading to the prize URL.

### Theory D: Staircase Grid Is QR-Related
The staircase grid (bottom-right) might be a QR fragment or decoder for the main grid.

## Status: INTERESTING BUT UNCONFIRMED
The 21x21 size match is notable but the grid structure appears to contradict standard QR code patterns. Worth keeping in mind as we fill in the grid.

## How a Crossword→QR Would Work (If True)
1. Fill in ALL crossword answers
2. Map filled grid to binary (some rule: certain letters = black, others = white)
3. The resulting 21x21 binary pattern forms a scannable QR code
4. QR code resolves to a URL or final answer
5. Submit that answer via Slackbot

This would be clever because:
- You CAN'T generate the QR code without solving the entire crossword first
- The QR code is a verification mechanism (if it scans, your grid is correct)
- It provides a unique submission URL per correct solve
