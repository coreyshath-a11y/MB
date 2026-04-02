# THEORIES TESTED - Autonomous Solving Session
## Started: Feb 10, 2026 (evening)
## Last Updated: Feb 11, 2026
## Goal: Try EVERYTHING, track what works and what doesn't

---

## STATUS KEY
- **IMPOSSIBLE** = proven impossible, don't revisit
- **DEAD END** = tested thoroughly, nothing useful
- **WEAK** = some signal but not convincing
- **PROMISING** = worth pursuing further
- **CONFIRMED** = verified correct

---

## THEORY LOG

### T1: QR Code from Black Cell Pattern
- **Status: IMPOSSIBLE**
- Tested: 24 variants (2 inversions × 4 rotations × 3 flips)
- Results:
  - NO finder pattern found in ANY corner of ANY variant
  - Best corner match: 65.3% (need 100% for valid QR)
  - No finder pattern anywhere in grid
  - Grid is 25x25 (valid QR v2 size) but pattern doesn't match QR structure
- **Verdict: NOT a QR code in any orientation**

### T2: Data Matrix from Black Cell Pattern
- **Status: IMPOSSIBLE**
- Results:
  - Best L-pattern match: 68% (need ~100%)
  - Left col: 21/25 black (need 25/25)
  - Data Matrix uses EVEN-sized grids (10,12,14,...) - 25x25 is invalid
- **Verdict: NOT a Data Matrix**

### T3: Aztec Code from Black Cell Pattern
- **Status: IMPOSSIBLE**
- Results:
  - Best bull's eye match: 54.5% (5-ring), 49.0% (3-ring)
  - Center region doesn't have concentric ring pattern
- **Verdict: NOT an Aztec code**

### T4: 16 Circled Cells → Final Code
- **Status: PROMISING** (core extraction mechanism)
- Known: 3 of 16 letters: P(cell 13), S(cell 14), M(cell 15) — all from SUPERBOWLSTADIUM
- Final code pattern (row order): `____________PSM_`
- Key facts:
  - 5 cells are at entry starts (11, 91, 99, 137, 146), 11 are mid-entry
  - 78D appears in TWO circled cells (7 and 12) — 78D is a theme entry!
  - Entry number starts: 11, 91, 99, 137, 146 → A1Z26 = KMUGP (meaningless)
  - Countdown 7-5-3-1 sums to 16 = number of circled cells!
- Reading orders tested: row, column, across#, down#, spiral, clockwise, reverse
- To find remaining 13 letters: need to solve entries crossing each circled cell
- **Verdict: The extraction mechanism. Need more grid fills to complete.**

### T5: Hidden Locations in Theme Entries
- **Status: PROMISING** (core puzzle mechanic confirmed by 167A clue)
- 167A clue: "What this puzzle commemorates in eleven hidden words in theme entries"
- Location substrings found in known theme entries:
  - SUPERBOWLSTADIUM: SUPER, BOWL, STAD (no clear country/city locations)
  - CIRCLEABOUT: no location found (CABO not contiguous)
  - BEASTLAND: EAST, LAND (not specific locations)
- NIGER found backwards in REGINA (15,16-20) — but REGINA isn't a theme entry
- Word search of entire grid: no hidden AROUNDWORLD locations found yet
- **Verdict: Need more theme entries filled to find the 11 hidden locations**

### T6: All Four 94A Candidates
- **Status: WEAK** (CIRCLEABOUT still most likely but not certain)
- Tested all 4 level-11 P8 answers at the only 11-letter slot:

| Candidate | Placements | Impossible | Multi-match |
|-----------|-----------|------------|-------------|
| CIRCLEABOUT | 18 | 46 | 7 |
| TURNONADIME | 14 | 50 | 5 |
| OUTFORASPIN | 12 | 45 | 8 |
| REVOLUTIONS | 10 | 43 | 11 |

- TURNONADIME interesting: makes 67D=ROBINHOOD and 74D=HOODIE (real answers!)
  - BUT: conflicts with ZIP at 86D (forces .U. instead of .I.)
- CIRCLEABOUT: most placements but also most impossible (may be because more constraints reveal more gaps in our answer bank)
- **Verdict: CIRCLEABOUT still most likely, but TURNONADIME deserves investigation**

