#!/usr/bin/env python3
"""
Deep dive into vault ring sequence and other number theories.
"""

print("=" * 60)
print("VAULT RING SEQUENCE DEEP ANALYSIS")
print("=" * 60)

vault_ring = [4,1,8,4,1,3,1,8,4,1,1,3,4,4,4,1,2,1,1,4,4,10,1,1,1,2,4,1,1,1,1,3,1,3,1,1,1,1,8,4,3,1,1,1,1,10]

print(f"Sequence: {vault_ring}")
print(f"Length: {len(vault_ring)}")
print(f"Sum: {sum(vault_ring)}")
print(f"Max: {max(vault_ring)}")
print(f"Distinct values: {sorted(set(vault_ring))}")
print()

# Theory 1: The values ARE the message (A1Z26)
print("--- Theory 1: Direct A1Z26 ---")
result = ''
for v in vault_ring:
    if 1 <= v <= 26:
        result += chr(64 + v)
    else:
        result += '?'
print(f"A1Z26: {result}")
print()

# Theory 2: Pairs of values
print("--- Theory 2: Pairs → letters ---")
pairs = [(vault_ring[i], vault_ring[i+1]) for i in range(0, len(vault_ring)-1, 2)]
print(f"Pairs: {pairs}")
# As two-digit numbers
pair_nums = [a*10 + b for a, b in pairs]
print(f"Two-digit numbers: {pair_nums}")
pair_a1z26 = ''
for n in pair_nums:
    if 1 <= n <= 26:
        pair_a1z26 += chr(64 + n)
    else:
        pair_a1z26 += '?'
print(f"A1Z26: {pair_a1z26}")
print()

# Theory 3: Index into alphabet/message
print("--- Theory 3: Cumulative positions ---")
cumulative = []
pos = 0
for v in vault_ring:
    pos += v
    cumulative.append(pos)
print(f"Cumulative: {cumulative}")
print()

# Theory 4: Base conversion
print("--- Theory 4: Treat as digits in various bases ---")
for base in [5, 8, 10, 11, 12, 16]:
    try:
        # Treat each value as a digit in this base
        total = 0
        valid = all(v < base for v in vault_ring)
        if valid:
            for v in vault_ring:
                total = total * base + v
            print(f"  Base {base}: {total}")
        else:
            print(f"  Base {base}: invalid (values exceed base)")
    except:
        pass
print()

# Theory 5: Group by specific sizes
print("--- Theory 5: Grouping ---")
# The sum is 127. What if we group to get 7 values summing to specific things?
# 127 / 7 ≈ 18.1
# Or: 127 in binary = 1111111 (7 bits, all 1s)
print(f"127 in binary: {bin(127)} = 1111111 (7 ones)")
print(f"127 in ASCII: '{chr(127)}' (DEL)")
print(f"127 = 2^7 - 1 = all 7 bits set")
print()

# Theory 6: Morse code? (short=1, long=4+?)
print("--- Theory 6: Morse-like encoding ---")
morse_map = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z'
}
# If 1 = dot, 4 = dash, 3 = letter gap, 8 = word gap, 10 = sentence gap?
print("If 1=dot, 4=dash, 3=letter-gap, 8=word-gap, 10=sentence-gap:")
morse_str = ''
current_letter = ''
message = ''
for v in vault_ring:
    if v == 1:
        current_letter += '.'
    elif v == 4:
        current_letter += '-'
    elif v == 3:
        # letter boundary
        if current_letter in morse_map:
            message += morse_map[current_letter]
        else:
            message += f'[{current_letter}]'
        current_letter = ''
    elif v == 8:
        # word boundary
        if current_letter in morse_map:
            message += morse_map[current_letter]
        else:
            message += f'[{current_letter}]'
        current_letter = ''
        message += ' '
    elif v == 10:
        if current_letter in morse_map:
            message += morse_map[current_letter]
        else:
            message += f'[{current_letter}]'
        current_letter = ''
        message += ' | '
    elif v == 2:
        current_letter += '..'  # double dot?
        # Or 2 could be something else
print(f"  Morse attempt: {message}")
print()

# Theory 7: Differences
print("--- Theory 7: Differences between consecutive values ---")
diffs = [vault_ring[i+1] - vault_ring[i] for i in range(len(vault_ring)-1)]
print(f"Diffs: {diffs}")
print()

# Theory 8: Split at 10s (10 might be a delimiter)
print("--- Theory 8: Split at 10s ---")
groups = []
current_group = []
for v in vault_ring:
    if v == 10:
        if current_group:
            groups.append(current_group)
        current_group = []
    else:
        current_group.append(v)
if current_group:
    groups.append(current_group)
