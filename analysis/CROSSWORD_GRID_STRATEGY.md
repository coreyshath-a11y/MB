# Crossword Grid Filling Strategy
## February 12, 2026

## GOAL
Fill the 21×21 crossword grid (176 entries) to:
1. Find 11 hidden location names in theme entries
2. Read 167 Across (16 chars) = meta-answer
3. Extract ~16 circled cell letters = FINAL CODE

---

## KNOWN ANSWER INVENTORY

### By Length (for matching to grid entries):

**2-letter answers (7):**
OI, RA, ER, NO, OF, WE, [more from ad puzzles?]

**3-letter answers (7):**
ION, RAD, ERA, EON, ZIP, [more pending]

**4-letter answers (7):**
TONI, DORA, RACE, NOTE, HAFT, PUSH, NAME

**5-letter answers (10+):**
PINTO, ADORN, EVERY, ABASH, OPERA, ERASE, TRITE, LEADS, WORLD, TONER

**6-letter answers (6+):**
OPTION, ECLAIR, ORIENT, AROUND, MATTER, CHAIRS, CONVEX

**7-letter answers (5+):**
PORTION, CALIBER, HEARTED, MUSTERS, TOWARDS, HIRPLED, QUORUMS

**8-letter answers (8+):**
POSITRON, ROUTINES, CASHTENT, SCENARIO, NEUROTIC, SCREENER, ABSOLUTE, TEAMSEAS, LOCATION, FLAMINGO

**9-letter answers (6+):**
RATPOISON, CHALLENGE, SOMEWHERE, DITHERING, HOWITZERS, HIGHHEELS, ALLUSIONS, RESISTIVE, OUTLINERS

**10-letter answers (3+):**
STAINPROOF, RESOLUTION, ORBICULATE

**11-letter answers (3):**
OUTFORASPIN, CIRCLEABOUT, REVOLUTIONS

**13-letter answers (2):**
INTRODUCTIONS, CONTRADICTION

**16-letter answer (1):**
CHANGINGTHEWORLD (candidate for 167 Across)

---

## STRATEGY

### Step 1: Map Entry Lengths from PDF Grid
For each of the 176 entries, count the number of white squares. This gives us the target length for each position.

### Step 2: Place Length-Unique Answers
If only one known answer matches a particular entry length, place it confidently.
- 13-letter entries → INTRODUCTIONS or CONTRADICTION
- 11-letter entries → OUTFORASPIN, CIRCLEABOUT, or REVOLUTIONS
- 16-letter entry → 167 Across (CHANGINGTHEWORLD?)

### Step 3: Use Crossing Letters
Where placed answers cross other entries, the shared letters become constraints. Use these to:
- Validate placements
- Narrow possibilities for intersecting entries
- Identify inconsistencies (wrong placement)

### Step 4: Identify Theme Entries
Theme entries are typically the longest Across entries spanning the full or near-full width of the grid. In a 21×21 grid, these are likely:
- 1 Across (top row)
- Entries in rows 4, 7, 10, 13, 16, 19 (every 3 rows)
- 176 Across (last row?)

### Step 5: Search for Hidden Locations
Once theme entries are filled, search for consecutive letter sequences that spell location names:
- KENYA (5)
- GHANA (5)
- DUBAI (5)
- EGYPT (5)
- GIZA (4)
- RIO (3)
- CANADA (6)
- GREENVILLE (10)
- SANFRANCISCO (12)
- YELLOWKNIFE (11)
- DOMINICANREPUBLIC (17)

### Step 6: Extract Circled Letters
Read circled cells in standard crossword order (left-to-right, top-to-bottom).
These ~16 letters = THE FINAL CODE.

---

## CIRCLED CELL POSITIONS (from PDF visual analysis)

From the crossword PDF, circles appear at approximately these grid positions:
(Need precise mapping — visible circles in the image at several numbered cells)

Approximate positions based on PDF examination:
- Row 3: around cells 25-26 area
- Row 4: around cell 30 area
- Row 5: around cells 37-38 area
- Row 6: around cell 40 area
- Row 7: around cells 48-49 area
- Row 9: around cell 80 area
- Row 10: around cells 86-87 area
- Row 14: around cell 97 area
- Row 17: around cell 160 area
- Row 18: around cell 167-169 area
- Row 19: around cell 170 area

**NOTE:** These positions need precise verification by careful grid counting.

---

## COORDINATE SYSTEM FROM PUZZLE 3

Puzzle 3 generated 19 coordinate pairs that may specify WHERE answers go in the crossword:
```
WI(3,4)  KR(10,7) AF(9,6)  KS(10,3) CC(5,4)
BN(8,10) FT(1,6)  KL(3,6)  GA(4,10) FI(3,2)
GS(5,2)  TG(1,6)  RD(10,3) WS(7,8)  NC(10,4)
YD(3,1)  BG(6,1)  ML(2,7)  KP(4,9)
```

If the 2-letter codes are TV show initials:
- WI = WHAT IF...?
- KR = KNIGHT RIDER
- AF = ASTRO FARM
- KS = KAREN SISCO
- CC = CASH CAB
- BN = BURN NOTICE
- FT = (?)
- KL = KNOTS LANDING
- GA = GREEN ACRES
- FI = (?)
- GS = GET SMART
- TG = TOP GEAR
- RD = RUSSIAN DOLL
- WS = (?)
- NC = NIGHT COURT
- YD = YES DEAR
- BG = BEAST GAMES
- ML = MODERN LOVE
- KP = KIM POSSIBLE

And the coordinates (x,y) may point to positions in the crossword grid where corresponding answers (HAFT, DITHERING, etc.) should be placed.

---

## AUTOMATED SOLVER APPROACH

A Python constraint-satisfaction solver could:
1. Parse the grid to get entry positions and lengths
2. Load all known answers
3. For each entry, generate candidate answers matching the length
4. Propagate crossing letter constraints
5. Use backtracking search to find consistent fill
6. Output the completed grid

This would require:
- Accurate grid digitization (position + length of each entry)
- Full list of candidate answers for each position
- Standard crossword word list for non-puzzle entries (if any exist)

---

*Strategy document — to be updated as more answers are discovered*
