# Additional Crossword Answers from Puzzles 2, 4, 5, 6, 7, 9

## Summary

| Puzzle | Mechanism | Likely Crossword Entries | Count | Confidence |
|--------|-----------|------------------------|-------|------------|
| P2 (Sudoku) | Fill grid → box pattern → CHALLENGE | None | 0 | HIGH (none exist) |
| P4 (Experiences) | 21 strips → 21 place names → extract TOWARDS | 21 place names | 21 | HIGH that they exist; LOW on identities |
| P5 (Pokemon) | 18 Pokedex → 18 Pokemon → grid → LOCATION | 18 Pokemon names (proper nouns) | 18 | LOW (proper nouns unlikely in crossword) |
| P6 (Tents) | Tent counts → clue phrases → NAME | None | 0 | HIGH (none exist) |
| P7 (Dogs) | Venn lines → encoded string → ONE | None | 0 | HIGH (none exist) |
| P9 (Circle) | Hidden words in string → geodesic extraction → WORLD | 9 hidden words | 9 | MODERATE-HIGH |

**New potential entries: 21 (P4) + 9 (P9) = 30 entries (high confidence)**
**Plus 18 (P5) = 48 entries if Pokemon names count (low confidence)**

---

## Puzzle 2: LIFECHANG Sudoku → CHALLENGE

### Mechanism
- 9x9 Sudoku grid using letters L, I, F, E, C, H, A, N, G (instead of 1-9)
- Solve the Sudoku (standard rules, one of each letter per row/column/box)
- "Box pattern" extraction: read one specific cell from each of the 9 3x3 boxes
- The 9 extracted letters spell CHALLENGE

### Solved Grid
```
H L F | C A N | E G I
C E N | F G I | L H A
A I G | E H L | N F C
------+-------+------
G N I | L E F | C A H
L H C | G I A | F E N
F A E | H N C | I L G
------+-------+------
E F A | N C G | H I L
N G H | I L E | A C F
I C L | A F H | G N E
```

### Analysis: Does P2 Generate Crossword Entries?

**NO.** The Sudoku is a purely mechanical puzzle with a single extraction step.

Reasons:
1. **No intermediate clue-answer pairs.** Unlike P3 (which had 19 TV shows + 19 "after cleanup" crossword clues) or P8 (which had 43 crossword-format clues for pyramid words), P2 has zero side clues, definitions, or intermediate words.
2. **Every row/column/box contains the same 9 letters** (LIFECHANG). No row or box spells a meaningful word in any reading order.
3. **The "box pattern" is a single extraction**, not a multi-word generation process.
4. **The given cells** (the visible letters that let you solve the Sudoku) don't encode additional words when read in any obvious order.

### Crossword Entries from P2: **0**

---

## Puzzle 4: $1-$5000 Experiences → TOWARDS

### Mechanism
- 21 strips with scrambled colored text
- Instruction: "I went all over the world for these experiences. Where did I go?"
- Each strip shows a "boolean intersection" of two letter layers:
  - **Colored letters** (outer shape) = one letter per position
  - **White letters** (inner cutout) = a different letter per position
- The colored letters, when unscrambled per strip, form **21 real place names** (locations MrBeast visited)
- The white letters (hidden inside) are extracted to spell **TOWARDS**
- Belt from commercial may indicate how to pair/layer strips (3 strips of each color, 7 colors)

### The 21 Strips (Raw Text from Image)

Reading the image top-to-bottom, left-to-right:

| # | Strip Text (as visible) | Letters | Color(s) | Possible Place Name |
|---|------------------------|---------|----------|-------------------|
| 1 | GLENCA.RY | ~9 | Red/multi | GRAN CANARY / GLENGARRY |
| 2 | WASCANY | 7 | Purple | SWANSEA? / TUSCANY? |
| 3 | OITTEL | 6 | Red | ? |
| 4 | WESTASKA | 8 | Red/green | WEST ALASKA? / KEY WEST + AK? |
| 5 | CAMOIN | 6 | Orange | MONACO (M,O,N,A,C,O)? |
| 6 | LSIPAIZER | 9 | Green | LEIPZIGER → LEIPZIG? |
| 7 | MCOLLY | 6 | Purple | ? |
| 8 | F.LIROKA | ~8 | Red/purple | FLORIDA? / SRI LANKA? |
| 9 | CHALOGEN | 8 | Yellow | LONG BEACH? / HONG KONG? |
| 10 | BLCHANON | 8 | Green | BUCHANAN? |
| 11 | COLFAA | 6 | Yellow | COLFAX? |
| 12 | JUASDFAQYAS | 11 | Purple | ? |
| 13 | COVERCOURT | 10 | Green | DOVERCOURT? / VANCOUVER? |
| 14 | GRCKINGREST | 11 | Green/red | ? |
| 15 | MALIAAQLEN | 10 | Red | ? |
| 16 | MCGUCRIAN | 9 | Green | NICARAGUA? (N,I,C,A,R,A,G,U,A=9) |
| 17 | AALVISC | 7 | Red | ? |
| 18 | LOSTHER | 7 | Blue | ? |
| 19 | ATCIPSCY | 8 | Purple | CAPACITY? / ATLANTIC CITY? |
| 20 | NIMTOS | 6 | Red | MINTOS? / TIMONS? |
| 21 | LLIMCGREGOY | 11 | Yellow/green | MCGREGOR? / MONTGOMERY? |

### Key Insight from Discord
- arcometric: "ignore the colored letters, the letters are white, overlayed over the colored ones"
- jerrycid_49702 initially tried Gran Canaria, Madagascar, Montreal (most were wrong)
- t334: "21 for both" and "3 of each color"
- vattenskog claims to have solved it but won't share
- The boolean intersection means the visible letter shapes are COMPOSITE of two overlapping letters

### Assessment: Are the 21 Place Names Crossword Entries?

**HIGH PROBABILITY.** Here's why:

1. **Count fits.** 21 entries from P4 would bring our total from 71 to 92. Combined with P9's 9 hidden words, that's 101 total. The remaining ~75 would come from P8's missing entries (4-5), P5's possible entries, and the main video puzzles.

2. **Theme alignment.** The crossword's theme is "eleven hidden words in the theme entries" and the 9-word sentence says "EVERY CHALLENGE LEADS TOWARDS LOCATION NAME ONE AROUND WORLD." Place names from MrBeast's challenges are exactly what should be in this crossword.

3. **Structural parallel.** P3 generates 19 crossword answers (clue-answer pairs). P4 generating 21 answers (place names) is structurally analogous — each strip is one entry.

4. **Concern:** Place names are proper nouns, which are less common in standard crosswords. However, this is a custom puzzle by Lone Shark Games where the entire theme is about real-world locations. Mike Selinker regularly incorporates proper nouns in meta-puzzles.

### What We Still Need
- High-resolution image analysis to separate the two letter layers in each strip
- OR community identification of all 21 place names
- The belt color key may indicate how to pair strips for the overlay extraction

### Crossword Entries from P4: **~21 place names (identities mostly unknown)**

---

## Puzzle 5: Pokemon Go Stereotypes → LOCATION

### Mechanism
- 18 Pokedex numbers map to 18 Pokemon names
- Each Pokemon name fills a row of the internal crossword-style grid
- "Cage bars" (patterns of blue/white squares) show which cells correspond to each Pokemon
- When all 18 names are placed in the grid:
  - Right column intersections going down: L-O-C-A-T-I-O-N = **LOCATION**
  - Left column intersections going down: S-O-L-O-U-T-I-O-N = **SOLOUTION** (≈ SOLUTION)
  - S at top right completes: **"SOLUTION IS LOCATION"**

### The 18 Pokemon Names

| # | Pokedex | Pokemon | Length |
|---|---------|---------|--------|
| 1 | 142 | AERODACTYL | 10 |
| 2 | 200 | MISDREAVUS | 10 |
| 3 | 261 | POOCHYENA | 9 |
| 4 | 343 | BALTOY | 6 |
| 5 | 439 | ARCEUS | 6 |
| 6 | 696 | TYRUNT | 6 |
| 7 | 803 | POIPOLE | 7 |
| 8 | 947 | BRAMBLEGHAST | 12 |
| 9 | 961 | WUGTRIO | 7 |
| 10 | 1006 | IRONVALIANT | 11 |
| 11 | 138 | OMANYTE | 7 |
| 12 | 148 | DRAGONAIR | 9 |
| 13 | 175 | TOGEPI | 6 |
| 14 | 266 | SILCOON | 7 |
| 15 | 276 | TAILLOW | 7 |
| 16 | 441 | CHATOT | 6 |
| 17 | 791 | SOLGALEO | 8 |
| 18 | 852 | CLOBBOPUS | 9 |