print(f"Groups (split at 10): {groups}")
for i, g in enumerate(groups):
    print(f"  Group {i}: {g}, sum={sum(g)}, len={len(g)}")
print()

# Theory 9: As braille/binary blocks
print("--- Theory 9: Groups of 6 as braille cells ---")
# Each braille cell is 6 dots. 46 values / 6 ≈ 7.7 cells
for start in range(0, len(vault_ring) - 5, 6):
    block = vault_ring[start:start+6]
    # Interpret as binary: 1 if > threshold, 0 if <= threshold
    binary = ''.join('1' if v > 2 else '0' for v in block)
    val = int(binary, 2)
    if 32 <= val + 32 <= 126:
        print(f"  Block {block} → binary {binary} → val {val} → ASCII '{chr(val + 32) if val + 32 <= 126 else '?'}'")
print()

# Theory 10: What if the sequence indices into the 9-word sentence?
print("--- Theory 10: Index into 9-word sentence ---")
sentence = "EVERY CHALLENGE LEADS TOWARDS LOCATION NAME SOMEWHERE AROUND WORLD"
sentence_no_spaces = "EVERYCHALLENGELEADSTOWARDSLOCATIONNAMESOMEWHEREAROUNDWORLD"
print(f"Sentence (no spaces): {sentence_no_spaces}")
print(f"Length: {len(sentence_no_spaces)}")

# Use vault values as indices into the sentence
idx_result = ''
for v in vault_ring:
    if 0 <= v-1 < len(sentence_no_spaces):
        idx_result += sentence_no_spaces[v-1]
    else:
        idx_result += '?'
print(f"Index (1-based): {idx_result}")

# Cumulative index
cum_result = ''
pos = 0
for v in vault_ring:
    pos += v
    if 0 <= pos-1 < len(sentence_no_spaces):
        cum_result += sentence_no_spaces[pos-1]
    else:
        cum_result += '?'
print(f"Cumulative index: {cum_result}")
print()

# ============================================================
print("=" * 60)
print("LOST NUMBERS DEEP ANALYSIS")
print("=" * 60)

lost = [4, 8, 15, 16, 23, 42]
print(f"Lost numbers: {lost}")
print(f"Sum: {sum(lost)} = 108")
print()

# As entry numbers
print("--- As entry numbers ---")
# Entry positions:
entries = {
    4: ('D', 0, 3, 8, 'down'),
    8: ('A/D', 0, 9, '6/8', 'both'),
    15: ('D', 0, 18, 5, 'down'),
    16: ('D', 0, 19, 5, 'down'),
    23: ('A/D', 1, 8, '7/4', 'both'),
    42: ('A', 5, 0, 4, 'across'),
}
for num in lost:
    if num in entries:
        info = entries[num]
        print(f"  Entry {num}: {info}")

print()
print("--- As grid coordinates (row, col) ---")
# Pairs: (4,8), (15,16), (23,42)
pairs = [(lost[i], lost[i+1]) for i in range(0, len(lost), 2)]
for r, c in pairs:
    if r < 25 and c < 25:
        print(f"  ({r},{c}): valid grid cell")
    else:
        print(f"  ({r},{c}): INVALID (col {c} > 24)")
print()

# As (row,col) triples
print("--- As row,col alternating ---")
# 4=row, 8=col → (4,8), 15=row, 16=col → (15,16), 23=row, 42=col → invalid
print("  (4,8): row 4, col 8 - black cell (4,8) is not black... wait")
# Check: is (4,8) black?
black_cells = {
    (0,7),(0,8),(0,15),(0,16),(1,7),(1,15),(1,16),(2,16),
    (3,4),(3,10),(3,14),(3,20),(4,4),(4,5),(4,6),(4,11),(4,21),
    (5,4),(5,8),(5,13),(5,18),(5,19),(6,16),(6,23),(6,24),
    (7,7),(7,12),(7,17),(7,24),(8,3),(8,9),(8,14),(8,15),(8,20),
    (9,0),(9,1),(9,2),(9,9),(9,10),(10,0),(10,4),(10,8),(10,9),(10,16),(10,21),
    (11,5),(11,11),(11,17),(11,21),(12,6),(12,18),
    (13,3),(13,7),(13,13),(13,19),(14,3),(14,8),(14,15),(14,16),(14,20),(14,24),
    (15,14),(15,15),(15,22),(15,23),(15,24),(16,4),(16,9),(16,10),(16,15),(16,21),
    (17,0),(17,7),(17,12),(17,17),(18,0),(18,1),(18,8),
    (19,5),(19,6),(19,11),(19,16),(19,20),(20,3),(20,13),(20,18),(20,19),(20,20),
    (21,4),(21,10),(21,14),(21,20),(22,8),(23,8),(23,9),(23,17),
    (24,8),(24,9),(24,16),(24,17)
}

