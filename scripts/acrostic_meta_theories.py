#!/usr/bin/env python3
"""
Test meta-puzzle patterns for the MrBeast Million Dollar Puzzle Hunt crossword.
Tests 8 different theories about hidden messages in entry numbers, lengths, etc.
"""

# =============================================================================
# DATA
# =============================================================================

ALL_ENTRY_NUMBERS = list(range(1, 177))  # 1..176

# Placed entries: number -> (direction, answer, row, col, length)
placed = {
    36: ('A', 'DORA', 4, 7, 4),
    37: ('D', 'ABASH', 4, 10, 5),
    53: ('D', 'ROTUNDA', 6, 13, 7),
    58: ('A', 'PUSH', 7, 8, 4),
    66: ('A', 'HAFT', 8, 10, 4),
    86: ('D', 'ZIP', 11, 8, 3),
    87: ('D', 'TRITE', 11, 9, 5),
    88: ('A', 'ADORN', 11, 12, 5),
    94: ('A', 'CIRCLEABOUT', 12, 7, 11),
    96: ('D', 'TONER', 12, 17, 5),
    102: ('A', 'PINTO', 13, 8, 5),
    103: ('A', 'ACHOO', 13, 14, 5),
    109: ('A', 'TOLEDO', 14, 9, 6),
    110: ('D', 'DENVER', 14, 13, 6),
    117: ('A', 'REGINA', 15, 16, 6),
    121: ('A', 'TONI', 16, 11, 4),
    123: ('A', 'ERASE', 16, 16, 5),
    149: ('A', 'BEASTLAND', 20, 4, 9),
    167: ('A', 'SUPERBOWLSTADIUM', 22, 9, 16),
}

# All confirmed answer first letters (from the user's list)
ALL_FIRST_LETTERS = list("ATSHOAHDSN MOARAETDRPHZTACTPATDRTE RELEAEORCPISICDRONEDT NIOPLHCROBS".replace(" ", ""))
# Clean version from user:
ALL_FIRST_LETTERS_RAW = "A,T,S,H,O,A,H,D,S,N,M,O,A,R,A,E,T,D,R,P,H,Z,T,A,C,T,P,A,T,D,R,T,E,R,E,L,E,A,E,O,R,C,P,I,S,I,C,D,R,O,N,E,D,T,N,I,O,P,L,H,C,R,O,B,S".split(",")

# Circled cell data: (row, col) -> (across_entry, down_entry)
CIRCLED_CELLS = [
    ((0, 12), (8, 11)),
    ((2, 4), (25, 5)),
    ((3, 8), (30, 8)),
    ((3, 24), (34, 21)),
    ((4, 19), (38, 16)),
    ((10, 12), (80, 67)),
    ((11, 2), (83, 78)),
    ((11, 22), (91, 124)),
    ((13, 0), (99, 83)),
    ((18, 7), (136, 137)),
    ((19, 17), (146, 140)),
    ((20, 2), (148, 78)),
    ((22, 11), (167, 95)),
    ((22, 18), (167, 104)),
    ((22, 24), (167, 126)),
    ((24, 20), (176, 170)),
]

# Unused answers (exist but can't fit in grid)
UNUSED_LENGTH_2 = ["RA", "ER", "OI", "NO"]
UNUSED_LENGTH_10 = ["TRADEUNION", "ORBICULATE", "STAINPROOF", "RESOLUTION", "WILMINGTON", "SACRAMENTO"]
UNUSED_LENGTH_13 = ["INTRODUCTIONS", "CONTRADICTION"]

# The 9-word sentence
SENTENCE_WORDS = ["EVERY", "CHALLENGE", "LEADS", "TOWARDS", "LOCATION", "NAME", "SOMEWHERE", "AROUND", "WORLD"]

# Comprehensive location list
LOCATIONS = set()

