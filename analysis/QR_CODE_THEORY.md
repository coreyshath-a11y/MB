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

## TESTED: Black Cells Do NOT Form QR Code ❌

Programmatic analysis confirms the crossword black cells do NOT form a QR code:

```
Extracted black cell pattern:
R01: ░░░░░░██░░░░░█░░░░░░░
R02: ░░░░░░█░░░░░░█░░░░░░░
R03: ░░░░░░░░░░░░░█░░░░░░░
R04: ░░░███░░░█░░░░░░░░░░░
R05: ░░░█░░░█░░░█░░░██░░░░
R06: ░░░░░░░░░░░░░█░░░░░██
R07: ░░░░░░░░░░░░█░░░░█░░░
R08: ███░░░░░█░░░░░░░░░░░░
R09: ░░░░█░░░░█░░░░█░░░█░░
R10: ░░░░░█░░░░░░░░░█░░░░░
R11: ░░░░░░█░░░░█░░░░█░░░░
R12: ░░░░░░░░░░░░█░░░░░███
R13: ░░░█░░░░█░░░░░░░░░░░░
R14: ██░░░░░█░░░░░░░░░░░░░
R15: ░░░░██░░░█░░░█░░░█░░░
R16: ░░░░░░░░░░░█░░░███░░░
R17: ░░░░░░░█░░░░░░░░░░░░░
R18: ░░░░░░░█░░░░░░█░░░░░░
R19: ░░░░░░░░░░░░░░░░░░░░░
R20: ░░░░░░░░░░░░░░░░░░░░░
R21: ░░░░░░░░░░░░░░░░░░░░░

Black cells: 54 / 441 = 12.2% (QR needs ~50%)
```

**Failures:**
- No QR finder patterns in any corner (needs 24 black cells per corner, top-left has 6)
- Inverted (white=black) also fails
- pyzbar QR scanner: "NO QR DETECTED" for normal, inverted, and bordered versions
- Black cell count (54) is far too low for QR (needs ~220)

**Interesting observations:**
- Rows 19-21 have ZERO black cells (unusual for crossword)
- Grid does NOT have standard 180° rotational symmetry (very unusual)
- The 21x21 size match appears to be coincidence

## Status: BLACK CELLS ALONE AS QR = DISPROVEN
The filled-letter mapping theory (Theory A) is still untested.

## NEW: Vault Door Overlap Theory (from community image)

### Source: `screenshots/Possible QR overlap from video.png`

The community discovered that the vault door in the video has raised bumps arranged in two groups (left side and right side). When these bump patterns are mapped onto the 21×21 crossword grid:

1. **Left side bumps** → mapped as black cells on left portion of grid
2. **Right side bumps** → mapped as black cells on right portion of grid
3. **The two halves don't overlap** ("not doubling up")
4. **Combined overlay** shown in red (one side) and blue (other side)

### What This Means
The vault door bumps + crossword black cells together might form a MORE COMPLETE binary pattern:
- Crossword black cells = ~54 cells (12.2%)
- Vault door bumps (left) = additional dark cells
- Vault door bumps (right) = additional dark cells
- **Combined total might approach ~220 cells (50%)** needed for QR code