for r, c in pairs:
    if r < 25 and c < 25:
        is_black = (r, c) in black_cells
        print(f"  ({r},{c}): {'BLACK' if is_black else 'WHITE'}")

# ============================================================
print()
print("=" * 60)
print("JERSEY NUMBERS ANALYSIS")
print("=" * 60)

jerseys = [597, 482, 374, 990, 723, 240, 478, 531, 109, 237, 453, 499, 930]
print(f"Jersey numbers: {jerseys}")
print()

# As entry numbers
print("--- Last 2-3 digits as entry numbers ---")
for j in jerseys:
    last2 = j % 100
    last3 = j % 1000
    first1 = j // 100
    mid = (j // 10) % 10
    last1 = j % 10
    print(f"  {j}: digits={first1},{mid},{last1}  last2={last2}  sum_digits={first1+mid+last1}")

print()
print("--- Sum of all digits ---")
total_dsum = 0
for j in jerseys:
    dsum = sum(int(d) for d in str(j))
    total_dsum += dsum
print(f"Sum of all individual digits: {total_dsum}")

# First digits
print(f"First digits: {[j // 100 for j in jerseys]}")
print(f"  = {''.join(chr(64 + j // 100) for j in jerseys if 1 <= j // 100 <= 26)}")

# ============================================================
print()
print("=" * 60)
print("COUNTDOWN 7-5-3-1 ANALYSIS")
print("=" * 60)
countdown = [7, 5, 3, 1]
print(f"Countdown: {countdown}")
print(f"Sum: {sum(countdown)} = 16 = number of circled cells!")
print(f"Product: {7*5*3*1} = 105")
print()

# 16 = number of circled cells. Coincidence?
# Or: use these as step sizes to extract from somewhere?
print("--- Use as step sizes to extract from grid ---")
grid_text = "SUPERBOWLSTADIUM"  # just test with 167A
print(f"In '{grid_text}', every 7th, 5th, 3rd, 1st character:")
for step in countdown:
    chars = grid_text[::step]
    print(f"  Step {step}: {chars}")

# ============================================================
print()
print("=" * 60)
print("BELT CODE 3X771 ANALYSIS")
print("=" * 60)
print("Belt code: 3X771")
print("Red-highlighted: second 7")
print()
print("--- As entry reference ---")
print("  Entry 37, position 71? No entry 71...")
print("  Entry 3, position X=10?, 7,7,1? ")
print("  3*771 = 2313")
print("  3+7+7+1 = 18 = R in A1Z26")
print("  X in hex = 10, so 3(10)771? or 310771?")
print("  If X=multiply: 3×771 = 2313")
print("  If X=24 (A1Z26): 3,24,7,7,1 → C,X,G,G,A = CXGGA? No")
print()

# ============================================================
print()
print("=" * 60)
print("INSTAGRAM 'DON'T SAY 67' + ENTRY 67D")
print("=" * 60)
print()
print("67D pattern: F??AEOE?O")
print("Entry 67D is at (8,12) down 9 cells")
print("Contains circled cell at (10,12)")
print()
print("'Don't say 67' could mean:")
print("  1. Don't use entry 67's answer")
print("  2. The number 67 is a red herring")
print("  3. 67 = something specific in cipher")
print(f"  67 in A1Z26: 67 mod 26 = {67 % 26} = {chr(64 + 67 % 26)}")
print(f"  6+7 = 13 = M")
print(f"  6*7 = 42 (Lost number!)")
print()

# ============================================================
print()
print("=" * 60)
print("PHONE NUMBER 704-BEAST-23 ANALYSIS")
print("=" * 60)
print("704-232-7823 = 704-BEAST-23")
print()
print("What if we call/text this number? (Can't do that)")
print("But the digits: 7-0-4-2-3-2-7-8-2-3")
print(f"Sum: {7+0+4+2+3+2+7+8+2+3} = {7+0+4+2+3+2+7+8+2+3}")
print(f"As entry numbers: 70, 42, 32, 78, 23")
print()
print("Entry 70A: (8,21) len 4")
print("Entry 42A: (5,0) len 4")
print("Entry 32A: (3,15) len 5")
print("Entry 78D: (10,2) len 15 ← THEME ENTRY!")
print("Entry 23A: (1,8) len 7")
print()
print("Interesting: 78D is a 15-letter theme down entry!")
print("704-BEAST-23 → entries 70,42,32,78,23")
print("First letters of these entries would need to be found first")

print()
print("DONE!")
