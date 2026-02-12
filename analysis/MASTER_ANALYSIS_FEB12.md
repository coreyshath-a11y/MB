# MASTER ANALYSIS — MrBeast x Salesforce Million Dollar Puzzle Hunt
## Updated: February 12, 2026

**STATUS: PRIZE UNCLAIMED — RACE IS ON**
**Deadline: April 2, 2026 at 11:59 PM ET**
**Submit via: Slackbot at mrbeast.salesforce.com**

---

## TABLE OF CONTENTS
1. [Architecture Overview](#architecture)
2. [9-Word Sentence (SOLVED)](#sentence)
3. [All 9 Variety Puzzles (SOLVED)](#variety-puzzles)
4. [Super Bowl Ad Puzzles (6/32 SOLVED)](#ad-puzzles)
5. [The Crossword — Critical Path](#crossword)
6. [Known Crossword Answers](#known-answers)
7. [Visual Clue Analysis](#visual-clues)
8. [Location Theory — 11 Hidden Words](#locations)
9. [Confirmed Red Herrings](#red-herrings)
10. [Critical Next Steps](#next-steps)
11. [Questions for Slackbot](#slackbot-questions)

---

## 1. ARCHITECTURE OVERVIEW <a name="architecture"></a>

```
┌─────────────────────────────────────────────────────────┐
│  STAGE 1: THREE HUBS                                    │
│                                                          │
│  HUB A: YouTube Playlist (9 videos)                      │
│  ├─ Each video has pinned comment → variety puzzle        │
│  ├─ Each puzzle → ONE word (9 words total)                │
│  ├─ 9 words form a sentence = meta-instruction            │
│  └─ Each puzzle ALSO generates crossword clue-answers     │
│                                                          │
│  HUB B: Super Bowl Commercial                             │
│  ├─ "Almost everything Jimmy passes is a clue"            │
│  ├─ ~32 embedded puzzles using online ciphers             │
│  └─ Each puzzle → one crossword answer                    │
│                                                          │
│  HUB C: Bank Video ("Red Herring Bank")                   │
│  ├─ Requires answers FROM the Super Bowl ad as input      │
│  ├─ Creates dependency chain: ad → bank                   │
│  └─ Each bank puzzle → one crossword answer               │
│                                                          │
│  TOTAL: ~50 puzzles producing ~176 crossword answers      │
│  + crossword itself = 51st puzzle                         │
├─────────────────────────────────────────────────────────┤
│  STAGE 2: THE CROSSWORD                                  │
│  ├─ 21×21 grid, 176 entries (90 Across + 86 Down)        │
│  ├─ NO printed clues — answers come from Stage 1          │
│  ├─ Only meta-clue: 167A (16 chars)                       │
│  │   "What this puzzle commemorates in eleven hidden       │
│  │    words in the theme entries"                          │
│  ├─ 11 theme entries contain HIDDEN LOCATION NAMES         │
│  ├─ ~16 CIRCLED CELLS → extract letters → final code      │
│  └─ Small staircase grid (bottom-right) = visual guide    │
├─────────────────────────────────────────────────────────┤
│  FINAL SUBMISSION                                         │
│  └─ 16 circled letters (in reading order) = THE CODE      │
│      → Submit to Slackbot at mrbeast.salesforce.com       │
└─────────────────────────────────────────────────────────┘
```

---

## 2. THE 9-WORD SENTENCE (SOLVED) <a name="sentence"></a>

**Official word lengths:** 5, 9, 5, 7, 8, 4, 9, 6, 5

| Slot | Length | Word | Source Puzzle | Confidence |
|------|--------|------|--------------|------------|
| 1 | 5 | **EVERY** | P1: 100 Wells in Africa | DEFINITIVE |
| 2 | 9 | **CHALLENGE** | P2: 600 Strangers | DEFINITIVE |
| 3 | 5 | **LEADS** | P3: Dirtiest Beach | DEFINITIVE |
| 4 | 7 | **TOWARDS** | P4: $1-$500K Experiences | CONFIRMED |
| 5 | 8 | **LOCATION** | P5: Pokemon Go | DEFINITIVE |
| 6 | 4 | **NAME** | P6: Wilderness | DEFINITIVE |
| 7 | 9 | **SOMEWHERE** | P7: 100 Dogs | CONFIRMED |
| 8 | 6 | **AROUND** | P8: Pyramids | VERIFIED |
| 9 | 5 | **WORLD** | P9: Circle | SOLVED |

### Complete Sentence:
> **"EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD"**

### Interpretation:
"Every challenge leads to a location — name somewhere around the world"
→ Find **11 hidden location names** in the crossword's theme entries
→ These are places where MrBeast filmed his challenge videos

### Note on P7:
Official hint says word 7 must be 9 letters. "SOMEWHERE" (9) fits. Earlier community answer "ONE" (3) was WRONG. Alternative candidate "COUNTRIES" (9) was considered but "SOMEWHERE" confirmed by community consensus.

---

## 3. ALL 9 VARIETY PUZZLES — SOLVED <a name="variety-puzzles"></a>

### Puzzle 1: I Built 100 Wells in Africa → EVERY
- **Type:** Word grid with water droplet (💧) symbols hiding letters
- **Method:** H2O count → index positions; crossword clues fill hidden letters
- **Grid:** 9×9 with 14 water droplets
- **Clues:** 13 crossword-style clues (cold noise, natural disaster, etc.)
- **Intermediate crossword answers:** ~13 entries generated

### Puzzle 2: Changing the Lives of 600 Strangers → CHALLENGE
- **Type:** 9×9 Sudoku using letters LIFECHANG instead of digits 1-9
- **Solved grid:**
```
H L F C A N E G I
C E N F G I L H A
A I G E H L N F C
G N I L E F C A H
L H C G I A F E N
F A E H N C I L G
E F A N C G H I L
N G H I L E A C F
I C L A F H G N E
```
- **Mapping:** L=1,I=2,F=3,E=4,C=5,H=6,A=7,N=8,G=9
- **Extraction:** Box pattern → CHALLENGE

### Puzzle 3: I Cleaned The World's Dirtiest Beach → LEADS
- **Type:** TV show identification + crossword clue generation
- **Initial debris:** AABBCCCDDFFFGGGGIIIKKKKLLMNNPRRSSSTTWWY
- **Method:** 19 TV shows identified by genre+year → paired with "after cleanup" definitions
- **19 crossword answers generated:** HAFT, DITHERING, HOWITZERS, SCENARIO, ABASH, NEUROTIC, HEARTED, HIGHHEELS, SCREENER, INTRODUCTIONS, MATTER, OPERA, ALLUSIONS, RESISTIVE, ABSOLUTE, ERASE, TEAMSEAS, TRITE, MUSTERS
- **Coordinate pairs:** 19 two-letter pairs with (x,y) coords for grid placement
- **Final extraction:** "Chief roles or metals with symbol Pb" → LEADS

### Puzzle 4: $1 vs $500,000 Experiences → TOWARDS
- **Type:** 21 colored letter strips (anagram place names)
- **Method:** Each strip = scrambled street/place name from MrBeast's travels
- **Extraction:** White letter overlay (Boolean intersection) → TOWARDS
- **21 place names = 21 potential crossword entries**

**Visible strips (from image):**
GLENEAGRY, WASCANA, ORTTEL, WESTASUKA, CAMOIN, LSIPAIGER, MCOLLY, F.LIROKA, CHALOGEN, RLCHANOA, COLFAA, JUASDEAQYAS, DOVERCOURT, GOCKENREST, MARIAAGLEN, MCGUCRIAN, AALVIOG, LOSTHER, ATGIPSCY, RIMTOS, CLDMCGREGOY

### Puzzle 5: Pokemon Go Stereotypes → LOCATION
- **Type:** Cage bars grid with Pokedex numbers
- **Method:** Numbers → Pokemon names → cage shapes placed in grid → column intersections
- **Cage bar numbers:** 142,200,261,343,439,696,803,947,961,1006 (horizontal) + 138,148,175,266,276,441,791,852 (vertical)
- **Extraction:** Intersecting columns spell LOCATION

### Puzzle 6: $10,000 Every Day You Survive in the Wilderness → NAME
- **Type:** 16×16 tent placement logic puzzle
- **Method:** Place tents adjacent to trees (no touching), numbers show row/col counts
- **Extraction:** Row+column sums → compound word completions → NAME (4 letters)
- **Rule:** "Quartet after pen" = pen+NAME, brand+NAME, etc.

### Puzzle 7: I Adopted 100 Dogs → SOMEWHERE
- **Type:** 100 cartoon dogs with 5-circle Venn diagram
- **Categories:** Ears up, Toy bone, Spots, Collar, Wiggling tail
- **Method:** Count dogs per Venn region → line drawing cipher → Coppola film reference
- **Extraction:** SOMEWHERE (9 letters)

### Puzzle 8: I Spent 100 Hours Inside the Pyramids → AROUND
- **Type:** Pyramid-shaped grid with 43 clues (left side down-left, right side down-right)
- **Method:** 4 vowel pyramids (A, E, I, O), each builds words line by line
- **43 crossword answers generated (these ARE crossword clues!):**

**I-Pyramid answers:**
OI, ION, TONI, PINTO, OPTION, PORTION, POSITRON, RATPOISON, STAINPROOF, OUTFORASPIN

**A-Pyramid answers:**
RA, RAD, DORA, ADORN, AROUND, ROTUNDA (+ more lines)

**E-Pyramid answers:**
ER, ERA, RACE, LECAR, ECLAIR, CALIBER, CABRIOLET, ORBICULATE, CIRCLEABOUT

**O-Pyramid answers:**
NO, EON, NOTE, TONER, ORIENT, INUTERO, ROUTINES, OUTLINERS, RESOLUTION, REVOLUTIONS

- **Extraction:** Missing 6th line of A-pyramid = AROUND

### Puzzle 9: Anything You Can Fit in the Circle I'll Pay For → WORLD
- **Type:** Two geodesic spheres (red/blue highlighted sections) + letter string
- **String:** ZXPCHAIRSQUORUMSFLAMINGOPUSHCONVEXOFWEHIRPLED
- **Hidden words:** ZIP, CHAIRS, QUORUMS, FLAMINGO, PUSH, CONVEX, OF, WE, HIRPLED
- **Note:** X and A have strikethroughs in the image
- **Method:** Colored triangle sections on spheres → position index → extract from words
- **Extraction:** Homophone of "WHIRLED" → WORLD
- **9 crossword answers:** ZIP, CHAIRS, QUORUMS, FLAMINGO, PUSH, CONVEX, OF, WE, HIRPLED

---

## 4. SUPER BOWL AD PUZZLES <a name="ad-puzzles"></a>

### SOLVED (6/32):

| # | Puzzle | Answer | Method |
|---|--------|--------|--------|
| 1 | Red-outlined bills | CASHTENT (8) | Bill denominations → A=1 alphabet |
| 2 | Birds on wire | DOMAIN ID | Birds-on-wire cipher (online) |
| 3 | Vault door rings | ACCRA GHANA | Scrabble TWL tile values |
| 4 | Morse code light | (community solved) | Morse code |
| 5 | YouTube hidden text | CONTRADICTION (13) | Text analysis |
| 6 | Buried alive reference | 6 FEET DOWN BY THE CROSS | Direct |

### UNSOLVED (26) — Organized by available data:

#### HIGH PRIORITY (data available, can analyze now):

**A. "Find puzzle maker" numbers:**
`11,6,2,12,4,7,8,13,7,3,13,11,8,9,7,12,1,11,9,4`
→ Indexed into "LONESHARKGAMES" → **"A HOME AREA NEAR KAM LAKE"**
→ = **YELLOWKNIFE, CANADA** (Kam Lake is in Yellowknife!)

**B. Jersey numbers:**
`597, 482, 374, 990, 723, 240, 478, 531, 109, 237, 453, 499, 930`
- 13 three-digit numbers
- Theories: digit sums, phone keypad, coordinate pairs
- Digit sums: 21,14,14,18,12,6,19,9,10,12,12,22,12
- As A=1: U,N,N,R,L,F,S,I,J,L,L,V,L → no clear word yet
- COULD BE: row/column/grid indices for crossword cells

**C. Check routing number: 650283979**
- 650 = San Francisco Bay Area code → **SAN FRANCISCO** (Salesforce HQ!)
- As A=1: F,E,_,B,H,C,I,G,I

**D. Check account number: 5480234354**
- 548 = Ontario, Canada area code

**E. Tank number: 3634826-1** (with ghost symbol)
- Tank text also reportedly reads "IPESIT" → anagram of **"SITE IP"**
- Combined with DOMAIN ID from birds cipher → hidden website exists
- QR code on tank (rivet pattern) — two halves overlap to form complete QR

**F. Smoke grenade: "{+1=?"**
- Mathematical hint: add 1 to something
- "Look +1 cube" instruction (from camera note) connects
- Red Rubik's cube always appears → cube+1 = ?

**G. ATSEI 44 on shirt:**
- ATSEI anagram = **SATIE** (Erik Satie, French composer)
- 44 could be: opus number, key, or separate clue

**H. Clock times (four world clocks):**
- Tokyo, London, Chicago, New York
- Specific times visible in BTS photos — need exact reading
- Times likely encode something (positions, numbers, letters)

**I. 10^5 on monitor = 100000**
- Five zeros? 5-letter word? "HUNDRED THOUSAND"?

**J. "$673" — "@Accounting the elephant ate $673"**
- Phone keypad: 6=MNO, 7=PQRS, 3=DEF → ORE/ORD/MPD/etc.
- Twitter account @elephant85673 may be related

**K. Combination lock: 020826**
- = Super Bowl date (02/08/26)
- Reference point for other date-based ciphers

**L. Camera code B002C004, timecode 4:11:44:18**
- B002C004 in hex = 2952970244
- Timecode format HH:MM:SS:FF — possibly a frame reference

**M. Numbers 001400 / 012800**
- Two values seen on screens
- 001400 and 012800 — military time? Coordinates?

#### NEED VIDEO FRAME ACCESS (26):
| Puzzle | Description | Priority |
|--------|-------------|----------|
| Red Rubik's cube | All red, multiple appearances, n²=n³ theory | HIGH |
| Backwards license plate | REVERSED text = domain/IP/URL | CRITICAL |
| Crosswalk (CGI) | Unusual CGI crosswalk effect | MEDIUM |
| Barcode on tank (full) | Need clearer frame | HIGH |
| Swiss alps/flag on screen | Switzerland reference | MEDIUM |
| Macon Coffee cup | Georgia ref but filmed in LA | LOW |
| Bank withdrawal slip | Dated 2/5, numbers visible | MEDIUM |
| Parking ticket | Dated 2/8 = Super Bowl | LOW |
| Two different belts | Color X pattern → flags? | HIGH |
| Clipboard paper | Operating Capital Expenses list | MEDIUM |
| Spider | Flash-frame symbol | MEDIUM |
| Sine wave | Frequency pattern | MEDIUM |
| Calendar dates (Mrs. Maybelle) | Circled: Jan 1, Feb 2, Mar 1, Mar 3 = "1,2,1,3" | HIGH |
| Chrome vs matte spheres | Binary encoding? | MEDIUM |
| 11 influencer puzzles | Each influencer = separate clue | HIGH |

---

## 5. THE CROSSWORD — CRITICAL PATH <a name="crossword"></a>

### Grid Facts:
- **Size:** 21×21
- **Entries:** 176 total (90 Across, 86 Down)
- **Black squares:** ~10% (unusually low = more interconnected)
- **Circled cells:** ~16 (for final code extraction)
- **Only printed clue:** 167 Across (16 characters)
- **Staircase grid:** Bottom-right corner, 11 rows — likely shows the 11 hidden location names

### Across Entry Numbers (90):
1, 8, 14, 22, 23, 24, 25, 28, 29, 30, 31, 32, 34, 35, 36, 38, 41, 42, 43, 45, 47, 48, 50, 54, 57, 58, 59, 61, 63, 64, 66, 68, 70, 72, 73, 77, 79, 80, 81, 82, 83, 85, 88, 90, 91, 92, 94, 97, 99, 100, 102, 103, 105, 106, 107, 109, 111, 113, 114, 117, 119, 120, 121, 123, 124, 127, 129, 132, 134, 136, 138, 141, 143, 145, 148, 153, 155, 156, 158, 159, 161, 164, 165, 167, 171, 172, 173, 174, 175, 176

### Down Entry Numbers (86):
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 26, 27, 33, 37, 39, 40, 43, 44, 46, 49, 51, 52, 53, 55, 56, 60, 62, 65, 67, 69, 71, 72, 74, 75, 76, 77, 78, 80, 83, 84, 86, 87, 89, 93, 95, 96, 98, 101, 104, 108, 110, 112, 115, 116, 117, 118, 122, 124, 125, 126, 128, 130, 131, 133, 135, 137, 139, 140, 141, 142, 144, 150, 151, 152, 154, 157, 160, 162, 163, 166, 168, 169, 170

### 167 Across — THE META CLUE
- **Length:** 16 characters
- **Clue:** "What this puzzle commemorates in eleven hidden words in the theme entries"
- **Top candidate:** CHANGINGTHEWORLD (16 letters) ← "Changing the World" fits MrBeast's brand
- **Other candidates:** CHARITYCHALLENGE (16), PHILANTHROPYWORK (16)
- **The 11 hidden words** are LOCATION NAMES hidden consecutively within theme entries

### Circled Cell Positions (from PDF analysis):
Circled cells appear at specific numbered positions in the grid. These 16 letters, read in standard crossword order (left-to-right, top-to-bottom), form the FINAL CODE.

---

## 6. KNOWN CROSSWORD ANSWERS <a name="known-answers"></a>

### From Puzzle 3 (Beach — 19 answers):
| Answer | Length | Clue |
|--------|--------|------|
| HAFT | 4 | Axe's handle |
| DITHERING | 9 | Failing to make a decision |
| HOWITZERS | 9 | Short cannons |
| SCENARIO | 8 | Hypothetical sequence of events |
| ABASH | 5 | Make embarrassed |
| NEUROTIC | 8 | Paranoid, say |
| HEARTED | 7 | Follows "half" or "broken" |
| HIGHHEELS | 9 | Making oneself taller |
| SCREENER | 8 | Advance copy of a movie |
| INTRODUCTIONS | 13 | Hosts' spiels bringing out guests |
| MATTER | 6 | Anything that takes up space |
| OPERA | 5 | Browser or performance |
| ALLUSIONS | 9 | Indirect literary references |
| RESISTIVE | 9 | Pressure-detecting touchscreen |
| ABSOLUTE | 8 | Complete and unqualified |
| ERASE | 5 | Remove all traces of |
| TEAMSEAS | 8 | Jimmy and Mark's ocean charity |
| TRITE | 5 | Burnt or hackneyed |
| MUSTERS | 7 | Assembles British soldiers |

### From Puzzle 8 (Pyramids — 43 answers):
**I-Pyramid (11 lines):**
OI(2), ION(3), TONI(4), PINTO(5), OPTION(6), PORTION(7), POSITRON(8), RATPOISON(9), STAINPROOF(10), OUTFORASPIN(11)

**A-Pyramid (11 lines):**
RA(2), RAD(3), DORA(4), ADORN(5), AROUND(6), ROTUNDA(7), [8-11 need solving]

**E-Pyramid (11 lines):**
ER(2), ERA(3), RACE(4), LECAR(5), ECLAIR(6), CALIBER(7), CABRIOLET(9), ORBICULATE(10), CIRCLEABOUT(11)

**O-Pyramid (11 lines):**
NO(2), EON(3), NOTE(4), TONER(5), ORIENT(6), INUTERO(7), ROUTINES(8), OUTLINERS(9), RESOLUTION(10), REVOLUTIONS(11)

### From Puzzle 9 (Circle — 9 answers):
ZIP(3), CHAIRS(6), QUORUMS(7), FLAMINGO(8), PUSH(4), CONVEX(6), OF(2), WE(2), HIRPLED(7)

### From Super Bowl Ad (6 answers):
CASHTENT(8), DOMAINID(?), ACCRAGHANA(?), CONTRADICTION(13), SIXFEETDOWNBYTHECROSS(?)

### TOTAL KNOWN: ~77 answers (of 176 needed)

---

## 7. VISUAL CLUE ANALYSIS <a name="visual-clues"></a>

### Belt Cipher (BTS Photo):
- **Visible X colors (left to right):** Red, Blue/Cyan, Red, Green, Yellow/Gold, Blue, White/Silver, Green
- **Could map to:** Semaphore flags, international maritime signal flags, country flag colors
- **Theory:** Each color sequence = a country → 11 locations

### Four World Clocks (BTS Photo):
- **Cities:** Tokyo (top-left), London (top-right), Chicago (bottom-left), New York (bottom-right)
- **Need exact times** — these likely encode numbers or positions

### Mrs. Maybelle's Calendar:
- **2026 calendar visible** on desk (upside down)
- **Circled dates:** January 1, February 2, March 1, March 3
- **Pattern:** 1, 2, 1, 3 → could be extraction indices, or "ABAC" pattern

### QR Code on Tank:
- **Two halves** of a QR code formed by rivet/stud pattern on tank
- **"The two sides overlap perfectly with not 'doubling up'"**
- When overlaid → scannable QR code → likely links to hidden website
- Connects to: DOMAIN ID (birds cipher) + SITE IP (IPESIT anagram)

### Smoke Grenade: "{+1=?"
- Mathematical operation: something + 1 = ?
- Camera note says "Look +1 cube"
- Red Rubik's cube appears everywhere → cube + 1 = TESSERACT? 4D hypercube?
- Or: current value +1 = next in sequence

### Magazine Clue:
- **CEO Today** magazine featuring **Marc Benioff** (Salesforce CEO)
- "CEO of the Year" visible
- A **watch/clock** is visible on the opposite page — time readable as potential clue

---

## 8. LOCATION THEORY — 11 HIDDEN WORDS <a name="locations"></a>

The 9-word sentence tells us to find **location names hidden in the crossword's theme entries.** These are places where MrBeast filmed challenge videos.

### Confirmed/Likely Locations:
| # | Location | Source Evidence |
|---|----------|----------------|
| 1 | **KENYA** | Video 1: Built 100 Wells in Africa (Kenya specifically) |
| 2 | **ACCRA, GHANA** | Vault door Scrabble cipher (confirmed) |
| 3 | **YELLOWKNIFE, CANADA** | "Find puzzle maker" numbers → KAM LAKE |
| 4 | **SAN FRANCISCO** | 650 area code in routing number (Salesforce HQ) |
| 5 | **DOMINICAN REPUBLIC** | Video 3: Dirtiest Beach was DR |
| 6 | **DUBAI** | Video 4: $1-$500K Experiences |
| 7 | **EGYPT/GIZA** | Video 8: 100 Hours in Pyramids |
| 8 | **GREENVILLE, NC** | MrBeast's hometown, P1 clue reference |
| 9-11 | Unknown | Could be from videos 5,6,7,9 locations |

### Where Locations Hide in Crossword:
Hidden locations appear as **consecutive letters within longer theme entries**, e.g.:
- CABRIOLET → contains **RIO** (R-I-O)
- CIRCLEABOUT → could contain a location
- INTRODUCTIONS → 13 letters, likely theme entry
- CONTRADICTION → 13 letters, likely theme entry
- REVOLUTIONS → 11 letters, possible theme
- STAINPROOF → 10 letters, possible theme

### The Staircase Grid (Bottom-Right):
The small staircase-shaped grid in the crossword PDF likely represents the 11 hidden location names arranged in descending length, providing a visual guide for extraction.

---

## 9. CONFIRMED RED HERRINGS <a name="red-herrings"></a>

| # | Red Herring | How We Know |
|---|-------------|-------------|
| 1 | "Red Herring Bank" | Literally named after the concept |
| 2 | Acrostic poem | Spells "THIS MEANS NOTHING I JUST WANTED TO WASTE YOUR TIME LOL" |
| 3 | Smoke device MrBeast holds | Dismissed in the ad dialogue itself |

---

## 10. CRITICAL NEXT STEPS <a name="next-steps"></a>

### IMMEDIATE (can do now):
1. **Map crossword grid entry lengths** — Count squares for each of the 176 entries from the PDF
2. **Match known answers by length** — Place the ~77 known answers into entries of matching length
3. **Use crossing letters for constraint propagation** — Where answers cross, check letter consistency
4. **Research remaining Puzzle 8 answers** — A-pyramid lines 8-11 still unknown
5. **Decode QR code from tank** — Reconstruct from two-half overlay image
6. **Identify all 21 place names from Puzzle 4** — Unscramble each colored strip

### REQUIRES VIDEO ANALYSIS:
7. **Read backwards license plate** → hidden URL
8. **Read exact clock times** from four world clocks
9. **Count pennies in jar** → number clue
10. **Solve all 26 remaining ad puzzles** → crossword answers
11. **Identify 11 influencer puzzles** → 11 more answers

### CROSSWORD SOLVING PHASE:
12. **Build constraint satisfaction solver** — Python script
13. **Fill grid with known answers** → use crossings to validate
14. **Identify theme entries** (longest Across entries)
15. **Search for 11 hidden location names** in theme entries
16. **Determine 167 Across answer** (16 characters)
17. **Extract 16 circled cell letters** → final code
18. **SUBMIT TO SLACKBOT**

### MONITOR:
19. Check mrbeast.salesforce.com for new hints (24hr/48hr release cycle)
20. Monitor Lone Shark Games Discord for community breakthroughs
21. Check Reddit r/mrbeast and r/puzzles daily

---

## 11. QUESTIONS FOR SLACKBOT <a name="slackbot-questions"></a>

When the Slackbot at mrbeast.salesforce.com becomes interactive, ask:

### About Puzzle Structure:
- "How many total puzzles are in Stage 1?"
- "Is the crossword the gateway to Stage 2?"
- "How many stages are there total?"
- "Are all 176 crossword entries clued by the puzzles, or are some standard fill?"

### About Specific Puzzles:
- "What does the red Rubik's cube represent?"
- "What do the four world clocks encode?"
- "Is the QR code on the tank scannable?"
- "What cipher is used for the jersey numbers?"
- "What does {+1=? on the smoke grenade mean?"

### About the Crossword:
- "How many circled cells are in the crossword?"
- "Is 167 Across the final answer or just a meta-clue?"
- "Are the 11 hidden words all country names or could they be cities?"
- "Does the staircase grid in the corner relate to the 11 hidden words?"

### About Progress:
- "Has anyone correctly filled more than half the crossword?"
- "Are we missing any puzzle sources beyond the ad, bank, and variety puzzles?"
- "Will more hints be released?"

---

## APPENDIX A: CIPHER REFERENCE

| Cipher | Where Used | How It Works |
|--------|-----------|--------------|
| A=1 (Simple substitution) | Multiple | A=1, B=2, ... Z=26 |
| Reverse alphabet | Twitter elephant msg 2 | A=26, B=25, ... Z=1 |
| Birds-on-wire | Ad room 2 | Online cipher alphabet |
| Scrabble TWL values | Vault door | Standard tile point values |
| Morse code | Ad light flashes | Dots and dashes |
| Phone keypad | 3634826 → ENDGAME? | 2=ABC, 3=DEF, etc. |
| Letter indexing | "Find puzzle maker" | Numbers index into a known string |
| Boolean overlay | P4 white letters | Intersection of colored letter sets |

## APPENDIX B: KEY URLS

- Contest site: https://mrbeast.salesforce.com
- 9-video playlist: https://www.youtube.com/playlist?list=PLj-VLkYRjRxm5HVGFVpPP5W7jkvvzd1q7
- Lone Shark Games Discord: https://lonesharkgames.com/discord
- Crossword PDF: https://lonesharkgames.com/wp-content/uploads/2026/02/Million-Dollar-Crossword.pdf
- ARGNet coverage: https://argn.com/2026/02/start_slacking_off_with_mrbeasts_million_dollar_puzzle_hunt/
- Red Herring Bank Wiki: https://wiki.redherringbank.com
- Reddit puzzle poster: u/BeastForce67
- Community Google Doc: https://docs.google.com/document/d/1ghb_zIRVLNlt2oRNyMBWeP3ZqWT-lnX59ePXoMKAkSw/

---

*Analysis compiled by Claude Code — Session Feb 12, 2026*
*This document should be updated as new hints and community findings emerge.*