# Countries
COUNTRIES = [
    "AFGHANISTAN", "ALBANIA", "ALGERIA", "ANDORRA", "ANGOLA", "ANTIGUA", "ARGENTINA",
    "ARMENIA", "AUSTRALIA", "AUSTRIA", "AZERBAIJAN", "BAHAMAS", "BAHRAIN", "BANGLADESH",
    "BARBADOS", "BELARUS", "BELGIUM", "BELIZE", "BENIN", "BHUTAN", "BOLIVIA",
    "BOSNIA", "BOTSWANA", "BRAZIL", "BRUNEI", "BULGARIA", "BURKINA", "BURUNDI",
    "CAMBODIA", "CAMEROON", "CANADA", "CHAD", "CHILE", "CHINA", "COLOMBIA",
    "COMOROS", "CONGO", "COSTARICA", "CROATIA", "CUBA", "CYPRUS", "CZECH",
    "DENMARK", "DJIBOUTI", "DOMINICA", "ECUADOR", "EGYPT", "ELSALVADOR",
    "EQUATORIALGUINEA", "ERITREA", "ESTONIA", "ESWATINI", "ETHIOPIA", "FIJI",
    "FINLAND", "FRANCE", "GABON", "GAMBIA", "GEORGIA", "GERMANY", "GHANA",
    "GREECE", "GRENADA", "GUATEMALA", "GUINEA", "GUYANA", "HAITI", "HONDURAS",
    "HUNGARY", "ICELAND", "INDIA", "INDONESIA", "IRAN", "IRAQ", "IRELAND",
    "ISRAEL", "ITALY", "JAMAICA", "JAPAN", "JORDAN", "KAZAKHSTAN", "KENYA",
    "KIRIBATI", "KOSOVO", "KUWAIT", "KYRGYZSTAN", "LAOS", "LATVIA", "LEBANON",
    "LESOTHO", "LIBERIA", "LIBYA", "LIECHTENSTEIN", "LITHUANIA", "LUXEMBOURG",
    "MADAGASCAR", "MALAWI", "MALAYSIA", "MALDIVES", "MALI", "MALTA", "MARSHALL",
    "MAURITANIA", "MAURITIUS", "MEXICO", "MICRONESIA", "MOLDOVA", "MONACO",
    "MONGOLIA", "MONTENEGRO", "MOROCCO", "MOZAMBIQUE", "MYANMAR", "NAMIBIA",
    "NAURU", "NEPAL", "NETHERLANDS", "NEWZEALAND", "NICARAGUA", "NIGER",
    "NIGERIA", "NORTHKOREA", "NORTHMACEDONIA", "NORWAY", "OMAN", "PAKISTAN",
    "PALAU", "PALESTINE", "PANAMA", "PAPUANEWGUINEA", "PARAGUAY", "PERU",
    "PHILIPPINES", "POLAND", "PORTUGAL", "QATAR", "ROMANIA", "RUSSIA",
    "RWANDA", "SAMOA", "SANMARINO", "SAOTOME", "SAUDIARABIA", "SENEGAL",
    "SERBIA", "SEYCHELLES", "SIERRALEONE", "SINGAPORE", "SLOVAKIA", "SLOVENIA",
    "SOLOMONISLANDS", "SOMALIA", "SOUTHAFRICA", "SOUTHKOREA", "SOUTHSUDAN",
    "SPAIN", "SRILANKA", "SUDAN", "SURINAME", "SWEDEN", "SWITZERLAND",
    "SYRIA", "TAIWAN", "TAJIKISTAN", "TANZANIA", "THAILAND", "TOGO", "TONGA",
    "TRINIDAD", "TUNISIA", "TURKEY", "TURKMENISTAN", "TUVALU", "UGANDA",
    "UKRAINE", "UAE", "UK", "USA", "URUGUAY", "UZBEKISTAN", "VANUATU",
    "VATICAN", "VENEZUELA", "VIETNAM", "YEMEN", "ZAMBIA", "ZIMBABWE",
]

US_STATES = [
    "ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO",
    "CONNECTICUT", "DELAWARE", "FLORIDA", "GEORGIA", "HAWAII", "IDAHO",
    "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY", "LOUISIANA",
    "MAINE", "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA",
    "MISSISSIPPI", "MISSOURI", "MONTANA", "NEBRASKA", "NEVADA",
    "NEWHAMPSHIRE", "NEWJERSEY", "NEWMEXICO", "NEWYORK", "NORTHCAROLINA",
    "NORTHDAKOTA", "OHIO", "OKLAHOMA", "OREGON", "PENNSYLVANIA",
    "RHODEISLAND", "SOUTHCAROLINA", "SOUTHDAKOTA", "TENNESSEE", "TEXAS",
    "UTAH", "VERMONT", "VIRGINIA", "WASHINGTON", "WESTVIRGINIA",
    "WISCONSIN", "WYOMING",
]

WORLD_CAPITALS = [
    "KABUL", "TIRANA", "ALGIERS", "ANDORRALAVELLA", "LUANDA", "BUENOSAIRES",
    "YEREVAN", "CANBERRA", "VIENNA", "BAKU", "NASSAU", "MANAMA", "DHAKA",
    "BRIDGETOWN", "MINSK", "BRUSSELS", "BELMOPAN", "PORTONOVO", "THIMPHU",
    "LAPAZ", "SUCRE", "SARAJEVO", "GABORONE", "BRASILIA", "SOFIA",
    "OUAGADOUGOU", "GITEGA", "PHNOMPENH", "YAOUNDE", "OTTAWA", "PRAIA",
    "NDJAMENA", "SANTIAGO", "BEIJING", "BOGOTA", "MORONI", "BRAZZAVILLE",
    "KINSHASA", "SANJOSE", "ZAGREB", "HAVANA", "NICOSIA", "PRAGUE",
    "COPENHAGEN", "DJIBOUTI", "ROSEAU", "SANTODOMINGO", "QUITO", "CAIRO",
    "SANSALVADOR", "MALABO", "ASMARA", "TALLINN", "MBABANE", "ADDISABABA",
    "SUVA", "HELSINKI", "PARIS", "LIBREVILLE", "BANJUL", "TBILISI",
    "BERLIN", "ACCRA", "ATHENS", "GRENADA", "GUATEMALACITY", "CONAKRY",
    "BISSAU", "GEORGETOWN", "PORTAUPRINCE", "TEGUCIGALPA", "BUDAPEST",
    "REYKJAVIK", "NEWDELHI", "JAKARTA", "TEHRAN", "BAGHDAD", "DUBLIN",
    "JERUSALEM", "ROME", "KINGSTON", "TOKYO", "AMMAN", "ASTANA",
    "NAIROBI", "TARAWA", "PRISTINA", "KUWAITCITY", "BISHKEK", "VIENTIANE",
    "RIGA", "BEIRUT", "MASERU", "MONROVIA", "TRIPOLI", "VADUZ", "VILNIUS",
    "LUXEMBOURG", "ANTANANARIVO", "LILONGWE", "KUALALUMPUR", "MALE",
    "BAMAKO", "VALLETTA", "MAJURO", "NOUAKCHOTT", "PORTLOUIS", "MEXICOCITY",
    "PALIKIR", "CHISINAU", "MONACO", "ULAANBAATAR", "PODGORICA", "RABAT",
    "MAPUTO", "NAYPYIDAW", "WINDHOEK", "YAREN", "KATHMANDU", "AMSTERDAM",
    "WELLINGTON", "MANAGUA", "NIAMEY", "ABUJA", "PYONGYANG", "SKOPJE",
    "OSLO", "MUSCAT", "ISLAMABAD", "NGERULMUD", "PANAMACITY", "PORTMORESBY",
    "ASUNCION", "LIMA", "MANILA", "WARSAW", "LISBON", "DOHA", "BUCHAREST",
    "MOSCOW", "KIGALI", "APIA", "SAOTOME", "RIYADH", "DAKAR", "BELGRADE",
    "VICTORIA", "FREETOWN", "SINGAPORE", "BRATISLAVA", "LJUBLJANA",
    "HONIARA", "MOGADISHU", "PRETORIA", "SEOUL", "JUBA", "MADRID",
    "COLOMBO", "KHARTOUM", "PARAMARIBO", "STOCKHOLM", "BERN", "DAMASCUS",
    "TAIPEI", "DUSHANBE", "DODOMA", "BANGKOK", "LOME", "NUKUALOFA",
    "PORTOFSPAIN", "TUNIS", "ANKARA", "ASHGABAT", "FUNAFUTI", "KAMPALA",
    "KYIV", "ABUDHABI", "LONDON", "WASHINGTON", "MONTEVIDEO", "TASHKENT",
    "PORTVILA", "VATICANCITY", "CARACAS", "HANOI", "SANAA", "LUSAKA", "HARARE",
]

