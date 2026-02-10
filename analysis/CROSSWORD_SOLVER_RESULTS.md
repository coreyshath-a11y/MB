# CROSSWORD SOLVER RESULTS
## Last Updated: Feb 10, 2026 (v4 - MAJOR UPDATE: community screenshot data + gist integration)

## Grid Confirmed: 25×25
- 100 black cells, 525 white cells
- 176 numbered entries (93 across, 95 down)
- Entry length distribution: 3(34), 4(46), 5(32), 6(28), 7(18), 8(12), 9(9), 11(1), 14(2), 15(2), 16(4)

## CRITICAL FINDING: Missing Lengths
The grid has NO entries of length 2, 10, 12, or 13. These confirmed answers CANNOT be direct crossword entries:

| Answer | Length | Source | Implication |
|--------|--------|--------|-------------|
| RA, ER, OI, NO | 2 | P8 (level 2) | Too short for any grid entry |
| TRADEUNION | 10 | P8 (level 10) | No 10-letter slots |
| ORBICULATE | 10 | P8 (level 10) | No 10-letter slots |
| STAINPROOF | 10 | P8 (level 10) | No 10-letter slots |
| RESOLUTION | 10 | P8 (level 10) | No 10-letter slots |
| WILMINGTON | 10 | P4 | No 10-letter slots |
| SACRAMENTO | 10 | P4 | No 10-letter slots |
| INTRODUCTIONS | 13 | P3 | No 13-letter slots |
| CONTRADICTION | 13 | Video | No 13-letter slots |

## 94A COMPETITION (Only 1 length-11 slot)

| Candidate | Placements | Verdict |
|-----------|-----------|---------|
| **CIRCLEABOUT** | **13** | **BEST - most cascading constraints** |
| TURNONADIME | 11 | Second best |
| OUTFORASPIN | 9 | Third |
| REVOLUTIONS | 5 | Worst fit |

## CONFIRMED PLACEMENTS (19 entries + 2 hypothetical)

### Original 17 (from constraint solver)
| Entry | Answer | Position | Length | Source | How Placed |
|-------|--------|----------|--------|--------|------------|
| 36A | DORA | (4,7) | 4 | P8 | Constraint propagation |
| 37D | ABASH | (4,10) | 5 | P3 | Constraint propagation |
| 53D | ROTUNDA | (6,13) | 7 | P8 | Constraint propagation |
| 58A | PUSH | (7,8) | 4 | P9 | Only 4-letter answer with S at pos 2 |
| 66A | HAFT | (8,10) | 4 | P3 | Only 4-letter answer starting with H |
| 86D | ZIP | (11,8) | 3 | P9 | Only 3-letter answer with I at pos 1 |
| 87D | TRITE | (11,9) | 5 | P3 | Only 5-letter answer matching ?R?T? |
| 88A | ADORN | (11,12) | 5 | P8 | Only 5-letter answer starting with A |
| 94A | CIRCLEABOUT | (12,7) | 11 | P8 | Best fit for only 11-letter slot |
| 96D | TONER | (12,17) | 5 | P8 | Only answer fitting ?O?E? constraint |
| 102A | PINTO | (13,8) | 5 | P8 | Constraint propagation |
| 103A | ACHOO | (13,14) | 5 | P1 | Only answer fitting ????O constraint |
| 109A | TOLEDO | (14,9) | 6 | P4 | Constraint propagation |
| 110D | DENVER | (14,13) | 6 | P4 | Constraint propagation |
| 117A | REGINA | (15,16) | 6 | P4 | Only answer fitting ?E???? constraint |
| 121A | TONI | (16,11) | 4 | P8 | Constraint propagation |
| 123A | ERASE | (16,16) | 5 | P3 | Only answer fitting E???? constraint |

### NEW from community screenshot (Feb 10)
| Entry | Answer | Position | Length | Source | How Placed |
|-------|--------|----------|--------|--------|------------|
| **167A** | **SUPERBOWLSTADIUM** | **(22,9)** | **16** | **Screenshot** | **Community solve - zero conflicts** |
| **149A** | **BEASTLAND** | **(20,4)** | **9** | **Screenshot** | **Community solve - zero conflicts** |