### Assessment: Are the 18 Pokemon Names Crossword Entries?

**LOW PROBABILITY.** Here's why:

1. **Proper nouns.** All 18 are Pokemon character names — proper nouns from a specific franchise. Standard crosswords rarely use proper nouns, and a Mike Selinker crossword would be less likely to include 18 Pokemon names among 176 entries.

2. **No clue-answer format.** Unlike P3 (which generated real crossword clue-answer pairs like "Axe's handle → HAFT") or P8 (which had crossword clues for each pyramid word), P5 has no intermediate clue text. The Pokemon names are just identified by Pokedex number.

3. **Self-contained grid.** The internal grid in P5 is purpose-built for the Pokemon names to interlock and spell the extraction message. It's not the Million Dollar Crossword.

4. **However:** If the crossword includes entries from ALL puzzle types, Pokemon names could appear. The crossword is custom-made, so there are no "standard" restrictions. And 18 entries would account for a significant chunk of the 176 needed.

5. **Alternative possibility:** The P5 internal crossword grid might generate additional words at intersections beyond the Pokemon names themselves. Without seeing the filled grid, this is unverifiable.

### If Pokemon Names ARE Entries (for reference)

| Pokemon | Length | Notes |
|---------|--------|-------|
| AERODACTYL | 10 | |
| MISDREAVUS | 10 | |
| POOCHYENA | 9 | |
| BALTOY | 6 | |
| ARCEUS | 6 | |
| TYRUNT | 6 | |
| POIPOLE | 7 | |
| BRAMBLEGHAST | 12 | Theme entry candidate (could hide location) |
| WUGTRIO | 7 | |
| IRONVALIANT | 11 | Theme entry candidate (could hide IRAN or OVAL) |
| OMANYTE | 7 | Could hide OMAN (location!) |
| DRAGONAIR | 9 | Could hide DRAGON, NAIROBI if rearranged? No — but AGONAIR... |
| TOGEPI | 6 | |
| SILCOON | 7 | Could hide SILICON |
| TAILLOW | 7 | |
| CHATOT | 6 | |
| SOLGALEO | 8 | Could hide GALEO, SOLE, SOL |
| CLOBBOPUS | 9 | Could hide LOBBO, OPUS |

**Notable: OMANYTE contains OMAN (a real country/location).** If theme entries contain hidden location names, and OMANYTE is an entry, OMAN could be one of the 11 hidden words.

### Crossword Entries from P5: **18 Pokemon names (LOW confidence)**

---

## Puzzle 6: Wilderness Tents → NAME

### Mechanism
- 16x16 Tents logic puzzle (trees, numbers along edges)
- Place tents next to trees following standard Tents rules:
  - One tent per tree, horizontally or vertically adjacent
  - No tent touches another tent (even diagonally)
  - Row/column numbers indicate tent count in that direction
- After solving the tent placement:
  - Row tent counts → converted to letters → "QUARTET AFTER PEN"
  - Column tent counts → converted to letters → "BRAND LAST USER"
- Interpretation: All are compound-word completions with NAME:
  - PEN + NAME = penname
  - QUARTET = four letters = NAME
  - AFTER + NAME = aftername (or: "quartet after pen" = 4-letter word after PEN = NAME)
  - BRAND + NAME = brandname
  - LAST + NAME = lastname
  - USER + NAME = username
- Answer: **NAME**

### Analysis: Does P6 Generate Crossword Entries?

**NO.** The puzzle produces two clue phrases from numerical tent counts, not a list of word-level answers.

Reasons:
1. **No intermediate words.** The tent placement process is purely logical (constraint satisfaction). There are no clue-answer pairs, no word lists, no labeled elements.
2. **The row/column sums encode phrases, not individual words.** The sums convert to "QUARTET AFTER PEN" and "BRAND LAST USER" — these are clue PHRASES, not crossword entry answers.
3. **The compound words** (penname, brandname, lastname, username) are the solving logic, not crossword entries. They all point to the single answer NAME.
4. **No visible side clues or numbered entries** in the puzzle image.

### Could the Tent Positions Encode Something Else?