MAJOR_CITIES = [
    "NEWYORK", "LOSANGELES", "CHICAGO", "HOUSTON", "PHOENIX", "PHILADELPHIA",
    "SANANTONIO", "SANDIEGO", "DALLAS", "AUSTIN", "DENVER", "DETROIT",
    "MEMPHIS", "NASHVILLE", "PORTLAND", "LASVEGAS", "LOUISVILLE", "BALTIMORE",
    "MILWAUKEE", "ALBUQUERQUE", "TUCSON", "FRESNO", "SACRAMENTO", "MESA",
    "KANSASCITY", "ATLANTA", "OMAHA", "RALEIGH", "MIAMI", "CLEVELAND",
    "TAMPA", "TULSA", "OAKLAND", "MINNEAPOLIS", "PITTSBURGH", "CINCINNATI",
    "STLOUIS", "TOLEDO", "ORLANDO", "BUFFALO", "NEWARK", "RENO", "BOISE",
    "RICHMOND", "SPOKANE", "NORFOLK", "ANCHORAGE",
    # World major cities
    "MUMBAI", "DELHI", "SHANGHAI", "SAO", "PAULO", "ISTANBUL", "KARACHI",
    "LAGOS", "KOLKATA", "KINSHASA", "LIMA", "BOGOTA", "DHAKA", "CAIRO",
    "MEXICO", "LAHORE", "BANGALORE", "OSAKA", "CHENGDU", "WUHAN",
    "HANGZHOU", "SHENZHEN", "RIODEJANEIRO", "TIANJIN", "CHENNAI",
    "HYDERABAD", "NANJING", "DONGGUAN", "AHMEDABAD", "JOHANNESBURG",
    "TORONTO", "SYDNEY", "MELBOURNE", "PERTH", "BRISBANE", "AUCKLAND",
    "DUBAI", "DOHA", "CAPE", "TOWN", "CAPETOWN", "NAIROBI",
    "CASABLANCA", "ACCRA", "DURBAN", "LUANDA", "ADDISABABA",
    "DAKAR", "DAR", "ESSALAAM", "DARESSALAAM", "ABIDJAN", "KANO",
    "IBADAN", "KUMASI", "OUAGADOUGOU", "BAMAKO",
    # Additional well-known places
    "BALI", "CABO", "CANCUN", "FIJI", "GUAM", "MAUI", "OAHU",
    "TAHITI", "BERMUDA", "ARUBA", "TRINIDAD", "TOBAGO", "BARBADOS",
    "GRENADA", "MARTINIQUE", "CURACAO", "BONAIRE", "BAHAMAS",
    "ANTIGUA", "DOMINICA", "ADEN", "ALAN", "ALEPPO",
    "ASPEN", "BERN", "BONN", "CORK", "GRAZ", "HILO",
    "HULL", "KOBE", "LHASA", "LINZ", "LYON", "METZ", "NICE",
    "ORAN", "PERM", "PISA", "PUNE", "RENO", "SANA", "SIAN",
    "TULA", "WACO", "YORK", "ZURICH", "TURIN", "GENOA", "NAPLES",
    "MILAN", "FLORENCE", "VENICE", "VERONA", "PALERMO", "SEVILLE",
    "MALAGA", "BILBAO", "PORTO", "LISBON", "MUNICH", "HAMBURG",
    "COLOGNE", "DRESDEN", "LEIPZIG", "PRAGUE", "BUDAPEST", "KRAKOW",
    "GDANSK", "WARSAW", "VILNIUS", "RIGA", "TALLINN", "MINSK",
    "ODESSA", "TBILISI", "BAKU", "TASHKENT",
    "GOA", "STAN", "EAST", "WEST", "LAND", "DALE", "LODI",
    "NOME", "ERIE", "TROY", "GARY", "WACO", "MESA", "YUMA",
    "ELKO", "ENID", "LIMA", "AMES", "OREM",
    # Regions and territories
    "WALES", "SCOTLAND", "ENGLAND", "TIBET", "CRIMEA", "SIBERIA",
    "SAHARA", "SUDAN", "NIGER", "MALI", "CHAD", "TOGO", "BENIN",
    "GABON", "QATAR", "OMAN", "YEMEN", "SYRIA", "IRAQ", "IRAN",
    "LAOS", "NEPAL", "BURMA", "SAMOA", "GUAM", "PALAU", "NAURU",
    "TONGA", "NIUE",
]