### Hypothetical (unconfirmed)
| Entry | Answer | Position | Length | Source | How Placed |
|-------|--------|----------|--------|--------|------------|
| **104D** | **ORGANIC** | **(13,18)** | **7** | **Dict** | **HYPOTHESIS: most common O?GA??? match** |
| **111A** | **NRA** | **(14,17)** | **3** | **Dict** | **HYPOTHESIS: unique fit NR? from ORGANIC** |

### FAILED placement (from screenshot)
| Entry | Answer | Attempted | Conflict | Notes |
|-------|--------|-----------|----------|-------|
| 73A | FOOTBALLSTANDS | (9,11) | Cell (9,13): needs O, has U from ROTUNDA | Screenshot may have been misread, or answer differs |

### 73A INVESTIGATION
73A is 14 letters at row 9, cols 11-24. Screenshot showed something like FOOTBALLSTANDS but this conflicts with ROTUNDA (53D) which places U at (9,13). The correct 73A answer must have U at position 2 (col 13). Alternatives:
- Could be a compound phrase with U in position 2
- Screenshot may show a different but similar word
- Position 2 must be U (confirmed from ROTUNDA cascade through CIRCLEABOUT)

### LEVISSUPERBOWL - No valid 14-letter position
Tested at both 14-letter slots (73A and 114A) — conflicts at both:
- 73A: V at pos 2 conflicts with U (ROTUNDA)
- 114A: R at pos 9 conflicts with E (TRITE), L at pos 13 conflicts with E (DENVER)

**SUPERBOWLATLEVIS** (16 letters) fits at **25A** (row 2, cols 0-15) with zero conflicts — plausible but unconfirmed.

## CURRENT PARTIAL GRID (v4 with community screenshot data)
```
     0123456789012345678901234
R 0 |.......##......##........
R 1 |.......#.......##........
R 2 |................#........
R 3 |....#.....#...#.....#....
R 4 |....###DORA#.........#...
R 5 |....#...#.B..#....##.....
R 6 |..........A..R..#......##
R 7 |.......#PUSH#O...#......#
R 8 |...#.....#HAFT##....#....
R 9 |###......##..U...........
R10 |#...#...##...N..#....#...
R11 |.....#..ZT.#ADORN#...#...
R12 |......#CIRCLEABOUT#......
R13 |...#...#PINTO#ACHOo#.....
R14 |...#....#TOLEDO##NrA#...#
R15 |.........E...E##REGiNA###
R16 |....#....##TONI#ERaSE#...
R17 |#......#....#V...#n......
R18 |##......#....E....i......
R19 |.....##....#.R..#.c.#....
R20 |...#BEASTLAND#....###....
R21 |....#.....#...#.....#....
R22 |........#SUPERBOWLSTADIUM
R23 |........##.......#.......
R24 |........##......##.......
```
Note: UPPERCASE = confirmed, lowercase = from ORGANIC/NRA hypothesis
NEW: SUPERBOWLSTADIUM at 167A (row 22) and BEASTLAND at 149A (row 20)

### Circled Cell Values (now 3 of 16 known)
| # | Cell | Letter | Source |
|---|------|--------|--------|
| 13 | (22,11) | **P** | 167A = SUPERBOWLSTADIUM |
| 14 | (22,18) | **S** | 167A = SUPERBOWLSTADIUM |
| 15 | (22,24) | **M** | 167A = SUPERBOWLSTADIUM |

### New Down-Entry Constraints (from SUPERBOWLSTADIUM + BEASTLAND)
| Down Entry | Length | Pattern | New Letters |
|-----------|--------|---------|-------------|
| 128D | 4 | `...B` | B from BEASTLAND |
| 130D | 6 | `...L.S` | L from BEASTLAND, S from 167A |
| 131D | 4 | `..A.` | A from BEASTLAND |
| 137D | 7 | `..S....` | S from BEASTLAND |
| 139D | 7 | `..D.E..` | D from BEASTLAND, E from 167A |
| 144D | 3 | `..N` | N from BEASTLAND (now ???N → entry 144D is 3 letters, this is pos 2) |
| 150D | 5 | `E....` | E from BEASTLAND |
| 151D | 5 | `A....` | A from BEASTLAND |
| 152D | 5 | `N.P..` | N from BEASTLAND, P from 167A |
| 168D | 3 | `U..` | U from 167A |
| 169D | 3 | `B..` | B from 167A |
| 170D | 3 | `A..` | A from 167A |
| 124D | 9 | `......I..` | I from 167A at pos 6 |
| 125D | 9 | `......U..` | U from 167A at pos 6 |
| 126D | 9 | `......M..` | M from 167A at pos 6 |
| 133D | 8 | `.....W..` | W from 167A at pos 5 |
| 135D | 8 | `.....T..` | T from 167A at pos 5 |
| 140D | 5 | `...L.` | L from 167A at pos 3 |
| 154D | 4 | `..O.` | O from 167A at pos 2 |
| 162D | 4 | `..S.` | S from 167A at pos 1 |
| 163D | 4 | `..T.` | T from 167A at pos 1 |

