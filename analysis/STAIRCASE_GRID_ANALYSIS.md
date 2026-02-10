# Staircase Grid Analysis (Bottom-Right of Crossword)
## Last Updated: Feb 10, 2026 (v3 - PRECISE DIGITIZATION COMPLETE)

## What Is It?
The crossword PDF has a small secondary grid in the bottom-right corner. It consists of grey cells arranged in an interlocking staircase pattern with **11 rows** on a **9-column** grid.

## Connection to 167 Across
167 Across: "What this puzzle commemorates in **eleven hidden words** in the theme entries"
The staircase has exactly **11 rows** = the 11 hidden location names.

## CONFIRMED Grid Structure (from pixel analysis + community HTML)

```
        Col: 0  1  2  3  4  5  6  7  8
Row  1:             [_][_][_][_]            = 4 letters
Row  2:       [_][_][_][_][_][_]            = 6 letters
Row  3:       [_][_][_][_][_]               = 5 letters
Row  4:             [_][_][_][_][_]         = 5 letters
Row  5:       [_][_][_][_]                  = 4 letters
Row  6:             [_][_][_][_]            = 4 letters
Row  7:                [_][_][_][_][_]      = 5 letters
Row  8:             [_][_][_]               = 3 letters
Row  9:    [_][_][_][_][_]                  = 5 letters
Row 10:          [_][_][_][_][_]            = 5 letters
Row 11:       [_][_][_][_]                  = 4 letters
```

**Word lengths: 4, 6, 5, 5, 4, 4, 5, 3, 5, 5, 4 = 50 total letters**

### HTML Layout Confirmation (from community source)
```javascript
const layout = [
  [0,0,0,1,1,1,1,0,0],  // Row 1: cols 3,4,5,6
  [0,1,1,1,1,1,1,0,0],  // Row 2: cols 1,2,3,4,5,6
  [0,1,1,1,1,1,0,0,0],  // Row 3: cols 1,2,3,4,5
  [0,0,0,1,1,1,1,1,0],  // Row 4: cols 3,4,5,6,7
  [0,1,1,1,1,0,0,0,0],  // Row 5: cols 1,2,3,4
  [0,0,0,1,1,1,1,0,0],  // Row 6: cols 3,4,5,6
  [0,0,0,0,1,1,1,1,1],  // Row 7: cols 4,5,6,7,8
  [0,0,0,1,1,1,0,0,0],  // Row 8: cols 3,4,5
  [1,1,1,1,1,0,0,0,0],  // Row 9: cols 0,1,2,3,4
  [0,0,1,1,1,1,1,0,0],  // Row 10: cols 2,3,4,5,6
  [0,1,1,1,1,0,0,0,0],  // Row 11: cols 1,2,3,4
];
```

## Interlocking Constraints (ADJACENT ROWS ONLY)

**CRITICAL FIX**: Only vertically adjacent rows share letters. Non-adjacent rows at the same column CAN have different letters (there are "breaks" in the chain).

### Adjacent Row Overlaps (29 constraints total)
| Rows | Shared Columns | Constraint |
|------|---------------|------------|
| R1-R2 | 3,4,5,6 | ALL of R1 appears in last 4 positions of R2 |
| R2-R3 | 1,2,3,4,5 | ALL of R3 appears in first 5 positions of R2 |
| R3-R4 | 3,4,5 | Middle 3 letters shared |
| R4-R5 | 3,4 | 2 letters shared |
| R5-R6 | 3,4 | 2 letters shared |
| R6-R7 | 4,5,6 | 3 letters shared |
| R7-R8 | 4,5 | 2 letters shared |
| R8-R9 | 3,4 | 2 letters shared |
| R9-R10 | 2,3,4 | 3 letters shared |
| R10-R11 | 2,3,4 | 3 letters shared |

### Column 4 = THE SPINE
Column 4 is used by ALL 11 rows AND passes through all adjacent pairs without a break. Therefore **column 4 has ONE letter shared by all 11 words**.

### Key Derived Constraints
- **R2 = R3[0:2] + R1** (first 2 letters of R3 + all of R1)
- **R3[2:5] = R1[0:3]** (last 3 of R3 = first 3 of R1)
- **R4[0:3] = R1[0:3]** (first 3 of R4 = first 3 of R1)
- **R5[2:4] = R1[0:2]** (last 2 of R5 = first 2 of R1)
- **R6[0:2] = R1[0:2]** (first 2 of R6 = first 2 of R1)

## Solver Results

### With Location Names Only: 0 solutions
The R1-R2-R3 chain is extremely tight: R2 (6 letters) must contain ALL of R1 as its last 4 letters AND ALL of R3 as its first 5 letters. No combination of known geographic names satisfies this.

### With Full English Dictionary: 589 valid R1-R2-R3 chains
Proves the constraint model is CORRECT. The issue is just finding the right location names.

### Geographic Chains Found
Chains where R2 is a 6-letter location name containing a 4-letter location as its last 4 letters:
| R1 | R2 | R3 | Notes |
|----|----|----|-------|
| MALI | **SOMALI** | SOMAL | SOMALI contains MALI |
| DIAN | **INDIAN** | INDIA | INDIAN contains INDIA (R3) |
| PALI | **NEPALI** | NEPAL | NEPALI contains NEPAL (R3) |
| MOAN | **SAMOAN** | SAMOA | SAMOAN contains SAMOA (R3) |
| EDEN | **SWEDEN** | SWEDE | SWEDEN contains EDEN |
| ROME | STROME | STROM | Strome is a Scottish village |
| SCAT | **MUSCAT** | MUSCA | MUSCAT contains... |
| APIA | OKAPIA | OKAPI | OKAPIA isn't standard |
| GERS | **ANGERS** | ANGER | Angers (France), Gers (France) |

### Implication
The 11 location names likely include demonym-like geographic terms (SOMALI, INDIAN, NEPALI, SAMOAN, etc.) as well as standard place names. These ARE found hidden in English words/phrases that could be theme entry answers.

## 11 Calendar Dates (Possible Connection)
From the Super Bowl ad video, 11 circled dates on a calendar:
1. January 1
2. February 2
3. March 1
4. March 3
5. June 1
6. July 1
7. August 1
8. August 6
9. September 1
10. November 5
11. December 7

**11 dates = 11 locations!** These likely correspond to dates of MrBeast philanthropic events at the 11 locations.

## MrBeast Known Locations
- Accra, Ghana (hospital, confirmed from vault puzzle)
- Lima, Peru (confirmed from belt/wire puzzle)
- Dubai/UAE (Beastland, MrBeast Burger)
- Riyadh, Saudi Arabia (Beastland)
- Various US cities (Greenville NC hometown)

## Theory: 167A = Commemorating Philanthropy
The 11 hidden location names likely represent places where MrBeast did significant philanthropic work. 167A (16 letters) commemorates this. Candidates:
- CHARITYCHALLENGE (16)
- TENTHANNIVERSARY (16)
- WORLDRECORDVIDEO (16)
- GLOBALPHILANTHRO (16)

## Next Steps
- [x] EXACT cell count per row (CONFIRMED: 4,6,5,5,4,4,5,3,5,5,4)
- [x] Column alignment mapping (CONFIRMED: 9 columns, 0-8)
- [x] Constraint model (FIXED: adjacent-only, not all-pairs)
- [ ] Full staircase solve with expanded word list (RUNNING)
- [ ] Match calendar dates to MrBeast events at specific locations
- [ ] Fill crossword theme entries to find hidden location names
- [ ] Determine 167A answer