# Build comprehensive set
for lst in [COUNTRIES, US_STATES, WORLD_CAPITALS, MAJOR_CITIES]:
    for loc in lst:
        LOCATIONS.add(loc)

# Also add some short locations that are commonly found as substrings
SHORT_LOCATIONS = [
    "US", "UK", "EU",
    "AL", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "IA", "ID",
    "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI", "MN", "MO",
    "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY", "OH",
    "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VT",
    "WA", "WI", "WV", "WY",
]
# Don't add 2-letter codes to main set to avoid noise; check them separately

print("=" * 80)
print("THEORY 1: Entry Numbers -> A1Z26 -> Message")
print("=" * 80)

def num_to_letter(n):
    """Convert number to letter: 1=A, 2=B, ..., 26=Z, 27=A, etc."""
    return chr((n - 1) % 26 + ord('A'))

message = ''.join(num_to_letter(n) for n in ALL_ENTRY_NUMBERS)
print(f"Full message ({len(message)} chars):")
print(message)
print()

# Look for words in running text
print("Checking for English words in the sequence...")
# Check sliding windows of length 3-10
common_words = set([
    "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HER",
    "WAS", "ONE", "OUR", "OUT", "DAY", "HAD", "HAS", "HIS", "HOW", "MAN",
    "NEW", "NOW", "OLD", "SEE", "WAY", "WHO", "BOY", "DID", "ITS", "LET",
    "SAY", "SHE", "TOO", "USE", "DAD", "MOM", "RUN", "GOT", "BIG", "END",
    "FAR", "GET", "GOD", "HIM", "HIT", "LOT", "PUT", "SET", "TOP", "TRY",
    "THAT", "WITH", "HAVE", "THIS", "WILL", "YOUR", "FROM", "THEY", "BEEN",
    "CALL", "COME", "EACH", "FIND", "GIVE", "HERE", "JUST", "KNOW", "LIKE",
    "LONG", "LOOK", "MAKE", "MANY", "MOST", "NAME", "OVER", "PART", "SAID",
    "SOME", "TAKE", "TELL", "THAN", "THEM", "THEN", "TIME", "VERY", "WANT",
    "WHAT", "WHEN", "WORD", "WORK", "YEAR", "ALSO", "BACK", "BEST", "BOTH",
    "CITY", "DOES", "DOWN", "EVEN", "FACT", "FIRST", "FIVE", "FOUR", "GOES",
    "GOOD", "HAND", "HEAD", "HELP", "HOME", "KEEP", "KIND", "LAST", "LEFT",
    "LIFE", "LINE", "LIVE", "LOVE", "MUCH", "MUST", "NEED", "NEXT", "ONLY",
    "OPEN", "PLAY", "REAL", "SAME", "SHOW", "SIDE", "SUCH", "SURE", "TURN",
    "USED", "WELL", "WENT", "ABOUT", "AFTER", "AGAIN", "BEING", "BELOW",
    "COULD", "EVERY", "FIRST", "FOUND", "GREAT", "HOUSE", "LARGE", "LEARN",
    "NEVER", "OTHER", "PLACE", "PLANT", "POINT", "RIGHT", "SHALL", "SMALL",
    "SOUND", "SPELL", "STILL", "STORY", "STUDY", "THEIR", "THERE", "THESE",
    "THING", "THINK", "THREE", "UNDER", "WATER", "WHERE", "WHICH", "WHILE",
    "WORLD", "WOULD", "WRITE", "BEAST", "PRIZE", "MONEY", "SOLVE", "CLUE",
    "PUZZLE", "ANSWER", "LOCATION", "HIDDEN", "SECRET",
])

found_words = []
for wlen in range(3, 11):
    for i in range(len(message) - wlen + 1):
        substr = message[i:i+wlen]
        if substr in common_words:
            found_words.append((i, substr))

print(f"Found {len(found_words)} common English words:")
for pos, word in found_words:
    print(f"  Position {pos}: {word} (from entries {pos+1}-{pos+wlen})")

# Also check if the mod-26 sequence has any repeating pattern
print("\nChecking for repeating patterns...")
# Since entries are 1-176, mod 26: the sequence is just ABCDEFGHIJ...Z repeated ~6.7 times
print("Note: Since entries are sequential 1-176, mod 26 just gives:")
print("  ABCDEFGHIJKLMNOPQRSTUVWXYZ repeated 6 times + ABCDEFGHIJKLMNOPQRST")
print("  This is trivially the alphabet cycling. No hidden message here.")

print()
print("=" * 80)
print("THEORY 2: Entry Lengths Encoding")
print("=" * 80)

# We need to know the length of each entry. We only know lengths for placed entries.
# For a full analysis, we'd need all 176 lengths. Let's work with what we have.
print("\nWe only have lengths for 19 placed entries out of 176.")
print("Placed entry lengths in entry-number order:")
placed_sorted = sorted(placed.items())
for num, (dirn, answer, row, col, length) in placed_sorted:
    print(f"  Entry {num:3d} ({dirn}): length {length} ({answer})")