Theoretically, the solved tent positions in the 16x16 grid could encode additional data:
- Tent positions as binary per row → letters (but row sums already used for extraction)
- Tent positions forming a visual pattern (like a shape or letter)
- Coordinates of tents mapping to crossword positions

None of these have been identified by the community, and the puzzle appears fully solved with the NAME answer.

### Crossword Entries from P6: **0**

---

## Puzzle 7: I Adopted 100 Dogs → ONE

### Mechanism
- 100 dogs in a 10x10 grid, each with 5 binary features:
  1. Ears up?
  2. Toy bone?
  3. Spots?
  4. Collar?
  5. Wiggling tail?
- 5-circle Venn diagram (bottom-left) corresponds to the 5 questions
- Lines drawn from each question to matching dogs spell letters
- Full encoded string: "JUST A HUNDRED EXQUISITELY FUZZY PUPPIES CAN BE VIEWED LIKE AN ADVERB, A NUMBER FROM A SPIELBERG MOVIE, OR A FILM BY COPPOLA"
- Interpretation:
  - "Just a hundred" + 1 more = 101 → **101 Dalmatians** (adverb: "one hundred and one")
  - "Number from a Spielberg movie" → **Ready Player ONE** (Spielberg produced)
  - "Film by Coppola" → **ONE from the Heart** (Francis Ford Coppola, 1982)
  - All three point to: **ONE**

### Analysis: Does P7 Generate Crossword Entries?

**NO.** The puzzle produces a single long encoded string, not multiple intermediate words.

Reasons:
1. **Single encoded output.** The line-drawing mechanism produces one continuous message. There are no separate clue-answer pairs.
2. **No labeled intermediate steps.** Unlike P3 (which had 19 TV shows as an intermediate layer before the "after cleanup" answers), P7 goes directly from dog features to encoded string to answer.
3. **The movie references are interpretive, not entry-level.** "101 Dalmatians," "Ready Player One," and "One from the Heart" are referenced in the encoded text as solving hints, not as crossword entries. They're too long for typical entries (13, 14, and 16 letters respectively).
4. **The 100 dogs are visual elements, not word generators.** Each dog is a combination of binary features, not a named/labeled entity that could produce a word.

### Could the Dog Data Encode Something Else?

- Each dog has a 5-bit feature signature (e.g., ears=1, bone=0, spots=1, collar=1, tail=0). With 100 dogs and 5 bits each, that's 500 bits of data.
- The Venn diagram has 2^5 = 32 possible regions. Some dogs fall in specific regions.
- The COUNT of dogs per region could encode data. But nobody has found additional extraction here.

### Crossword Entries from P7: **0**

---

## Puzzle 9: Anything You Can Fit in the Circle → WORLD

### Mechanism
- Text string: **ZIPCHAIRSQUORUMSFLAMINGOPUSHCONVEXOFWEHIRPLED**
  - (Note: original text has X marks through certain characters; confirmed string uses ZIP not ZXP)
- 9 hidden words concatenated in the string:
  1. ZIP (positions 1-3)
  2. CHAIRS (positions 4-9)
  3. QUORUMS (positions 10-16)
  4. FLAMINGO (positions 17-24)
  5. PUSH (positions 25-28)
  6. CONVEX (positions 29-34)
  7. OF (positions 35-36)
  8. WE (positions 37-38)
  9. HIRPLED (positions 39-45)
- Geodesic spheres with colored triangles indicate extraction positions
- Triangle counts give character positions: [5,12,20,24,25,28,30,31,33,35,36,37,39,40,41,43,44,45]
- Extracted letters: **HOMOPHONEOFWHIRLED** = "HOMOPHONE OF WHIRLED"
- WHIRLED sounds like WORLD → Answer: **WORLD**

### The 9 Hidden Words as Crossword Entries

| # | Word | Length | Standard English? | Crossword Viable? |
|---|------|--------|-------------------|-------------------|
| 1 | ZIP | 3 | Yes (speed, zero, fastener) | Yes |
| 2 | CHAIRS | 6 | Yes (furniture, presides) | Yes |
| 3 | QUORUMS | 7 | Yes (minimum voting members) | Yes |
| 4 | FLAMINGO | 8 | Yes (pink bird) | Yes |
| 5 | PUSH | 4 | Yes (shove, effort) | Yes |
| 6 | CONVEX | 6 | Yes (curved outward) | Yes |
| 7 | OF | 2 | Yes (preposition) | Marginal (very short) |
| 8 | WE | 2 | Yes (pronoun) | Marginal (very short) |
| 9 | HIRPLED | 7 | Yes (Scottish: limped) | Yes (unusual but valid) |

