# Crossword Brute-Force Strategy

## The Problem
- 21x21 crossword grid with 176 entries
- NO clue text — clues come from solving variety puzzles + video puzzles
- 167 Across (16 chars): "What this puzzle commemorates in eleven hidden words in the theme entries"
- 16 circled cells in grid → extract letters = FINAL CODE
- Staircase grid (bottom-right) has 11 rows for 11 hidden words

## What We Have (71+ Confirmed Answers)

### From Puzzle 1 (13 answers — H2O word clues):
ACHOO, TYPHOON, SCHOOL, HOODWINK, WHOOP, SHOO, HOOLIGAN, HOOCH, HOOPLA, BROOD, HOOT, VOODOO, HOORAY
(Lengths: 5,7,6,8,5,4,8,5,6,5,4,6,6)

### From Puzzle 3 (19 answers — TV show cleanup clues):
HAFT(4), DITHERING(9), HOWITZERS(9), SCENARIO(8), ABASH(5), NEUROTIC(8), HEARTED(7), HIGHHEELS(9), SCREENER(8), INTRODUCTIONS(13), MATTER(6), OPERA(5), ALLUSIONS(9), RESISTIVE(9), ABSOLUTE(8), ERASE(5), TEAMSEAS(8), TRITE(5), MUSTERS(7)

### From Puzzle 8 (39+ answers — pyramid words):
I-pyramid: ION(3), TONI(4), PINTO(5), OPTION(6), PORTION(7), POSITRON(8), RATPOISON(9), STAINPROOF(10), OUTFORASPIN(11)
A-pyramid: RAD(3), DORA(4), ADORN(5), AROUND(6), ROTUNDA(7), ?(8), CALIBRATE?(9), ?(10), CIRCLEABOUT?(11)
E-pyramid: ERA(3), RACE(4), LECAR(5)→CLEAR?, ECLAIR(6), CALIBER(7), CABRIOLET(9), ORBICULATE(10), ?(11)
O-pyramid: EON(3), NOTE(4), TONER(5), ORIENT(6), INUTERO(7), ROUTINES(8), OUTLINERS(9), RESOLUTION(10), REVOLUTIONS(11)

### Other Candidate Answers:
- CONTRADICTION (13 letters) — from YouTube puzzle, theme entry candidate!
- ACCRAGHANA (10 letters) — from vault door Scrabble cipher
- CASHTENT (8 letters) — from red-outlined bills
- WORLD (5 letters) — P9 answer, may appear in crossword

## Brute-Force Approaches

### Approach 1: Constraint Propagation (Most Promising)
1. Map all 176 entries → lengths from grid image
2. Filter our 71+ answers by length → assign candidate entries
3. Where entries cross, letters must match → eliminate impossible placements
4. With enough constraints, unique placements emerge
5. Known letters from placed answers constrain unknown entries

**Feasibility:** HIGH — standard crossword solving via constraint satisfaction
**Tool needed:** Python script with grid model

### Approach 2: 167 Across Direct Attack
- 167 Across = 16 characters
- "What this puzzle commemorates" = ?
- Strong candidates:
  - MRBEASTSUPERBOWL (16) ← top candidate
  - SUPERBOWLSUNDAYLX?
  - MRBEASTCHALLENGE (16)
  - Could be a phrase about his charitable work
- If we get ANY crossing letters from DOWN entries at 167's position, we can verify

### Approach 3: Theme Entry Identification
- Theme entries = longer entries (11-15 letters typically)
- 11 hidden words span across multiple theme entries
- Our long answers: INTRODUCTIONS(13), CIRCLEABOUT(11), OUTFORASPIN(11), REVOLUTIONS(11), CONTRADICTION(13), STAINPROOF(10), RESOLUTION(10), ORBICULATE(10)
- Look for hidden location names inside these: e.g., INTRODUCTIONS contains "TROD", CONTRADICTION contains "CONTRA" (Contra Costa?)
- MrBeast locations: Ghana, various US states, international locations

### Approach 4: Letter Frequency / Dictionary Attack
- Standard crossword answers follow English letter frequency
- Use crossing constraints + common crossword fill words
- Tools: could use a crossword database or word list

### Approach 5: Circled Cell Focus
- 16 circled cells → final code
- If we can identify which cells are circled (from PDF image)
- Even partial crossword fill could reveal enough circled letters
- Final code might be recognizable with just some letters

## Implementation Plan
1. Build grid model in Python (21x21 array)
2. Mark black/white cells from PDF
3. Number all entries with lengths
4. Place confirmed answers by length matching
5. Propagate letter constraints
6. Use word list for remaining entries
7. Focus on 167 Across and circled cells

## Key Insight: "6 FEET DOWN BY THE CROSS"
"The cross" = THE CROSSWORD?
"6 feet down" = go to 6 Down in the crossword?
"6 feet" = 6 squares below something?
This could be a direct crossword navigation instruction!

## Key Insight: "REVERSE YOUR STEPS" (Twitter cipher)
The elephant account says to advance, reverse your steps.
- Could mean reverse the 9-word sentence order
- Could mean read answers backwards
- Could relate to backwards license plate
- Or: reverse the solving direction (crossword → puzzles instead of puzzles → crossword)