## HEAVILY CONSTRAINED ENTRIES (dictionary analysis)

Several entries near placed answers have heavy constraints but NO standard dictionary matches:

| Entry | Pattern | Constraints | Notes |
|-------|---------|-------------|-------|
| 67D | F??AEOE?O | 6/9 known | 0 dict matches! Likely compound word |
| 74D | ??OBAO | 4/6 known | 0 dict matches! |
| 75D | ??ROC | 3/5 known | 4 matches: DUROC, MOROC, SIROC, TAROC |
| 80D | ??CNO? | 3/6 known | 0 dict matches! |
| 95D | LTL?T?? | 4/7 known | 0 dict matches! |
| 85A | ??ZT? | 2/5 known | 0 dict matches! ZT combination very rare |
| 89D | NUH | 3/3 known | 0 dict matches (colloquial "nuh") |
| 8D | ????R??U | 2/8 known | 0 confirmed answers fit |

**Significance**: These zero-match patterns in the central grid are unusual. They suggest either:
1. These entries are compound words/phrases (common in puzzle crosswords)
2. Some may be proper nouns
3. Mike Selinker puzzles often use creative fills

## STRONG HYPOTHESIS: 104D = ORGANIC (cascading)

104D pattern: O?GA??? (7 letters, 3 confirmed)
- Dictionary matches: ORGANAL, ORGANDY, ORGANER, **ORGANIC**, ORGANON, ORGANRY, ORGANUM
- ORGANIC is the most common crossword word among these
- **Cascade chain if ORGANIC is correct:**
  - 111A = NR? → **NRA** (unique fit among known answers) ← PLACED
  - 112D = AIS??? → likely **AISLED** (only 6-letter word starting AIS)
  - 134A starts with **N** (7-letter answer beginning N)
  - **138A pos 9 = I** (theme entry constraint!)
  - 146A = ?C? (C at position 1)
  - 146A[2] = 112D[5] (linked constraint)

## DAKAR HYPOTHESIS for 50A

50A currently: `..........A..R..` (positions 10=A, 13=R confirmed)
- DAKAR (D-A-K-A-R) at positions 9-13 matches both known letters perfectly
- Would give: `.........DAKAR..`
- Problems: 46D would need K at pos 1 (pattern ?KHA??), which has 0 dictionary matches
- May indicate 46D is also an unusual word, or DAKAR theory needs refinement

## THEME ENTRY STATUS (Updated with community data)

| Entry | Length | Partial Fill | Known | Status |
|-------|--------|-------------|-------|--------|
| 25A | 16 | `................` | 0/16 | Candidate: SUPERBOWLATLEVIS? |
| 50A | 16 | `..........A..R..` | 2/16 | DAKAR at pos 9-13 confirmed |
| 73A | 14 | `..U...........` | 1/14 | NOT FOOTBALLSTANDS (conflicts with ROTUNDA) |
| 94A | 11 | `CIRCLEABOUT` | 11/11 | **COMPLETE** |
| 114A | 14 | `.........E...E` | 2/14 | Must have E at pos 9 and E at pos 13 |
| 138A | 16 | `....E....i......` | 2/16 | E from DENVER[4], i from ORGANIC hypothesis |
| **167A** | **16** | **`SUPERBOWLSTADIUM`** | **16/16** | **COMPLETE — from community screenshot** |
| 19D | 15 | `...............` | 0/15 | Unconstrained |
| 78D | 15 | `...............` | 0/15 | Unconstrained |

### ALSO: Non-theme long entries
| Entry | Length | Fill | Status |
|-------|--------|------|--------|
| **149A** | **9** | **`BEASTLAND`** | **COMPLETE — from community screenshot** |

Note: Lowercase = hypothetical (from ORGANIC hypothesis)

