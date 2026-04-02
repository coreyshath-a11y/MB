# Brute-Force Location Matching Results
## Generated: Feb 12, 2026

## Methodology
- Tests every world location (363 cities, countries, regions) against every unplaced entry
- Uses known crossing letter constraints from confirmed placements
- Higher constraint match count = higher confidence

---

## KEY FINDINGS

### Confirmed Location Placements (Already Known)
| Entry | Pattern | Location | Constraints |
|-------|---------|----------|-------------|
| 50A hidden | pos 9-13 | DAKAR | 5/5 (all letters confirmed) |
| 114A hidden | pos 8-12 | DELHI | 5/5 (all letters confirmed) |
| 109A | TOLEDO | TOLEDO | Already placed |
| 110D | DENVER | DENVER | Already placed |
| 117A | REGINA | REGINA | Already placed |
| 151D | ACCRA | ACCRA | Already placed |

### Medium-High Confidence Matches (2+ constraint letters)
| Entry | Pattern | Location | Matches | Notes |
|-------|---------|----------|---------|-------|
| 117D | RE?? | RENO | 2 | Also could be REDO |
| 130D | ???L?S | NAPLES or DALLAS | 2 | Need more constraints |
| 152D | N?P?? | NEPAL | 2 | Strong fit |

### Medium Confidence (1 constraint match, notable)
| Entry | Pattern | Location(s) | Notes |
|-------|---------|-------------|-------|
| 11D | ??????A | 29 locations ending in A | Circled cell 1! |
| 23D | ???O | OSLO, DIVO, RENO, TOGO | 4-letter ending O |
| 26D | ??D?? | INDIA, SUDAN | D at pos 2 |
| 59A | O??? | OMAN, OSLO | Starts with O |
| 134A | N?????? | NEWYORK, NIGERIA, NAIROBI, NAMIBIA | 7-letter starting N |
| 141D | ?????T | KUWAIT, BEIRUT | 6-letter ending T |
| 152D | N?P?? | NEPAL | N and P match |
| 158A | ?C??? | ACCRA | But ACCRA already at 151D |
| 161A | H???? | HAITI, HANOI | 5-letter starting H |
| 165A | ??????C? | FLORENCE, DOMINICA | 8-letter with C at pos 6 |

### Theme Entries - Hidden Location Candidates (2+ matches)
| Theme | Position | Location | Constraints | Notes |
|-------|----------|----------|-------------|-------|
| 50A | 9-13 | DAKAR | 5 | CONFIRMED |
| 114A | 8-12 | DELHI | 5 | CONFIRMED |
| 73A | 5-10 | UGANDA | 2 | But was SUDAN weak at 1-5 |
| 73A | 5-10 | RWANDA | 2 | Alternative |
| 73A | 5-10 | LUANDA | 2 | Alternative |
| 73A | 5-10 | CANADA | 2 | Alternative |
| 73A | 5-10 | DUBLIN | 2 | Alternative |
| 73A | 5-10 | KUWAIT | 2 | Alternative |
| 73A | 5-10 | AUSTIN | 2 | Alternative |
| 73A | 5-10 | RUSSIA | 2 | Alternative |
| 73A | 3-7 | SEOUL | 2 | Alternative |
| 73A | 3-6 | PERU | 2 | Alternative |
| 138A | 0-7 | BORDEAUX | 2 | Only 8-letter with 2 matches |
| 138A | 4-10 | BERMUDA | 2 | E at pos 4 |
| 138A | 4-10 | GRENADA | 2 | E at pos 4 |
| 138A | 2-9 | ADELAIDE | 2 | E at pos 4 + other |

---

## CIRCLED CELL STATUS (Final Code Extraction)

| # | Cell | Letter | Entries | Notes |
|---|------|--------|---------|-------|
| 1 | (0,12) | ? | 8A, 11D | 11D = 7-letter ending A |
| 2 | (2,4) | ? | 25A, 5D | Theme entry 25A |
| 3 | (3,8) | ? | 30A, 23D | 23D = 4-letter ending O |
| 4 | (3,24) | ? | 34A, 21D | |
| 5 | (4,19) | ? | 38A, 16D | |
| 6 | (10,12) | ? | 80A, 67D | |
| 7 | (11,2) | ? | 83A, 78D | Theme 78D |
| 8 | (11,22) | ? | 91A, 19D | Theme 19D |
| 9 | (13,0) | ? | 99A, 83D | |
| 10 | (18,7) | ? | 136A, 137D | |
| 11 | (19,17) | ? | 146A, 140D | |
| 12 | (20,2) | ? | 148A, 78D | Theme 78D |
| 13 | (22,11) | P | 167A, 152D | From SUPERBOWLSTADIUM |
| 14 | (22,18) | S | 167A, 162D | From SUPERBOWLSTADIUM |
| 15 | (22,24) | M | 167A, 126D | From SUPERBOWLSTADIUM |
| 16 | (24,20) | ? | 176A, 170D | |

**Code so far: `????????????PSM?`** (3/16 known)

---

## ENTRIES THAT COULD BE LOCATIONS (by length)

### 3-letter entries (34 total, 18A + 16D)
Could match: GOA, UAE
Notable: 59A starts with O → OMAN (4 letters, too long)

### 4-letter entries (46 total)
Could match: MALI, OMAN, ADEN, CHAD, IRAN, IRAQ, CUBA, FIJI, GUAM, LAOS, MALI, PERU, TOGO, BALI, BERN, DOHA, LIMA, LOME, OSLO, SUVA, ROME, RENO, etc.
Notable: 23D (???O), 117D (RE??→RENO), 131D (???A)

### 5-letter entries (32 total)
Could match: DAKAR, DELHI, LAGOS, SUDAN, WALES, ACCRA, ARLES, BENIN, CHILE, CHINA, EGYPT, GHANA, HAITI, INDIA, JAPAN, KENYA, KOREA, NEPAL, NIGER, QATAR, SPAIN, SYRIA, TIBET, WALES
Notable: 152D (N?P??→NEPAL), 161A (H????→HAITI/HANOI)

### 6-letter entries (28 total)
Could match: TEHRAN, LONDON, MEXICO, CANADA, FRANCE, GREECE, ISRAEL, JORDAN, KUWAIT, PANAMA, POLAND, RUSSIA, SWEDEN, TURKEY, UGANDA, VIENNA
Notable: 130D (???L?S→NAPLES/DALLAS)

### 7-letter entries (16 total)
Could match: MOROCCO, FINLAND, IRELAND, NIGERIA, etc.
Notable: 134A (N??????→NAIROBI?), 11D (??????A)

### 8-letter entries
Notable: 165A (??????C?→FLORENCE/DOMINICA)

---

## NEXT STEPS
1. **Upload new crossword PDF** with hints → extract clue text for numbered entries
2. **Use clue text** to confirm which entries ARE locations
3. **Cross-reference with P4 cities** (21 decoded) and P1/P3 answer bank
4. **Propagate new answers** through crossing constraints to reveal more letters