### T7: Number Patterns from Gist
- **Status: WEAK** (interesting connections but no smoking gun)
- Countdown 7-5-3-1 sum = 16 = circled cells count!
- "Don't say 67": 6×7 = 42 (a Lost number!)
- 704-BEAST-23 → entries 70, 42, 32, 78, 23 — 78D is a theme entry
- Lost numbers as entries: 4D, 8A/D, 15D, 16D, 23A/D, 42A — all in outer grid
- Vault ring sequence: sum=127, split at 10s → groups of 64 and 43
  - 127 = 2^7-1 = all 7 bits set
  - Morse decode attempt failed
  - Not RLE for 100 black cells (sum ≠ 100)
  - Braille-like decode gave: M9X<(4. (meaningless)
  - Cumulative index into sentence: RYGADOWANNASWE... (close to "round the world"?)
- **Verdict: Some tantalizing connections (7531→16, 6×7=42) but no clear mechanism**

### T8: Alternative Grid Reading Orders
- **Status: DEAD END**
- Tested: main diagonal, anti-diagonal, all diagonals, spiral, snake, column reads
- Results:
  - Diagonal: only trivial words (TOE, ODD, TEE)
  - Spiral: found PUSH, SHOT, TONE, HAFT, REIN (all from placed entries)
  - Snake: found CIRCLE, TOLEDO, ABOUT, ERASE, BEAST, SUPER — all placed entries
  - Columns: ROTUNDA(col13), ABASH(col10), TRITE(col9) — all placed entries
  - No hidden messages in any reading order
- **Verdict: No hidden messages in alternative reads. Grid is just a crossword.**

### T9: Calendar Dates → Entry Numbers → Theme Crossings
- **Status: PROMISING** (strong structural connection)
- 11 dates map to 11 entries: 11, 22, 31, 33, 61, 71, 81, 86, 91, 115, 127
- **7 of 11 calendar entries CROSS theme entries!**

| Date | Entry | Crosses Theme | Position in Theme |
|------|-------|--------------|-------------------|
| Jan 1 | 11D | 25A at pos 12 + 50A at pos 12 | col 12 |
| Feb 2 | 22A | NONE | — |
| Mar 1 | 31A | NONE | — |
| Mar 3 | 33D | NONE | — |
| Jun 1 | 61A | 19D at pos 7 | row 7 |
| Jul 1 | 71D | 73A at pos 13 | col 24 |
| Aug 1 | 81A | NONE | — |
| Aug 6 | 86D | 94A at pos 1 | col 8 |
| Sep 1 | 91A | 19D at pos 11 | row 11 |
| Nov 5 | 115D | 114A at pos 3 | col 3 |
| Dec 7 | 127A | 78D at pos 7 | row 17 |

- Calendar entry 11D at circled cell (0,12), 91A at circled cell (11,22)
- Entry number sum = 729 = 27³
- Only 2/11 entry lengths match staircase lengths (86D=3, 115D=5)
- **Verdict: Calendar entries point to specific positions in theme entries. This is likely the mechanism for finding hidden location names!**

### T10: Staircase Grid Brute Force
- **Status: IN PROGRESS** (agent running)
- AROUNDWORLD theory: column 4 spine
- Testing all valid location combinations

### T11: Acrostic Patterns
- **Status: DEAD END**
- First letters of placed entries (numerical order): DARPHZTACTPATDRTEBS → no words
- Last letters: AHAHTPENTROOORAIEDM → PENT found but likely coincidental
- Across entry #s at circles → A1Z26: HYDHLBEMUFPRKKKT → meaningless
- Down entry #s at circles → A1Z26: KEHUPOZTEGJZQZVN → meaningless
- **Verdict: No acrostic messages found**

### T12: Vault Ring Sequence Analysis
- **Status: WEAK**
- 46 values, sum = 127, max = 10
- Split at 10s → 2 groups: sum 64 and sum 43
- Direct A1Z26: DAHDACAHDAACDDDABAADDJAAABDAAAACACAAAAHDCAAAAJ
- Pairs as numbers: 41,84,13,18,41,13,44,41,21,14,50,11,12,41,11,13,13,11,11,84,31,11,20
- Morse attempt: failed (incomplete decode)
- Cumulative index into sentence: RYGADOWANNASWEUNWOR (suggestive but garbled)
- **Verdict: Sum=127=2^7-1 is notable, cumulative index shows fragments but nothing clean**

### T13: Octal Encoding Theory (User)
- **Status: WEAK** (mathematically clean but no clear output)
- 420₁₀ → 644₈, 73₁₀ → 111₈, 673₁₀ → 1241₈
- Concatenated: 6441111241 (10 digits)
- As binary (30 bits): 110100100001001001001010100001
- ASCII decode: garbage (210, 18, 'J')
- Various concatenation orders also produce garbage
- 6441111241 as decimal via octal → 881103521
- **Verdict: Math is clean but output doesn't decode to anything useful. Keep as reference.**

### T14: Binary from Grid Rows
- **Status: DEAD END**
- 25 rows × 25 cols = 625 bits total
- As 8-bit ASCII (black=1): random control chars + letters, no message
- As 8-bit ASCII (black=0): same, no message
- **Verdict: Grid black/white pattern doesn't encode binary ASCII**

### T15: 67D Pattern Analysis
- **Status: STUCK**
- Pattern: F??AEOE?O (6/9 letters known)
- 0 dictionary matches in /usr/share/dict/words
- Cross-references: pos 1 from 73A, pos 2 from 80A, pos 7 from 114A
- Contains circled cell at pos 2 (cell #6)
- Very unusual pattern — likely compound word, phrase, or proper noun
- If 94A=TURNONADIME instead: pattern changes completely (67D might = ROBINHOOD)
- **Verdict: Cannot solve without more crossing letters. Key dependency.**

---

## CONFIRMED FACTS (Don't Question These)
1. Grid is 25x25 with 100 black cells, 180° rotational symmetry
2. 176 entries (93 across, 95 down)
3. 16 circled cells → final extraction code (16 characters)
4. 167A = SUPERBOWLSTADIUM (from screenshot)
5. 149A = BEASTLAND (from screenshot)
6. 167A clue: "What this puzzle commemorates in eleven hidden words in theme entries"
7. 9-word sentence: EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD
8. Final answer submitted to Slackbot at mrbeast.salesforce.com
9. Countdown 7-5-3-1 sums to 16 = number of circled cells
10. 7 of 11 calendar entries cross theme entries

---

## KEY CONNECTIONS DISCOVERED
1. **Calendar → Theme Crossings**: 7/11 calendar dates point to specific theme entry positions
2. **7-5-3-1 → 16 circles**: Sum of countdown = number of extraction cells
3. **6×7 = 42**: "Don't say 67" connects to Lost numbers
4. **704-BEAST-23 → 78D**: Phone number digits → entries, including theme entry 78D
5. **NIGER in REGINA backwards**: Hidden location substring in grid (row 15)
6. **78D in TWO circled cells**: Theme entry 78D hits cells 7 and 12 — 15-letter entry is key

---

## WHAT'S IMPOSSIBLE (Ruled Out)
- QR code, Data Matrix, Aztec code from grid (all tested, all failed)
- Binary ASCII from grid row patterns
- Simple acrostics from entry first/last/middle letters
- Alternative reading orders (diagonal, spiral, snake) for hidden messages
- FOOTBALLSTANDS at 73A (conflicts with ROTUNDA at col 13)
- LEVISSUPERBOWL at any 14-letter position (conflicts at both 73A and 114A)
- Grid as 21x21 (confirmed 25x25)

---

## PRIORITY NEXT STEPS
1. **Solve the 13 unknown circled cells** — fill entries crossing them
2. **Find the 11 hidden location names** in theme entries
3. **Fill theme entries** 25A, 50A, 73A, 114A, 138A, 19D, 78D
4. **Investigate TURNONADIME as 94A** — makes 67D=ROBINHOOD which is clean
5. **Deep dive on calendar-theme crossing positions** — may reveal hidden location positions
6. **Crack 73A** — 14 letters, U at pos 2, Super Bowl themed