placed_lengths = [placed[num][4] for num in sorted(placed.keys())]
print(f"\nLengths sequence: {placed_lengths}")

# As digits concatenated
digits_str = ''.join(str(l) for l in placed_lengths)
print(f"Concatenated digits: {digits_str}")

# As A1Z26
letters_from_lengths = ''.join(chr(l - 1 + ord('A')) for l in placed_lengths)
print(f"Lengths as A1Z26: {letters_from_lengths}")

# Check if this spells anything
print(f"  Reading: {letters_from_lengths}")
print("  (Incomplete - need all 176 entry lengths for full analysis)")

print()
print("=" * 80)
print("THEORY 3: Puzzle Source Index")
print("=" * 80)

print("The 9 puzzle words: EVERY, CHALLENGE, LEADS, TOWARDS, LOCATION, NAME, SOMEWHERE, AROUND, WORLD")
print("\nThese words come from puzzles P1-P9.")
print("Each puzzle provides multiple answers that go into the crossword.")
print("Without knowing which specific entries each puzzle's answers map to,")
print("we can analyze the sentence itself.")
print()

# Analyze the sentence as instructions
print("Sentence word lengths: ", [len(w) for w in SENTENCE_WORDS])
print("Sum of lengths: ", sum(len(w) for w in SENTENCE_WORDS))
print("Word count: ", len(SENTENCE_WORDS))
print()

# First letters
first_letters = ''.join(w[0] for w in SENTENCE_WORDS)
print(f"First letters of sentence: {first_letters}")
print(f"  = ECLTLNSAW")

# Last letters
last_letters = ''.join(w[-1] for w in SENTENCE_WORDS)
print(f"Last letters of sentence: {last_letters}")

# Word lengths as letters
wl_letters = ''.join(chr(len(w) - 1 + ord('A')) for w in SENTENCE_WORDS)
print(f"Word lengths as A1Z26: {wl_letters}")
print(f"  Lengths: {[len(w) for w in SENTENCE_WORDS]}")

print()
print("=" * 80)
print("THEORY 4: Unused Answer Lengths Analysis")
print("=" * 80)

print("\nLength 2 answers (0 grid slots of length 2):")
for w in UNUSED_LENGTH_2:
    print(f"  {w}")
print(f"  First letters: {''.join(w[0] for w in UNUSED_LENGTH_2)}")
print(f"  All letters: {''.join(UNUSED_LENGTH_2)}")
print(f"  Sorted: {''.join(sorted(''.join(UNUSED_LENGTH_2)))}")

print("\nLength 10 answers (0 grid slots of length 10):")
for w in UNUSED_LENGTH_10:
    print(f"  {w}")
print(f"  First letters: {''.join(w[0] for w in UNUSED_LENGTH_10)}")
fl10 = ''.join(w[0] for w in UNUSED_LENGTH_10)
print(f"  Anagram check of '{fl10}': ", end="")
from itertools import permutations
# Check if first letters anagram to something
fl10_sorted = ''.join(sorted(fl10))
print(f"sorted = {fl10_sorted}")

print("\nLength 13 answers (0 grid slots of length 13):")
for w in UNUSED_LENGTH_13:
    print(f"  {w}")
print(f"  First letters: {''.join(w[0] for w in UNUSED_LENGTH_13)}")

print("\nLength 12 answers (0 grid slots of length 12):")
print("  (None listed)")

print("\nCombined first letters of ALL unused answers:")
all_unused = UNUSED_LENGTH_2 + UNUSED_LENGTH_10 + UNUSED_LENGTH_13
all_unused_fl = ''.join(w[0] for w in all_unused)
print(f"  {all_unused_fl}")
print(f"  Sorted: {''.join(sorted(all_unused_fl))}")

print("\nCombined last letters of ALL unused answers:")
all_unused_ll = ''.join(w[-1] for w in all_unused)
print(f"  {all_unused_ll}")

print("\nAll unused answers concatenated first letters + last letters:")
print(f"  First: {all_unused_fl}")
print(f"  Last:  {all_unused_ll}")

print("\nLetter frequency in unused answers:")
from collections import Counter
all_unused_letters = ''.join(all_unused)
freq = Counter(all_unused_letters)
print(f"  Total letters: {len(all_unused_letters)}")
for letter, count in sorted(freq.items()):
    print(f"    {letter}: {count}")

print("\nPossible purpose theories:")
print("  1. These answers are RED HERRINGS (exist to confuse)")
print("  2. Their first/last letters spell something")
print("  3. They map to the staircase grid (different puzzle)")
print("  4. They are for a DIFFERENT extraction mechanism")
print(f"  5. Note: Length 2 concat = {''.join(UNUSED_LENGTH_2)} - does 'RAERONOI' or subsets mean anything?")
all2 = ''.join(UNUSED_LENGTH_2)
print(f"     'RAEROINO' rearranged... checking: ", end="")
# Check subsets
for perm in set(permutations(all2)):
    s = ''.join(perm)
    if s in ["ROANEIRO", "RIODEJAN"]:
        print(f"FOUND: {s}")
        break
else:
    print("No obvious anagram found for 8 letters")

# Check length-10 words for hidden locations
print("\n  Checking length-10 words for hidden location substrings:")
for w in UNUSED_LENGTH_10:
    for loc in LOCATIONS:
        if len(loc) >= 3 and loc in w:
            print(f"    {w} contains {loc}")