### Analysis of the Overlay Image
- Red pixels (one vault side): ~25K pixels in overlay area
- Blue pixels (other vault side): ~16K pixels in overlay area
- White (empty): ~50K pixels
- Red:Blue:White ≈ 27%:18%:55% → combined dark ≈ 45% (close to QR's 50%!)

### Next Steps for QR Theory
1. Extract exact cell-by-cell pattern from the colored overlay
2. Combine with known crossword black cells
3. Test if the combined 21×21 binary pattern forms a valid QR code
4. Check for QR finder patterns (7×7 squares in 3 corners)
5. If valid → scan → should give URL or answer code

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

---

## UPDATE (Feb 10, 2026): Grid Confirmed as 25x25 — QR Code Version 2 Analysis

### Corrected Grid Size
The crossword grid has been confirmed as **25x25**, not 21x21 as previously assumed. This changes the analysis significantly because:
- **QR Code Version 1** = 21x21 (previous analysis, now moot)
- **QR Code Version 2** = 25x25 (exact match with the confirmed grid size)

QR code versions increase by 4 modules per side: V1=21, V2=25, V3=29, V4=33, etc.

---

### QR Code Version 2 (25x25) — Complete Technical Specification

#### Grid Layout
- **Total modules:** 625 (25 x 25)
- **Functional pattern modules:** ~266 (non-data)
- **Data modules:** ~359 (available for encoding)

#### Three Finder Patterns (7x7 each)
Each finder pattern is a concentric square: outer 7x7 black border, inner 5x5 white border, center 3x3 solid black.

Placement in 25x25 grid:
- **Top-left:** rows 0-6, columns 0-6
- **Top-right:** rows 0-6, columns 18-24
- **Bottom-left:** rows 18-24, columns 0-6
- **Bottom-right:** EMPTY (no finder pattern — this is what distinguishes QR orientation)

Each finder pattern includes a 1-module-wide white separator on its interior-facing edges:
- Top-left separator: column 7 and row 7
- Top-right separator: column 17 and row 7
- Bottom-left separator: column 7 and row 17

#### Single Alignment Pattern (5x5)
Version 2 has exactly ONE alignment pattern (center at row 18, column 18):
- 5x5 black outer square
- 3x3 white inner square
- 1x1 black center module
- Occupies rows 16-20, columns 16-20

(Three other candidate positions at (6,6), (6,18), (18,6) are omitted because they overlap with finder patterns.)

#### Timing Patterns
Alternating black-white modules along:
- **Row 6** (horizontal): from column 8 to column 16 (9 modules)
- **Column 6** (vertical): from row 8 to row 16 (9 modules)

#### Dark Module
One mandatory black module at position (row 17, column 8) — always present.

#### Format Information
15-bit format string placed in two copies around the finder patterns, encoding:
- Error correction level (2 bits: L/M/Q/H)
- Mask pattern (3 bits: 0-7)
- 10-bit BCH error correction for the format string itself

#### Data Capacity (Version 2)

| EC Level | Recovery | Numeric | Alphanumeric | Byte | Kanji |
|----------|----------|---------|--------------|------|-------|
| L (7%)   | Low      | 77      | 47           | 32   | 20    |
| M (15%)  | Medium   | 63      | 38           | 26   | 16    |
| Q (25%)  | Quartile | 48      | 29           | 20   | 12    |
| H (30%)  | High     | 34      | 20           | 14   | 8     |

Key takeaway: A Version 2 QR code can encode **20 to 47 alphanumeric characters** (or **14 to 32 bytes**) depending on error correction level. This is enough for a short URL like `mrbeast.salesforce.com/ANSWER` or a short code.

---

### Is 25x25 a Valid Size for OTHER 2D Barcode Formats?

#### Data Matrix (ECC 200) — NO
- Data Matrix ECC 200 requires an **even** number of rows and columns
- Valid sizes near 25: 24x24 and 26x26
- **25x25 is NOT a valid Data Matrix ECC 200 size**

#### Data Matrix (ECC 000-140, Legacy) — TECHNICALLY YES
- Legacy Data Matrix uses **odd** numbered sizes from 9x9 to 49x49
- 25x25 falls within this range
- However, ECC 000-140 is deprecated per ISO/IEC 16022 and almost never used
- Uses convolutional error correction (unreliable at large sizes)
- **Extremely unlikely** to be the intended format

#### Aztec Code — NO
- Compact Aztec: 15x15, 19x19, 23x23, 27x27 (jumps by 4)
- Full-range Aztec: 19x19, 23x23, 27x27, 31x31... (also jumps by 4)
- **25x25 is NOT a valid Aztec Code size** for either compact or full-range
- The step size of 4 (from 2-ring layers) means Aztec skips 25 entirely

#### Summary Table

| Format | Valid at 25x25? | Notes |
|--------|-----------------|-------|
| QR Code Version 2 | YES | Exact match |
| Data Matrix ECC 200 | NO | Even sizes only |
| Data Matrix ECC 000-140 | Technically | Deprecated, unreliable |
| Aztec Compact | NO | Goes 23 -> 27 |
| Aztec Full-Range | NO | Goes 23 -> 27 |
| Aztec Rune | NO | Fixed 11x11 |

**Conclusion: QR Code Version 2 is the ONLY standard modern 2D barcode format that uses exactly 25x25 modules.**

---

### Mapping Theory Analysis (Updated for 25x25)

#### Theory A: Black Cells = Black Modules (STILL FAILS)
- The crossword has approximately 50-80 black cells out of 625 total (~8-13%)
- A valid QR code needs approximately 50% dark modules (~312 of 625)
- Black cells alone are far too sparse
- **VERDICT: Insufficient density. Would need massive supplementation.**

#### Theory B: Filled Letters Map to Black/White
- After solving, each of 625 cells contains either a letter or is black
- Some mapping rule converts letters to binary (dark/light modules):
  - Possible rule: letter position in alphabet modulo 2 (odd = dark, even = light)
  - Possible rule: vowels vs consonants
  - Possible rule: letters in a key word (e.g., "MRBEAST") = dark
  - Possible rule: letter frequency or Scrabble values above/below threshold
- This theory could produce ~50% density if the rule is well-chosen
- **VERDICT: Plausible but untestable until grid is fully solved.**

#### Theory C: Crossword + Vault Door Overlay = QR Code
- Previous analysis (at 21x21) showed vault door bumps added significant dark cells
- Combined overlay reached ~45% dark (close to 50%)
- **If the grid is actually 25x25**, the vault door mapping needs to be re-examined:
  - Does the vault door have enough bumps to fill a 25x25 grid?
  - The vault door overlay image was made for 21x21 — may need rescaling
  - 25x25 = 625 cells; need ~312 dark. If crossword provides ~70 and vault provides ~240, total is ~310 (close!)
- **VERDICT: Needs re-analysis with correct 25x25 grid dimensions.**

#### Theory D: No Barcode — Circled Cells Spell Answer Directly
- The crossword has circled cells (~13-16)
- After filling the grid, read circled cell letters in order to get a submission code
- This is the standard meta-crossword mechanism
- No QR code needed at all
- **VERDICT: Most likely correct mechanism. QR code theory is probably unnecessary.**

---

### Critical Structural Test: Does the Crossword Grid Match QR Finder Pattern Positions?

For the 25x25 grid to be a QR code, the following cells MUST be specific colors:

**Top-left finder (rows 0-6, cols 0-6):**
Must contain a 7x7 pattern with specific black/white arrangement. In the crossword, these cells are the top-left corner — they should contain a mixture of black cells and letter cells matching the finder pattern exactly.

**Top-right finder (rows 0-6, cols 18-24):**
Same 7x7 pattern in the top-right corner of the crossword.

**Bottom-left finder (rows 18-24, cols 0-6):**
Same 7x7 pattern in the bottom-left corner of the crossword.

**Alignment pattern (rows 16-20, cols 16-20):**
Must contain a 5x5 black-white-black concentric square pattern.

**Test:** If anyone has a fully digitized 25x25 grid with black cell positions, check:
1. Do three corners have dense 7x7 black-bordered squares?
2. Is there a 5x5 concentric square near row 18, col 18?
3. Are row 6 and column 6 alternating black/white patterns?

If any of these structural elements are missing, the grid CANNOT be a QR code (regardless of data content).

---

### Probability Assessment

| Scenario | Likelihood | Reasoning |
|----------|------------|-----------|
| Grid is a QR code (black cells alone) | Very Low (<5%) | Density far too low |
| Grid becomes QR after letter-to-binary mapping | Low (10-15%) | Clever but complex; hard for solvers |
| Grid + vault door overlay = QR | Low (10-15%) | Needs precise alignment; rescaling issues |
| Grid is NOT a barcode at all | HIGH (70-80%) | Standard meta-crossword mechanism suffices |
| Coincidental size match | Moderate | 25x25 is a natural crossword size |

### Bottom Line
The 25x25 size is a **perfect match for QR Code Version 2** and does NOT match any other standard 2D barcode format. However, the structural requirements of a QR code (three 7x7 finder patterns, timing patterns, alignment pattern) impose very specific constraints on which cells must be dark or light. The crossword's black cell pattern would need to be verified against these structural requirements before the theory can be confirmed. The most likely extraction mechanism remains reading circled cells after solving the crossword, with no barcode involved.
