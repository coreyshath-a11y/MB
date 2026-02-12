# Slackbot Query Guide — Puzzle Vault
## What to Ask the MrBeast Salesforce Slackbot

Use this when interacting with the Slackbot at mrbeast.salesforce.com.
Organized by priority and topic.

---

## PRIORITY 1: VERIFY WHAT WE KNOW

### Confirm the 9-Word Sentence
```
The 9-word sentence from the YouTube playlist puzzles is:
"EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD"
Is this correct?
```

### Confirm Individual Puzzle Answers
```
Puzzle 1 (100 Wells): EVERY
Puzzle 2 (600 Strangers): CHALLENGE
Puzzle 3 (Dirtiest Beach): LEADS
Puzzle 4 (Experiences): TOWARDS
Puzzle 5 (Pokemon Go): LOCATION
Puzzle 6 (Wilderness): NAME
Puzzle 7 (100 Dogs): SOMEWHERE
Puzzle 8 (Pyramids): AROUND
Puzzle 9 (Circle): WORLD
Can you confirm these answers?
```

---

## PRIORITY 2: ASK ABOUT THE CROSSWORD

### Crossword Structure
```
How many circled cells are in the crossword?
Are the circled letters read left-to-right, top-to-bottom for the final code?
```

```
Is 167 Across the only printed clue in the crossword?
How do we get the other clues?
```

```
Are the 11 hidden words in the theme entries all location/place names?
Are they countries, cities, or a mix?
```

```
Does the staircase grid in the bottom-right corner of the crossword
represent the 11 hidden location names?
```

### Crossword Answers
```
We have ~77 crossword answers from solving the variety puzzles.
Are all 176 crossword entries clued by the puzzle system,
or are some standard crossword fill?
```

```
From Puzzle 3, we got 19 crossword answers (HAFT, DITHERING, etc.)
plus coordinate pairs like WI(3,4). Do these coordinates tell us
where to place the answers in the grid?
```

---

## PRIORITY 3: ASK ABOUT UNSOLVED AD PUZZLES

### The Red Rubik's Cube
```
What does the all-red Rubik's cube represent?
Is it a puzzle that yields a crossword answer?
What cipher or code does it use?
```

### The Four Clocks
```
The four world clocks show times for Tokyo, London, Chicago, and New York.
What do the clock times encode? Numbers? Letters? Grid positions?
```

### Tank / QR Code
```
The rivets on the tank form a QR code when the two visible sides are overlaid.
What does the QR code link to?
The tank number reads 3634826-1 — what does this decode to?
```

### The Belt
```
The belt has colored X marks: red, blue, green, yellow, white.
Is this a semaphore code? Does it map to country flags?
How many colors total are there?
```

### Jersey Numbers
```
The 13 jersey numbers are: 597, 482, 374, 990, 723, 240, 478, 531, 109, 237, 453, 499, 930
What cipher decodes these? Phone keypad? A=1 substitution? Coordinate pairs?
```

### License Plate
```
What text is on the backwards license plate in the Super Bowl ad?
Does it spell a URL or IP address when reversed?
```

### Smoke Grenade
```
The smoke grenade says "{+1=?" and camera note says "Look +1 cube"
What does "+1" mean in the context of this puzzle?
Does it relate to the Rubik's cube?
```

### Calendar Dates
```
Mrs. Maybelle has circled dates: Jan 1, Feb 2, Mar 1, Mar 3
The pattern is 1, 2, 1, 3 — what does this encode?
Is it an extraction pattern for the crossword?
```

---

## PRIORITY 4: ASK ABOUT LOCATIONS

### Confirm Known Locations
```
We believe these are some of the 11 hidden location names:
- KENYA (from Video 1: Wells in Africa)
- GHANA/ACCRA (from vault door cipher)
- YELLOWKNIFE (from "find puzzle maker" numbers)
- SAN FRANCISCO (from 650 area code)
- EGYPT/GIZA (from Video 8: Pyramids)
- DUBAI (from Video 4: Experiences)
- DOMINICAN REPUBLIC (from Video 3: Beach)
- GREENVILLE NC (MrBeast's hometown)
Are any of these correct? Are we missing any?
```

### Location Format
```
Are the hidden locations single words (like KENYA, DUBAI)?
Or can they be multi-word (like SAN FRANCISCO)?
What is the longest hidden location name?
```

---

## PRIORITY 5: GENERAL STRATEGY

```
How many total puzzles are in Stage 1?
The hint says 50 puzzles + crossword = 51. Is that right?
```

```
We've solved the 9 variety puzzles and 6 ad puzzles.
What should we focus on next to make the most progress?
```

```
Is there a hidden website connected to the DOMAIN ID and SITE IP clues?
How do we find it?
```

```
Are there any puzzles we're completely missing that aren't from
the YouTube playlist, Super Bowl ad, or bank video?
```

```
Will more hints be released? On what schedule?
```

---

## PRIORITY 6: CREATE ACTIVE THEORIES IN PUZZLE VAULT

When creating new "Active Theories" in the Puzzle Vault tabs:

### Theory: Belt Cipher
Title: "Belt Color X Pattern"
Notes: Colors are Red, Blue, Green, Yellow, White in specific order.
Could map to country flags or semaphore. Need to identify all colors
and decode the sequence.

### Theory: Clock Code
Title: "Four World Clock Times"
Notes: Tokyo, London, Chicago, New York clocks show specific times.
Times may encode numbers (hour×10 + minute?) or positions in grid.

### Theory: QR Code Reconstruction
Title: "Tank QR Code Overlay"
Notes: Two halves of QR formed by rivets. Overlay analysis shows
they combine perfectly. Need to scan reconstructed QR.

### Theory: Jersey Number Decode
Title: "13 Jersey Numbers"
Notes: 597,482,374,990,723,240,478,531,109,237,453,499,930
Try: phone keypad, modular arithmetic, ASCII, coordinates

### Theory: Calendar Pattern
Title: "Mrs. Maybelle Calendar 1-2-1-3"
Notes: Circled dates Jan 1, Feb 2, Mar 1, Mar 3.
Pattern 1,2,1,3 could be extraction indices or ABAC structure.

### Theory: Crossword Location Search
Title: "11 Hidden Location Names"
Notes: Theme entries contain hidden consecutive letter sequences
spelling out locations where MrBeast filmed. Known candidates:
KENYA, GHANA, DUBAI, EGYPT, GREENVILLE, SAN FRANCISCO,
YELLOWKNIFE, DOMINICAN REPUBLIC.

---

## TIPS FOR SLACKBOT INTERACTION

1. **Ask specific questions** — vague questions get vague answers
2. **Reference specific puzzle numbers** — "Puzzle 3 from the YouTube playlist"
3. **Share what you know** — context helps get better responses
4. **Try submitting partial codes** — unlimited guesses are allowed
5. **Ask about cipher types** — "What kind of code does the belt use?"
6. **Ask for confirmation** — "Is EVERY the answer to Puzzle 1?"
7. **Create theories as tabs** — organize findings by puzzle/topic

---

*Guide compiled Feb 12, 2026 — Update as new information emerges*