### Assessment: Are the 9 Hidden Words Crossword Entries?

**MODERATE-HIGH PROBABILITY.** Here's why:

1. **All are real English words.** Even HIRPLED, while obscure, is a legitimate English word (Scottish/dialectal for "walked with a limp"). Mike Selinker would know and appreciate this word.

2. **Length distribution matches crossword needs.** We need entries of various lengths. These range from 2 to 8 letters, filling gaps in our known answer distribution.

3. **Structural parallel.** The hidden words in P9 are analogous to the intermediate words in P1 (H2O words), P3 (TV show clues), and P8 (pyramid words). Each puzzle generates intermediate data that becomes crossword fill.

4. **The 2-letter words (OF, WE) are viable.** Our P8 pyramid entries already include 2-letter words (OI, RA, ER, NO), so the crossword has 2-letter entries. OF and WE are common crossword fill.

5. **Thematic connection.** The puzzle title is "Anything You Can Fit in the Circle." Things that fit in circles: a ZIP code area, CHAIRS around a table, QUORUMS in a circle, FLAMINGO standing in a circle, etc. The crossword clues for these might reference circular/fitting themes.

### Potential Crossword Clues for P9 Words

| Word | Possible Crossword Clue | Length |
|------|------------------------|--------|
| ZIP | Speed, code prefix, or zilch | 3 |
| CHAIRS | Leads a meeting, or furniture set | 6 |
| QUORUMS | Minimum attendances for votes | 7 |
| FLAMINGO | Pink wading bird | 8 |
| PUSH | Shove, or marketing campaign | 4 |
| CONVEX | Curved outward, like a dome | 6 |
| OF | Belonging to (preposition) | 2 |
| WE | First person plural pronoun | 2 |
| HIRPLED | Limped (Scottish) | 7 |

### Crossword Entries from P9: **9 hidden words (MODERATE-HIGH confidence)**

---

## Updated Grand Total

### Previously Confirmed (71 entries)
| Source | Count |
|--------|-------|
| P1 (Wells / H2O words) | 13 |
| P3 (Beach / TV show clues) | 19 |
| P8 (Pyramids / pyramid words) | 39 |
| **Subtotal** | **71** |

### New Candidates from This Analysis
| Source | Count | Confidence |
|--------|-------|------------|
| P4 (Experiences / place names) | 21 | HIGH |
| P9 (Circle / hidden words) | 9 | MODERATE-HIGH |
| P5 (Pokemon / Pokemon names) | 18 | LOW |
| P2 (Sudoku) | 0 | N/A |
| P6 (Tents) | 0 | N/A |
| P7 (Dogs) | 0 | N/A |
| **Subtotal (high confidence)** | **30** | |
| **Subtotal (with P5)** | **48** | |

### Projected Totals
| Scenario | Variety Puzzle Entries | Remaining Gap | Filled By |
|----------|----------------------|---------------|-----------|
| Conservative (P4+P9 only) | 71 + 30 = **101** | 75 | Main video puzzles + P8 missing entries |
| With P5 Pokemon names | 71 + 48 = **119** | 57 | Main video puzzles + P8 missing entries |
| Maximum (all sources) | ~119 + P8 missing (~5) = **124** | 52 | Main video puzzles (vault, laser, monitor, etc.) |

### Known Gaps in P8
The A-pyramid and E-pyramid each have ~5 missing entries (8-11 letter words):
- A-pyramid: 8, 9, 10, 11 letter entries (4 missing)
- E-pyramid: 8-letter entry (1 missing)
- Total P8 gap: ~5 entries

If we recover those: 124 + 5 = **129 confirmed entries** (still 47 short of 176).

The remaining ~47 entries likely come from:
- Main video puzzles (vault door, laser grid, monitor room, bills, morse code, etc.)
- Hint drops (24hr/48hr hints expected)
- Influencer puzzles (11 influencer contributors)
- Possibly the "CONTRADICTION" (13 letters), "CASHTENT" (8 letters), "ACCRAGHANA" (10 letters) from video puzzles