print()
print("=" * 80)
print("THEORY 5: Answer Anagrams (First Letters)")
print("=" * 80)

letters = ALL_FIRST_LETTERS_RAW
print(f"All {len(letters)} confirmed answer first letters:")
print(f"  {''.join(letters)}")
print()

freq = Counter(letters)
print("Frequency analysis:")
for letter, count in sorted(freq.items()):
    print(f"  {letter}: {count}")

print(f"\nTotal unique letters: {len(freq)}")
print(f"Total letters: {len(letters)}")

# Check if these could anagram to something meaningful
print("\nMost common letters:", freq.most_common(10))

# Look for common words that could be spelled
sorted_letters = ''.join(sorted(letters))
print(f"\nSorted: {sorted_letters}")

# Check specific meaningful phrases
def can_spell(word, available):
    """Check if word can be spelled with available letters."""
    avail = Counter(available)
    needed = Counter(word)
    for letter, count in needed.items():
        if avail[letter] < count:
            return False
    return True

test_phrases = [
    "MRBEAST", "SUPERBOWL", "CHALLENGE", "LOCATION", "TREASURE",
    "HIDDEN", "SECRET", "ANSWER", "CIRCLED", "STADIUM",
    "THOUSANDDOLLARS", "MILLIONDOLLARS", "PRIZEINSIDE",
    "THEANSWERIS", "LOOKHERE", "CONGRATULATIONS",
    "STARTEDON", "STARTHERE",
]

print("\nCan these be spelled from first letters?")
for phrase in test_phrases:
    result = can_spell(phrase, letters)
    if result:
        remaining = Counter(letters)
        for c in phrase:
            remaining[c] -= 1
        leftover = ''.join(sorted(c * n for c, n in remaining.items() if n > 0))
        print(f"  YES: {phrase} (leftover: {leftover})")
    else:
        needed = Counter(phrase)
        avail = Counter(letters)
        missing = {}
        for c, n in needed.items():
            if avail[c] < n:
                missing[c] = n - avail[c]
        print(f"  NO:  {phrase} (missing: {missing})")

print()
print("=" * 80)
print("THEORY 6: The 9-Word Sentence as Grid Instructions")
print("=" * 80)

print("\nSentence: EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD")
print()
print("Parsing as procedural instruction:")
print()
print("Interpretation 1: 'Every challenge leads towards [a] location name somewhere around [the] world'")
print("  -> The answer to each puzzle challenge points toward a location name hidden somewhere")
print("  -> The locations are hidden in theme entries (confirmed by 167A clue)")
print()
print("Interpretation 2: Word-by-word instructions:")
print("  EVERY     -> take every entry / every Nth")
print("  CHALLENGE -> the 9 puzzle challenges")
print("  LEADS     -> first letters ('leads' = 'heads')")
print("  TOWARDS   -> direction indicator (→ read forward)")
print("  LOCATION  -> find a location")
print("  NAME      -> specifically the name")
print("  SOMEWHERE -> it's hidden/embedded")
print("  AROUND    -> circular / surrounding")
print("  WORLD     -> global locations")
print()
print("Interpretation 3: Acrostic of the sentence:")
print(f"  First letters: {''.join(w[0] for w in SENTENCE_WORDS)}")
print(f"  = ECLTLNSAW")
print(f"  Anagram? Checking...")
ecltlnsaw = "ECLTLNSAW"
# Check meaningful anagrams
from itertools import permutations
# Too many permutations for 9 letters. Check known words instead.
nine_letter_words = ["NEWCASTLE", "LANCALETS", "ANCESTRAL"]
for w in nine_letter_words:
    if sorted(w) == sorted(ecltlnsaw):
        print(f"  ANAGRAM MATCH: {ecltlnsaw} -> {w}")
# Manual check
print(f"  Sorted: {''.join(sorted(ecltlnsaw))}")
print(f"  NEWCASTLE sorted: {''.join(sorted('NEWCASTLE'))}")
if sorted(ecltlnsaw) == sorted("NEWCASTLE"):
    print("  *** MATCH! ECLTLNSAW is an anagram of NEWCASTLE ***")
else:
    print(f"  Not NEWCASTLE (sorted: {''.join(sorted('NEWCASTLE'))})")

# Try other possibilities
print()
print("Interpretation 4: Letter positions in each word")
for i, word in enumerate(SENTENCE_WORDS):
    print(f"  P{i+1}: {word}")
    print(f"    Length: {len(word)}")
    print(f"    Middle letter: {word[len(word)//2]}")
    print(f"    Reversed: {word[::-1]}")