### 167A = SUPERBOWLSTADIUM: What It Means
"What this puzzle commemorates in eleven hidden words in theme entries"
→ The puzzle commemorates **SUPERBOWLSTADIUM** (Levi's Stadium, Super Bowl LX, Feb 8, 2026)
→ The 11 hidden words in theme entries are location names found WITHIN the theme entry text
→ This changes the interpretation: hidden locations are substrings of the filled theme entries

## CALENDAR DATES → ENTRY NUMBERS THEORY

The 11 circled calendar dates encode entry numbers (month×10+day):

| # | Date | Entry | Length | Staircase Row | Location |
|---|------|-------|--------|---------------|----------|
| 1 | Jan 1 | 11D | 7 | Row 1 (4-letter) | MALI? |
| 2 | Feb 2 | 22A | 7 | Row 2 (6-letter) | TEHRAN? |
| 3 | Mar 1 | 31A | 3 | Row 3 (5-letter) | LAGOS? |
| 4 | Mar 3 | 33D | 3 | Row 4 (5-letter) | SUDAN? |
| 5 | Jun 1 | 61A | 6 | Row 5 (4-letter) | OMAN? |
| 6 | Jul 1 | 71D | 6 | Row 6 (4-letter) | ADEN? |
| 7 | Aug 1 | 81A | 4 | Row 7 (5-letter) | WALES? |
| 8 | Aug 6 | 86D | 3=ZIP | Row 8 (3-letter) | GOA? |
| 9 | Sep 1 | 91A | 3 | Row 9 (5-letter) | NIGER? |
| 10 | Nov 5 | 115D | 5 | Row 10 (5-letter) | DELHI? |
| 11 | Dec 7 | 127A | 6 | Row 11 (4-letter) | CHAD? |

Note: Entry lengths DON'T match staircase row lengths. The connection mechanism is unclear — perhaps these entries CROSS theme entries at the positions where locations are hidden.

## BOTTLENECK: The Outer Grid

All 17 placed entries are in rows 4-16 (central band). Theme entries at rows 2, 6, 9, 15, 18, 22 need more crossing letters. The outer regions (rows 0-3, 17-24) have ZERO constraints, making it impossible to place answers there without additional information.

## ANSWER SURPLUS/DEFICIT BY LENGTH

| Length | Slots | Confirmed Answers | Surplus/Deficit |
|--------|-------|-------------------|-----------------|
| 3 | 34 | 4 unplaced | -30 |
| 4 | 46 | 3 unplaced | -43 |
| 5 | 32 | 6 unplaced | -26 |
| 6 | 28 | 12 unplaced | -16 |
| 7 | 18 | 14 unplaced | -4 |
| 8 | 12 | 13 available | +1 |
| 9 | 9 | 14 available | +5 |

At 8-letter and 9-letter, we have MORE answers than slots. This means some confirmed answers serve a different purpose (clue words? meta-puzzle inputs?) or some are wrong.

## MELANESIANS THEORY (Community Alternative — WEAKER)

Community suggestion for staircase: OMAN, GREECE, ITALY, JAPAN, IRAN, PERU, SPAIN, CIV, GHANA, KENYA, LAOS → column 4 = MELANESIANS.
- All lengths match the staircase
- BUT: CIV is an ISO code not a country name
- BUT: Only 3/11 are MrBeast philanthropy countries
- BUT: No location matches both 50A pos10=A AND pos13=R (DAKAR does for AROUNDWORLD)
- **AROUNDWORLD remains the stronger theory** (see STAIRCASE_GRID_ANALYSIS.md)

## NEXT STEPS (Updated Feb 10 evening)
1. ~~**Determine 167A**~~ → **SOLVED: SUPERBOWLSTADIUM**
2. **Resolve 73A conflict** — screenshot showed FOOTBALLSTANDS but U at pos 2 conflicts. Find correct 14-letter answer with U at position 2
3. **Determine 25A** — SUPERBOWLATLEVIS (16) is plausible, zero conflicts. Confirm from screenshot or community
4. **Cascade from SUPERBOWLSTADIUM + BEASTLAND** — 20+ new down-entry constraints
5. **Verify ORGANIC hypothesis** — ORGANIC → NRA chain looks solid
6. **Fill outer grid using new down constraints** — many entries now partially constrained
7. **Decode Super Bowl photo numbers** — Hint #1 still actionable
8. **Place P4 cities** — use new constraints from theme entries
9. **Find hidden location names** — now that theme entries are filling, look for AROUNDWORLD locations hidden within them