---

## Length Distribution of ALL Potential Entries

| Length | P1 | P3 | P4 | P5 | P8 | P9 | Total | Notes |
|--------|----|----|----|----|----|----|-------|-------|
| 2 | | | | | 4 (OI,RA,ER,NO) | 2 (OF,WE) | 6 | |
| 3 | | | | | 4 (ION,RAD,ERA,EON) | 1 (ZIP) | 5 | |
| 4 | 1 (DHOW) | 1 (HAFT) | ? | | 4 (TONI,DORA,RACE,NOTE) | 1 (PUSH) | 7+ | |
| 5 | 3 (ACHOO,WHOOP,HOOCH) | 4 (ABASH,OPERA,ERASE,TRITE) | ? | | 4 (PINTO,ADORN,LECAR,TONER) | | 11+ | |
| 6 | 4 (SCHOOL,OHIOAN,HOODIE,HOOPLA) | 1 (MATTER) | ? | 5 (BALTOY,ARCEUS,TYRUNT,TOGEPI,CHATOT) | 3 (OPTION,ECLAIR,ORIENT) | 2 (CHAIRS,CONVEX) | 15+ | |
| 7 | 2 (TYPHOON,OHSHOOT) | 2 (HEARTED,MUSTERS) | ? | 5 (POIPOLE,WUGTRIO,OMANYTE,SILCOON,TAILLOW) | 4 (PORTION,ROTUNDA,CALIBER,INUTERO) | 2 (QUORUMS,HIRPLED) | 15+ | |
| 8 | 2 (HOODWINK,HULAHOOP) | 4 (SCENARIO,NEUROTIC,SCREENER,ABSOLUTE,TEAMSEAS) | ? | 1 (SOLGALEO) | 2 (POSITRON,ROUTINES) | 1 (FLAMINGO) | 10+ | |
| 9 | 1 (HOOVERDAM) | 5 (DITHERING,HOWITZERS,HIGHHEELS,ALLUSIONS,RESISTIVE) | ? | 3 (POOCHYENA,DRAGONAIR,CLOBBOPUS) | 3 (RATPOISON,CABRIOLET,OUTLINERS) | | 12+ | |
| 10 | | | ? | 2 (AERODACTYL,MISDREAVUS) | 2 (STAINPROOF,ORBICULATE,RESOLUTION) | | 4+ | |
| 11 | | | ? | 1 (IRONVALIANT) | 2 (OUTFORASPIN,CIRCLEABOUT,REVOLUTIONS) | | 3+ | |
| 12 | | | ? | 1 (BRAMBLEGHAST) | | | 1+ | |
| 13 | | 1 (INTRODUCTIONS) | ? | | | | 1+ | |

P4 place names will fill various length slots once identified.

---

## Priority Actions

1. **IDENTIFY P4 PLACE NAMES** (Critical)
   - Need high-resolution image analysis to separate colored vs white letter layers
   - OR community crowdsourcing of the 21 locations
   - These 21 entries would be our single biggest new source of crossword fill
   - Belt color key may help: which color pairs overlay to reveal clean letters

2. **CONFIRM P9 HIDDEN WORDS AS ENTRIES** (Important)
   - Test whether ZIP, CHAIRS, QUORUMS, FLAMINGO, PUSH, CONVEX, OF, WE, HIRPLED match any crossword entry lengths at known grid positions
   - Cross-reference with any available crossword grid mapping

3. **RECOVER P8 MISSING ENTRIES** (Important)
   - A-pyramid levels 8-11 (8, 9, 10, 11 letter anagrams of {A,D,N,O,R,T,U,+3 more letters})
   - E-pyramid level 8 (8-letter anagram containing E,R,A,C,L,I,B,?)
   - Community may have solved these but not shared

4. **EVALUATE P5 POKEMON** (Low Priority)
   - Check if any crossword entry lengths match Pokemon name lengths in ways that can't be filled by other known answers
   - If grid positions force Pokemon-length entries, they may be needed

5. **INVESTIGATE MAIN VIDEO PUZZLES** (Parallel)
   - The remaining ~47-75 entries must come from video puzzles
   - CONTRADICTION (13), CASHTENT (8), ACCRA (5) are known candidates
   - Laser grid, monitor room, clocks, crosswalk, influencer puzzles = more entries