print()
print("Middle letters of sentence words:", ''.join(w[len(w)//2] for w in SENTENCE_WORDS))
print("Second letters:", ''.join(w[1] for w in SENTENCE_WORDS))
print("Last letters:", ''.join(w[-1] for w in SENTENCE_WORDS))

print()
print("=" * 80)
print("THEORY 7: Theme Entry Substring Analysis for Locations")
print("=" * 80)

theme_entries = {
    "CIRCLEABOUT": (94, 'A'),
    "BEASTLAND": (149, 'A'),
    "SUPERBOWLSTADIUM": (167, 'A'),
    # Other placed entries that might be thematic
    "TOLEDO": (109, 'A'),
    "DENVER": (110, 'D'),
    "REGINA": (117, 'A'),
}

# Add minimum length filter - only check locations of length >= 3
MIN_LOC_LEN = 3

print(f"\nSearching for location substrings (min length {MIN_LOC_LEN}) in theme entries:")
print()

for entry_word, (entry_num, dirn) in theme_entries.items():
    print(f"--- {entry_word} ({entry_num}{dirn}) ---")
    print(f"  Characters: {'-'.join(entry_word)}")
    found = []

    # Check all substrings against location list
    for start in range(len(entry_word)):
        for end in range(start + MIN_LOC_LEN, len(entry_word) + 1):
            substr = entry_word[start:end]
            if substr in LOCATIONS:
                found.append((start, end, substr))

    # Also check 2-letter state codes
    for start in range(len(entry_word) - 1):
        substr = entry_word[start:start+2]
        if substr in SHORT_LOCATIONS:
            found.append((start, start+2, f"{substr} (2-letter code)"))

    if found:
        # Sort by length descending for readability
        found.sort(key=lambda x: -(x[1] - x[0]))
        for start, end, loc in found:
            print(f"  [{start}:{end}] = {loc}")
    else:
        print("  No locations found")
    print()

# Deep dive into SUPERBOWLSTADIUM
print("=== DEEP DIVE: SUPERBOWLSTADIUM character-by-character ===")
word = "SUPERBOWLSTADIUM"
print(f"Positions: ", end="")
for i, c in enumerate(word):
    print(f"{i}={c} ", end="")
print()

print("\nAll substrings of length 3-8:")
for length in range(3, 9):
    row = []
    for start in range(len(word) - length + 1):
        substr = word[start:start+length]
        is_loc = substr in LOCATIONS
        marker = " ***" if is_loc else ""
        row.append(f"  [{start}:{start+length}] {substr}{marker}")
    if any("***" in r for r in row):
        print(f"\n  Length {length}:")
        for r in row:
            if "***" in r:
                print(r)
    else:
        # Print anyway for completeness
        pass

# Check specifically for well-known locations
print("\nSpecific location checks in SUPERBOWLSTADIUM:")
specific_checks = ["PERU", "BOWL", "STAD", "STADI", "STADIUM", "SUPER",
                   "OWL", "TAD", "USTA", "DUBAI", "AUSTIN", "BOSTON",
                   "DALLAS", "TULSA", "MESA", "LIMA", "OSLO", "ROME",
                   "LODI", "WADI", "IOWA", "ASIA", "BALI"]
for loc in specific_checks:
    if loc in word:
        idx = word.index(loc)
        print(f"  FOUND: {loc} at position {idx}-{idx+len(loc)-1}")

# Deep dive into CIRCLEABOUT
print("\n=== DEEP DIVE: CIRCLEABOUT character-by-character ===")
word = "CIRCLEABOUT"
print(f"Positions: ", end="")
for i, c in enumerate(word):
    print(f"{i}={c} ", end="")
print()

specific_checks_2 = ["CABO", "CLEO", "BOUT", "CLEA", "ABLE",
                     "CAIRO", "BOCA", "COLE", "EABC", "TOUR",
                     "CIRCLE", "ABOUT", "ROUT", "LOUT", "CLOUT",
                     "IRCA", "BEAU", "ARUBA", "CUBA", "RICO",
                     "ORCA", "ORAL", "LEAN", "ABEL", "ACRE",
                     "BOLE", "OLEA", "LACE", "RACE", "BOAR",
                     "BEAR", "EARL", "REAL", "CRAB", "ABOU",
                     "IRC", "LEA", "ABO", "OUT", "BOT", "OUR",
                     "IRE", "ERIE", "CIRE"]
for loc in ["ERIE", "CUBA", "IRAQ", "IRAN", "BALI", "LIMA", "OSLO",
            "NICE", "ROME", "CORK", "ADEN", "BERN", "BONN", "GOA",
            "CABO", "LODI", "TROY", "MESA", "YUMA", "ENID"]:
    if loc in word:
        idx = word.index(loc)
        print(f"  FOUND: {loc} at position {idx}-{idx+len(loc)-1}")

# Deep dive into BEASTLAND
print("\n=== DEEP DIVE: BEASTLAND character-by-character ===")
word = "BEASTLAND"
print(f"Positions: ", end="")
for i, c in enumerate(word):
    print(f"{i}={c} ", end="")
print()

for loc in LOCATIONS:
    if len(loc) >= 3 and loc in word:
        idx = word.index(loc)
        print(f"  FOUND: {loc} at position {idx}-{idx+len(loc)-1}")

# Check some specific ones
for loc in ["EAST", "LAND", "STAN", "BEAST", "ALAN", "ALAND",
            "ESTAL", "ELAND", "EASTLAND", "ASTANA", "BLAND"]:
    if loc in word:
        idx = word.index(loc)
        is_location = loc in LOCATIONS
        tag = "LOCATION" if is_location else "word"
        print(f"  Contains: {loc} at position {idx}-{idx+len(loc)-1} ({tag})")

print()
print("=" * 80)
print("THEORY 8: Circled Cell Entry Number Patterns")
print("=" * 80)

print("\nCircled cells and their across/down entry pairs:")
across_entries = []
down_entries = []
for (row, col), (a_entry, d_entry) in CIRCLED_CELLS:
    print(f"  ({row:2d},{col:2d}): {a_entry:3d}A, {d_entry:3d}D")
    across_entries.append(a_entry)
    down_entries.append(d_entry)

print(f"\nAcross entries at circled cells: {across_entries}")
print(f"Down entries at circled cells:   {down_entries}")

# Differences
diffs = [abs(a - d) for a, d in zip(across_entries, down_entries)]
print(f"\n|Across - Down| differences: {diffs}")
print(f"As A1Z26 (mod 26): {''.join(num_to_letter(d) if d > 0 else '?' for d in diffs)}")

# Check if diffs mod 26 spell something
diff_letters = []
for d in diffs:
    if d == 0:
        diff_letters.append('?')
    else:
        diff_letters.append(num_to_letter(d))
print(f"Diff letters: {''.join(diff_letters)}")

# Sums
sums = [a + d for a, d in zip(across_entries, down_entries)]
print(f"\nAcross + Down sums: {sums}")
print(f"Sums mod 26: {[s % 26 for s in sums]}")
print(f"Sums mod 26 as letters: {''.join(num_to_letter(s % 26) if s % 26 != 0 else 'Z' for s in sums)}")

# Products
products = [a * d for a, d in zip(across_entries, down_entries)]
print(f"\nAcross * Down products: {products}")

# XOR
xors = [a ^ d for a, d in zip(across_entries, down_entries)]
print(f"\nAcross XOR Down: {xors}")
print(f"XOR mod 26 as letters: {''.join(num_to_letter(x % 26) if x % 26 != 0 else 'Z' for x in xors)}")

# Just the across entries as letters
print(f"\nAcross entries mod 26 as letters: {''.join(num_to_letter(a % 26) if a % 26 != 0 else 'Z' for a in across_entries)}")
print(f"Down entries mod 26 as letters: {''.join(num_to_letter(d % 26) if d % 26 != 0 else 'Z' for d in down_entries)}")

# Min of pair
mins = [min(a, d) for a, d in zip(across_entries, down_entries)]
print(f"\nMin of each pair: {mins}")
print(f"Min mod 26 as letters: {''.join(num_to_letter(m % 26) if m % 26 != 0 else 'Z' for m in mins)}")

# Max of pair
maxs = [max(a, d) for a, d in zip(across_entries, down_entries)]
print(f"Max of each pair: {maxs}")
print(f"Max mod 26 as letters: {''.join(num_to_letter(m % 26) if m % 26 != 0 else 'Z' for m in maxs)}")

# The ACTUAL letters at circled cells from placed answers
print("\n\n--- Letters at circled cells from placed entries ---")
# Build a grid from placed entries
grid = {}
for num, (dirn, answer, row, col, length) in placed.items():
    for i, ch in enumerate(answer):
        if dirn == 'A':
            grid[(row, col + i)] = ch
        else:  # Down
            grid[(row + i, col)] = ch

print("Circled cell letters (from placed entries):")
circled_letters = []
for (row, col), (a_entry, d_entry) in CIRCLED_CELLS:
    letter = grid.get((row, col), '?')
    circled_letters.append(letter)
    print(f"  ({row:2d},{col:2d}): {letter}  (entries {a_entry}A/{d_entry}D)")

known_circled = ''.join(circled_letters)
print(f"\nCircled cell letters in order: {known_circled}")
print(f"Known letters only: {''.join(c for c in circled_letters if c != '?')}")

# Count knowns vs unknowns
n_known = sum(1 for c in circled_letters if c != '?')
print(f"Known: {n_known}/16, Unknown: {16 - n_known}/16")

# For SUPERBOWLSTADIUM (167A at row 22, col 9, length 16)
# Circled cells at (22,11), (22,18), (22,24)
print("\nCircled cells in SUPERBOWLSTADIUM (167A: row=22, col=9):")
for (row, col), (a_entry, d_entry) in CIRCLED_CELLS:
    if row == 22:
        offset = col - 9
        if 0 <= offset < 16:
            letter = "SUPERBOWLSTADIUM"[offset]
            print(f"  ({row},{col}): offset {offset} = '{letter}'")

# Row/col analysis of circled cells
print("\n--- Circled cell coordinate analysis ---")
rows = [r for (r,c), _ in CIRCLED_CELLS]
cols = [c for (r,c), _ in CIRCLED_CELLS]
print(f"Rows: {rows}")
print(f"Cols: {cols}")
print(f"Row differences: {[rows[i+1]-rows[i] for i in range(len(rows)-1)]}")
print(f"Col differences: {[cols[i+1]-cols[i] for i in range(len(cols)-1)]}")

print()
print("=" * 80)
print("SUMMARY OF FINDINGS")
print("=" * 80)

print("""
Theory 1 (Entry Numbers -> A1Z26): TRIVIAL - sequential numbers just give repeating alphabet.
         No hidden message possible since entries are numbered 1-176 sequentially.

Theory 2 (Entry Lengths): INCOMPLETE - need all 176 entry lengths.
         Placed entries give partial data only.

Theory 3 (Puzzle Source Index): Need mapping of which puzzle provides which entries.
         Sentence first letters = ECLTLNSAW.

Theory 4 (Unused Answers): These answers exist but have no grid slots.
         First letters of unused: check output above.
         May serve a different extraction purpose (staircase? code?).

Theory 5 (Answer First Letters): 65 letters available.
         Check output above for what phrases can be spelled.

Theory 6 (Sentence as Instructions): Multiple interpretations possible.
         Most literal: "locations hidden somewhere in entries"
         ECLTLNSAW anagram check: see above.

Theory 7 (Theme Entry Substrings): Check output above for found locations.
         BEASTLAND contains EAST, LAND, STAN.
         SUPERBOWLSTADIUM, CIRCLEABOUT need detailed review.

Theory 8 (Circled Cell Entries): Various numeric encodings tested.
         Check letter sequences above for recognizable patterns.
         Most circled cells are in UNKNOWN entries - only a few letters known.
""")
