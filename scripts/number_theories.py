#!/usr/bin/env python3
"""
MrBeast Million Dollar Puzzle Hunt - Number Theory Tester
Tests various number-based theories connecting video clues to the crossword grid.
"""

import itertools
import string

# ===========================================================================
# DATA DEFINITIONS
# ===========================================================================

# Lost numbers from vault door (from TV show Lost)
lost_numbers = [4, 8, 15, 16, 23, 42]  # sum = 108

# Belt code
belt_code = "3X771"

# Phone numbers
phone_704beast = "7042327823"  # 704-BEAST-23

# Jersey numbers from Super Bowl ad
jersey_numbers = [597, 482, 374, 990, 723, 240, 478, 531, 109, 237, 453, 499, 930]

# Instagram numbers (MrBeast's hint posts)
instagram_numbers = [73, 60, 309, 1, 67, 99, 20, 17, 12, 8]

# Key repeating numbers
key_numbers = [7, 14, 17, 27, 41, 75, 103, 108, 777]

# Countdown
countdown = [7, 5, 3, 1]  # sum = 16

# Vehicle plates
plates = ["JP1117", "BPE527", "BP6327"]

# Calendar dates as entry numbers
calendar_entries = [11, 22, 31, 33, 61, 71, 81, 86, 91, 115, 127]

# Vault ring sequence
vault_ring = [4,1,8,4,1,3,1,8,4,1,1,3,4,4,4,1,2,1,1,4,4,10,1,1,1,2,4,1,1,1,1,3,1,3,1,1,1,1,8,4,3,1,1,1,1,10]

# Tank number
tank_number = 6601

# ENDGAME phone keypad
endgame = 3634826

# GPS theory
gps_lat = 36.34826  # Nevada desert

# Camera code / Timecode
camera_code = "B002C004"
timecode = "4:11:44:18"

# Super Bowl date
super_bowl_date = "020826"

# ===========================================================================
# GRID DATA (from CROSSWORD_GRID_DIGITIZED.md)
# ===========================================================================

# All across entries: {entry_number: (row, col, length)}
across_entries = {
    1: (0, 0, 7), 8: (0, 9, 6), 14: (0, 17, 8),
    22: (1, 0, 7), 23: (1, 8, 7), 24: (1, 17, 8),
    25: (2, 0, 16), 28: (2, 17, 8),
    29: (3, 0, 4), 30: (3, 5, 5), 31: (3, 11, 3), 32: (3, 15, 5), 34: (3, 21, 4),
    35: (4, 0, 4), 36: (4, 7, 4), 38: (4, 12, 9), 41: (4, 22, 3),
    42: (5, 0, 4), 43: (5, 5, 3), 45: (5, 9, 4), 47: (5, 14, 4), 48: (5, 20, 5),
    50: (6, 0, 16), 54: (6, 17, 6),
    57: (7, 0, 7), 58: (7, 8, 4), 59: (7, 13, 4), 61: (7, 18, 6),
    63: (8, 0, 3), 64: (8, 4, 5), 66: (8, 10, 4), 68: (8, 16, 4), 70: (8, 21, 4),
    72: (9, 3, 6), 73: (9, 11, 14),
    77: (10, 1, 3), 79: (10, 5, 3), 80: (10, 10, 6), 81: (10, 17, 4), 82: (10, 22, 3),
    83: (11, 0, 5), 85: (11, 6, 5), 88: (11, 12, 5), 90: (11, 18, 3), 91: (11, 22, 3),
    92: (12, 0, 6), 94: (12, 7, 11), 97: (12, 19, 6),
    99: (13, 0, 3), 100: (13, 4, 3), 102: (13, 8, 5), 103: (13, 14, 5), 105: (13, 20, 5),
    106: (14, 0, 3), 107: (14, 4, 4), 109: (14, 9, 6), 111: (14, 17, 3), 113: (14, 21, 3),
    114: (15, 0, 14), 117: (15, 16, 6),
    119: (16, 0, 4), 120: (16, 5, 4), 121: (16, 11, 4), 123: (16, 16, 5), 124: (16, 22, 3),
    127: (17, 1, 6), 129: (17, 8, 4), 132: (17, 13, 4), 134: (17, 18, 7),
    136: (18, 2, 6), 138: (18, 9, 16),
    141: (19, 0, 5), 143: (19, 7, 4), 145: (19, 12, 4), 146: (19, 17, 3), 147: (19, 21, 4),
    148: (20, 0, 3), 149: (20, 4, 9), 153: (20, 14, 4), 155: (20, 21, 4),
    156: (21, 0, 4), 158: (21, 5, 5), 159: (21, 11, 3), 161: (21, 15, 5), 164: (21, 21, 4),
    165: (22, 0, 8), 167: (22, 9, 16),
    171: (23, 0, 8), 172: (23, 10, 7), 173: (23, 18, 7),
    174: (24, 0, 8), 175: (24, 10, 6), 176: (24, 18, 7),
}

# All down entries: {entry_number: (row, col, length)}
down_entries = {
    1: (0, 0, 9), 2: (0, 1, 9), 3: (0, 2, 9), 4: (0, 3, 8), 5: (0, 4, 3),
    6: (0, 5, 4), 7: (0, 6, 4), 8: (0, 9, 8), 9: (0, 10, 3), 10: (0, 11, 4),
    11: (0, 12, 7), 12: (0, 13, 5), 13: (0, 14, 3), 14: (0, 17, 7), 15: (0, 18, 5),
    16: (0, 19, 5), 17: (0, 20, 3), 18: (0, 21, 4), 19: (0, 22, 15), 20: (0, 23, 6),
    21: (0, 24, 6),
    23: (1, 8, 4), 26: (2, 7, 5), 27: (2, 15, 6), 33: (3, 16, 3),
    37: (4, 10, 5), 39: (4, 14, 4), 40: (4, 20, 4),
    43: (5, 5, 6), 44: (5, 6, 7), 46: (5, 11, 6), 49: (5, 21, 5),
    51: (6, 4, 4), 52: (6, 8, 4), 53: (6, 13, 7), 55: (6, 18, 6), 56: (6, 19, 7),
    60: (7, 16, 3), 62: (7, 23, 8),
    65: (8, 7, 5), 67: (8, 12, 9), 69: (8, 17, 3), 71: (8, 24, 6),
    72: (9, 3, 4), 74: (9, 14, 6), 75: (9, 15, 5), 76: (9, 20, 5),
    77: (10, 1, 8), 78: (10, 2, 15), 80: (10, 10, 6), 83: (11, 0, 6), 84: (11, 4, 5),
    86: (11, 8, 3), 87: (11, 9, 5), 89: (11, 16, 3), 93: (12, 5, 7),
    95: (12, 11, 7), 96: (12, 17, 5), 98: (12, 21, 4),
    101: (13, 6, 6), 104: (13, 18, 7), 108: (14, 7, 3), 110: (14, 13, 6),
    112: (14, 19, 6), 115: (15, 3, 5), 116: (15, 8, 3), 117: (15, 16, 4),
    118: (15, 20, 4), 122: (16, 14, 5), 124: (16, 22, 9), 125: (16, 23, 9),
    126: (16, 24, 9),
    128: (17, 4, 4), 130: (17, 9, 6), 131: (17, 10, 4), 133: (17, 15, 8),
    135: (17, 21, 8), 137: (18, 7, 7), 139: (18, 12, 7), 140: (18, 17, 5),
    141: (19, 0, 6), 142: (19, 1, 6), 144: (19, 8, 3),
    150: (20, 5, 5), 151: (20, 6, 5), 152: (20, 11, 5), 154: (20, 16, 4),
    157: (21, 3, 4), 160: (21, 13, 4), 162: (21, 18, 4), 163: (21, 19, 4),
    166: (22, 4, 3), 168: (22, 10, 3), 169: (22, 14, 3), 170: (22, 20, 3),
}

# Merge all entries for lookup
all_entries = {}
for num, (r, c, l) in across_entries.items():
    all_entries.setdefault(num, []).append(('A', r, c, l))
for num, (r, c, l) in down_entries.items():
    all_entries.setdefault(num, []).append(('D', r, c, l))

# Confirmed placements: {(entry_num, direction): answer}
confirmed = {
    (36, 'A'): 'DORA', (37, 'D'): 'ABASH', (53, 'D'): 'ROTUNDA',
    (58, 'A'): 'PUSH', (66, 'A'): 'HAFT', (86, 'D'): 'ZIP',
    (87, 'D'): 'TRITE', (88, 'A'): 'ADORN', (94, 'A'): 'CIRCLEABOUT',
    (96, 'D'): 'TONER', (102, 'A'): 'PINTO', (103, 'A'): 'ACHOO',
    (109, 'A'): 'TOLEDO', (110, 'D'): 'DENVER', (117, 'A'): 'REGINA',
    (121, 'A'): 'TONI', (123, 'A'): 'ERASE',
    (167, 'A'): 'SUPERBOWLSTADIUM', (149, 'A'): 'BEASTLAND',
}

# Build the grid from confirmed placements
grid = {}
for (num, direction), answer in confirmed.items():
    if direction == 'A':
        r, c, l = across_entries[num]
        for i, ch in enumerate(answer):
            grid[(r, c + i)] = ch
    else:
        r, c, l = down_entries[num]
        for i, ch in enumerate(answer):
            grid[(r + i, c)] = ch

# Theme entries
theme_entries_across = [25, 50, 73, 94, 114, 138, 167]
theme_entries_down = [19, 78]

# Circled cells: list of (row, col, entry_number_or_None)
circled_cells = [
    (0, 12, 11), (2, 4, None), (3, 8, None), (3, 24, None),
    (4, 19, None), (10, 12, None), (11, 2, None), (11, 22, 91),
    (13, 0, 99), (18, 7, 137), (19, 17, 146), (20, 2, None),
    (22, 11, None), (22, 18, None), (22, 24, None), (24, 20, None),
]

# Entry numbers that start at circled cells
circled_entry_numbers = [11, 91, 99, 137, 146]

# All valid entry numbers
all_entry_numbers = sorted(set(list(across_entries.keys()) + list(down_entries.keys())))


def a1z26(n):
    """Convert number 1-26 to letter A-Z."""
    if 1 <= n <= 26:
        return chr(64 + n)
    return '?'


def entry_info(num):
    """Get info about an entry number."""
    results = []
    if num in across_entries:
        r, c, l = across_entries[num]
        letter = grid.get((r, c), '?')
        results.append(f"  {num}A at ({r},{c}), length {l}, first letter: {letter}")
    if num in down_entries:
        r, c, l = down_entries[num]
        letter = grid.get((r, c), '?')
        results.append(f"  {num}D at ({r},{c}), length {l}, first letter: {letter}")
    if not results:
        results.append(f"  Entry {num} DOES NOT EXIST")
    return results


def get_first_letter(num):
    """Get the first letter of an entry (from grid)."""
    if num in across_entries:
        r, c, _ = across_entries[num]
        return grid.get((r, c), '?')
    if num in down_entries:
        r, c, _ = down_entries[num]
        return grid.get((r, c), '?')
    return '?'


def get_entry_word(num, direction='A'):
    """Get the full word of an entry from the grid (? for unknown cells)."""
    if direction == 'A' and num in across_entries:
        r, c, l = across_entries[num]
        return ''.join(grid.get((r, c+i), '?') for i in range(l))
    elif direction == 'D' and num in down_entries:
        r, c, l = down_entries[num]
        return ''.join(grid.get((r+i, c), '?') for i in range(l))
    return None


# ===========================================================================
print("=" * 80)
print("MRBEAST PUZZLE - NUMBER THEORY TESTER")
print("=" * 80)

# ===========================================================================
# T1: Lost Numbers as Entry Indices
# ===========================================================================
print("\n" + "=" * 80)
print("T1: LOST NUMBERS AS ENTRY INDICES")
print(f"Lost numbers: {lost_numbers} (sum = {sum(lost_numbers)})")
print("=" * 80)

first_letters_across = []
first_letters_down = []
lengths_across = []
lengths_down = []

for num in lost_numbers:
    print(f"\nEntry {num}:")
    for line in entry_info(num):
        print(line)
    if num in across_entries:
        r, c, l = across_entries[num]
        fl = grid.get((r, c), '?')
        first_letters_across.append(fl)
        lengths_across.append(l)
        word = get_entry_word(num, 'A')
        print(f"    Full word (A): {word}")
    if num in down_entries:
        r, c, l = down_entries[num]
        fl = grid.get((r, c), '?')
        first_letters_down.append(fl)
        lengths_down.append(l)
        word = get_entry_word(num, 'D')
        print(f"    Full word (D): {word}")

print(f"\nFirst letters (Across only): {''.join(first_letters_across)}")
print(f"First letters (Down only):   {''.join(first_letters_down)}")
print(f"First letters (all, Across pref): {''.join(first_letters_across)}")
print(f"Lengths (Across): {lengths_across} -> sum={sum(lengths_across)}")
print(f"Lengths (Down):   {lengths_down} -> sum={sum(lengths_down)}")

# Try interpreting lengths as A1Z26
print(f"\nLengths as A1Z26 (Across): {''.join(a1z26(l) for l in lengths_across)}")
print(f"Lengths as A1Z26 (Down):   {''.join(a1z26(l) for l in lengths_down)}")

# Sum = 108. Does 108 map to anything?
print(f"\nSum of lost numbers = 108")
print(f"  Entry 108: ", end="")
for line in entry_info(108):
    print(line)
print(f"  108 mod 26 = {108 % 26} = {a1z26(108 % 26)}")

# ===========================================================================
# T2: Jersey Numbers -> 3-digit codes
# ===========================================================================
print("\n" + "=" * 80)
print("T2: JERSEY NUMBERS AS 3-DIGIT CODES")
print(f"Jersey numbers: {jersey_numbers}")
print("=" * 80)

print("\n--- Interpretation 1: Jersey number = Entry number ---")
for j in jersey_numbers:
    if j in all_entries:
        print(f"  {j}: EXISTS as entry!")
        for line in entry_info(j):
            print(line)
    else:
        exists_close = [e for e in all_entry_numbers if abs(e - j) <= 2]
        if exists_close:
            print(f"  {j}: Not an entry, but close entries: {exists_close}")
        else:
            print(f"  {j}: Not an entry (way out of range 1-176)")

print("\n--- Interpretation 2: First digit = entry, last two = position ---")
for j in jersey_numbers:
    s = str(j)
    entry_num = int(s[0])
    pos = int(s[1:])
    info = f"  {j}: entry {entry_num}, position {pos}"
    if entry_num in all_entries:
        for d, r, c, l in all_entries.get(entry_num, []):
            if pos < l:
                if d == 'A':
                    letter = grid.get((r, c + pos), '?')
                else:
                    letter = grid.get((r + pos, c), '?')
                info += f" -> {entry_num}{d}[{pos}] = {letter}"
            else:
                info += f" -> {entry_num}{d} only has length {l}, pos {pos} out of range"
    print(info)

print("\n--- Interpretation 3: First two digits = entry, last = position ---")
for j in jersey_numbers:
    s = str(j)
    entry_num = int(s[:2])
    pos = int(s[2])
    info = f"  {j}: entry {entry_num}, position {pos}"
    if entry_num in all_entries:
        for d, r, c, l in all_entries.get(entry_num, []):
            if pos < l:
                if d == 'A':
                    letter = grid.get((r, c + pos), '?')
                else:
                    letter = grid.get((r + pos, c), '?')
                info += f" -> {entry_num}{d}[{pos}] = {letter}"
            else:
                info += f" -> {entry_num}{d} only has length {l}, pos {pos} out of range"
    else:
        info += f" -> entry {entry_num} NOT FOUND"
    print(info)

# Extract letters for interpretation 3
print("\n  Extracted letters (entry=first2, pos=last1, Across preferred):")
letters_j3 = []
for j in jersey_numbers:
    s = str(j)
    entry_num = int(s[:2])
    pos = int(s[2])
    letter = '?'
    if entry_num in across_entries:
        r, c, l = across_entries[entry_num]
        if pos < l:
            letter = grid.get((r, c + pos), '?')
    elif entry_num in down_entries:
        r, c, l = down_entries[entry_num]
        if pos < l:
            letter = grid.get((r + pos, c), '?')
    letters_j3.append(letter)
print(f"  Letters: {''.join(letters_j3)}")

print("\n--- Interpretation 4: Row-Col-something (RCC) ---")
for j in jersey_numbers:
    s = str(j)
    row, col_tens, col_ones = int(s[0]), int(s[1]), int(s[2])
    col = col_tens * 10 + col_ones
    # Also try: row from first two digits, col from last
    row2 = int(s[:2])
    col2 = int(s[2])
    info = f"  {j}: "
    if 0 <= row <= 24 and 0 <= col <= 24:
        letter = grid.get((row, col), '?')
        info += f"({row},{col})={letter}  "
    if 0 <= row2 <= 24 and 0 <= col2 <= 24:
        letter2 = grid.get((row2, col2), '?')
        info += f"({row2},{col2})={letter2}"
    print(info)

print("\n--- Interpretation 5: Sorted jersey numbers ---")
sorted_j = sorted(jersey_numbers)
print(f"  Sorted: {sorted_j}")
print(f"  First digits sorted: {''.join(str(j)[0] for j in sorted_j)}")
print(f"  Differences: {[sorted_j[i+1] - sorted_j[i] for i in range(len(sorted_j)-1)]}")

# Check which jerseys match valid entry numbers
print("\n--- Which jersey numbers are valid entry numbers? ---")
for j in jersey_numbers:
    if j in all_entries:
        print(f"  *** {j} IS a valid entry! ***")
        for line in entry_info(j):
            print("     " + line)

# ===========================================================================
# T3: Vault Ring as Run-Length Encoding
# ===========================================================================
print("\n" + "=" * 80)
print("T3: VAULT RING AS RUN-LENGTH ENCODING")
print(f"Vault ring: {vault_ring}")
print(f"Length of sequence: {len(vault_ring)}")
print(f"Sum of sequence: {sum(vault_ring)}")
print("=" * 80)

vr_sum = sum(vault_ring)
print(f"\nTotal cells encoded: {vr_sum}")
print(f"  Grid total cells: 625 (25x25)")
print(f"  Black cells: 100")
print(f"  White cells: 525")
print(f"  {vr_sum} == 100? {vr_sum == 100}")
print(f"  {vr_sum} == 525? {vr_sum == 525}")
print(f"  {vr_sum} == 625? {vr_sum == 625}")
print(f"  {vr_sum} == 176? {vr_sum == 176} (num entries)")
print(f"  {vr_sum} == 16? {vr_sum == 16} (circled cells)")

# Build binary string - alternating black/white
print("\n--- RLE Decoding (alternating black=1/white=0, starting with black) ---")
binary_bw = ""
for i, count in enumerate(vault_ring):
    if i % 2 == 0:  # even index = black
        binary_bw += "1" * count
    else:  # odd index = white
        binary_bw += "0" * count
print(f"  Binary length: {len(binary_bw)}")
print(f"  1-count: {binary_bw.count('1')}, 0-count: {binary_bw.count('0')}")
print(f"  First 80 bits: {binary_bw[:80]}")

print("\n--- RLE Decoding (alternating white=0/black=1, starting with white) ---")
binary_wb = ""
for i, count in enumerate(vault_ring):
    if i % 2 == 0:  # even index = white
        binary_wb += "0" * count
    else:  # odd index = black
        binary_wb += "1" * count
print(f"  Binary length: {len(binary_wb)}")
print(f"  1-count: {binary_wb.count('1')}, 0-count: {binary_wb.count('0')}")
print(f"  First 80 bits: {binary_wb[:80]}")

# Try decoding binary as ASCII (8-bit chunks)
for label, bs in [("Black-first", binary_bw), ("White-first", binary_wb)]:
    print(f"\n--- Binary -> ASCII ({label}) ---")
    chars = []
    for i in range(0, len(bs) - 7, 8):
        byte = bs[i:i+8]
        val = int(byte, 2)
        if 32 <= val <= 126:
            chars.append(chr(val))
        else:
            chars.append(f'[{val}]')
    print(f"  {''.join(chars)}")

# Try as 5-bit (A=1, B=2, ..., Z=26)
for label, bs in [("Black-first", binary_bw), ("White-first", binary_wb)]:
    print(f"\n--- Binary -> 5-bit A1Z26 ({label}) ---")
    chars = []
    for i in range(0, len(bs) - 4, 5):
        chunk = bs[i:i+5]
        val = int(chunk, 2)
        if 1 <= val <= 26:
            chars.append(chr(64 + val))
        elif val == 0:
            chars.append('_')
        else:
            chars.append(f'[{val}]')
    print(f"  {''.join(chars)}")

# Try the vault ring values themselves as letters (A1Z26)
print("\n--- Vault ring values as A1Z26 ---")
vr_letters = ''.join(a1z26(v) if 1 <= v <= 26 else f'[{v}]' for v in vault_ring)
print(f"  {vr_letters}")

# Try vault ring as pairs -> letters
print("\n--- Vault ring as digit pairs -> A1Z26 ---")
vr_str = ''.join(str(v) for v in vault_ring)
print(f"  Concatenated: {vr_str}")
pairs_letters = []
for i in range(0, len(vr_str) - 1, 2):
    val = int(vr_str[i:i+2])
    if 1 <= val <= 26:
        pairs_letters.append(chr(64 + val))
    else:
        pairs_letters.append(f'[{val}]')
print(f"  Pairs: {''.join(pairs_letters)}")

# Check if sum of vault ring encodes grid rows
print(f"\n--- Vault ring sum analysis ---")
print(f"  Sum = {vr_sum}")
print(f"  46 elements in sequence")
print(f"  Max value: {max(vault_ring)}, Min value: {min(vault_ring)}")
print(f"  Unique values: {sorted(set(vault_ring))}")
print(f"  Value frequencies: ", end="")
from collections import Counter
print(dict(Counter(vault_ring).most_common()))

# ===========================================================================
# T4: Instagram Numbers as Grid Coordinates / Entry Numbers
# ===========================================================================
print("\n" + "=" * 80)
print("T4: INSTAGRAM NUMBERS AS ENTRY NUMBERS")
print(f"Instagram numbers: {instagram_numbers}")
print("=" * 80)

print("\n--- As entry numbers (first letter extraction) ---")
insta_letters = []
for num in instagram_numbers:
    if num in all_entries:
        fl = get_first_letter(num)
        insta_letters.append(fl)
        print(f"  {num}: Entry exists, first letter = {fl}")
        for line in entry_info(num):
            print("     " + line)
    elif num > 176:
        print(f"  {num}: OUT OF RANGE (max entry = 176)")
        insta_letters.append('?')
    else:
        print(f"  {num}: NOT a valid entry number")
        insta_letters.append('?')

print(f"\nFirst letters: {''.join(insta_letters)}")

# Try full words
print("\n--- Full entry words from grid ---")
for num in instagram_numbers:
    if num in across_entries:
        word = get_entry_word(num, 'A')
        print(f"  {num}A: {word}")
    if num in down_entries:
        word = get_entry_word(num, 'D')
        print(f"  {num}D: {word}")

# Instagram numbers as row,col pairs (paired)
print("\n--- As row,col pairs (consecutive pairing) ---")
for i in range(0, len(instagram_numbers) - 1, 2):
    r, c = instagram_numbers[i], instagram_numbers[i+1]
    if 0 <= r <= 24 and 0 <= c <= 24:
        letter = grid.get((r, c), '?')
        print(f"  ({r},{c}) = {letter}")
    else:
        print(f"  ({r},{c}) = OUT OF BOUNDS")

# ===========================================================================
# T5: Calendar Entries Crossing Theme Entries
# ===========================================================================
print("\n" + "=" * 80)
print("T5: CALENDAR ENTRIES CROSSING THEME ENTRIES")
print(f"Calendar entries: {calendar_entries}")
print(f"Theme entries (across): {theme_entries_across}")
print("=" * 80)

# For each calendar entry, check if it crosses any theme entry
for cal in calendar_entries:
    print(f"\nCalendar entry {cal}:")

    # Get all directions for this entry
    for d, r, c, l in all_entries.get(cal, []):
        print(f"  {cal}{d} at ({r},{c}), length {l}")
        word = get_entry_word(cal, d)
        print(f"    Current fill: {word}")

        # Check crossing with theme entries
        for theme_num in theme_entries_across:
            tr, tc, tl = across_entries[theme_num]

            if d == 'D':
                # This is a down entry. It crosses an across entry if:
                # the down entry's column is within the across entry's column range,
                # AND the across entry's row is within the down entry's row range
                if tc <= c < tc + tl and tr >= r and tr < r + l:
                    theme_pos = c - tc  # position in theme entry
                    cal_pos = tr - r    # position in calendar entry
                    theme_letter = grid.get((tr, c), '?')
                    print(f"    ** CROSSES {theme_num}A at theme position {theme_pos}, "
                          f"calendar entry position {cal_pos}, letter = {theme_letter}")
            elif d == 'A':
                # This is an across entry. It crosses theme down entries (19D, 78D)
                # But let's check if they share a row
                if r == tr:
                    # Same row - overlapping columns?
                    overlap_start = max(c, tc)
                    overlap_end = min(c + l, tc + tl)
                    if overlap_start < overlap_end:
                        print(f"    ** OVERLAPS with {theme_num}A on row {r}, "
                              f"cols {overlap_start}-{overlap_end-1}")

        # Also check against down theme entries
        for theme_num in theme_entries_down:
            tr, tc, tl = down_entries[theme_num]
            if d == 'A':
                # Across entry crosses down theme entry
                if r >= tr and r < tr + tl and tc >= c and tc < c + l:
                    theme_pos = r - tr  # position in theme down entry
                    cal_pos = tc - c    # position in calendar across entry
                    theme_letter = grid.get((r, tc), '?')
                    print(f"    ** CROSSES {theme_num}D at theme position {theme_pos}, "
                          f"calendar entry position {cal_pos}, letter = {theme_letter}")

# Summary table
print("\n--- Summary: Calendar Entry -> Theme Entry Crossings ---")
print(f"{'Cal Entry':<12}{'Direction':<6}{'Theme':<8}{'Theme Pos':<10}{'Cal Pos':<8}{'Letter':<8}")
print("-" * 60)
for cal in calendar_entries:
    for d, r, c, l in all_entries.get(cal, []):
        for theme_num in theme_entries_across:
            tr, tc, tl = across_entries[theme_num]
            if d == 'D' and tc <= c < tc + tl and tr >= r and tr < r + l:
                theme_pos = c - tc
                cal_pos = tr - r
                letter = grid.get((tr, c), '?')
                print(f"{cal:<12}{d:<6}{theme_num}A{'':<4}{theme_pos:<10}{cal_pos:<8}{letter:<8}")
        for theme_num in theme_entries_down:
            tr, tc, tl = down_entries[theme_num]
            if d == 'A' and r >= tr and r < tr + tl and tc >= c and tc < c + l:
                theme_pos = r - tr
                cal_pos = tc - c
                letter = grid.get((r, tc), '?')
                print(f"{cal:<12}{d:<6}{theme_num}D{'':<4}{theme_pos:<10}{cal_pos:<8}{letter:<8}")

# ===========================================================================
# T6: A1Z26 on Entry Numbers at Circled Cells
# ===========================================================================
print("\n" + "=" * 80)
print("T6: A1Z26 AND MODULAR ARITHMETIC ON CIRCLED CELL ENTRY NUMBERS")
print(f"Circled cells with entry numbers: {circled_entry_numbers}")
print("=" * 80)

# Basic A1Z26 (capped at 26)
print("\n--- Direct A1Z26 (entries that fit 1-26) ---")
for num in circled_entry_numbers:
    if 1 <= num <= 26:
        print(f"  {num} -> {a1z26(num)}")
    else:
        print(f"  {num} -> OUT OF RANGE")

# Mod 26
print("\n--- Mod 26 ---")
mod26_letters = []
for num in circled_entry_numbers:
    m = num % 26
    if m == 0:
        m = 26
    letter = a1z26(m)
    mod26_letters.append(letter)
    print(f"  {num} mod 26 = {num % 26} -> {letter}")
print(f"  Result: {''.join(mod26_letters)}")

# Mod 25 (grid size)
print("\n--- Mod 25 (grid size) ---")
mod25_letters = []
for num in circled_entry_numbers:
    m = num % 25
    if 1 <= m <= 26:
        mod25_letters.append(a1z26(m))
    else:
        mod25_letters.append('?')
    print(f"  {num} mod 25 = {num % 25} -> {mod25_letters[-1]}")
print(f"  Result: {''.join(mod25_letters)}")

# Digital root
print("\n--- Digital root ---")
for num in circled_entry_numbers:
    dr = num
    while dr > 9:
        dr = sum(int(d) for d in str(dr))
    print(f"  {num} -> digital root = {dr} -> {a1z26(dr)}")

# Sum of digits
print("\n--- Sum of digits ---")
sod_letters = []
for num in circled_entry_numbers:
    s = sum(int(d) for d in str(num))
    sod_letters.append(a1z26(s) if 1 <= s <= 26 else '?')
    print(f"  {num} -> digit sum = {s} -> {sod_letters[-1]}")
print(f"  Result: {''.join(sod_letters)}")

# Now look at ALL 16 circled cells and their current grid letters
print("\n--- Current letters at ALL 16 circled cells ---")
circled_letters = []
for r, c, entry in circled_cells:
    letter = grid.get((r, c), '?')
    circled_letters.append(letter)
    entry_str = f"entry {entry}" if entry else "no entry start"
    print(f"  ({r:2d},{c:2d}) = {letter}  [{entry_str}]")
print(f"\n  All circled letters: {''.join(circled_letters)}")
print(f"  Known letters only: {''.join(l for l in circled_letters if l != '?')}")

# ===========================================================================
# T7: "Don't say 67" Connection
# ===========================================================================
print("\n" + "=" * 80)
print("T7: 'DON'T SAY 67' CONNECTION")
print("=" * 80)

print("\nEntry 67D analysis:")
for line in entry_info(67):
    print(line)
word_67d = get_entry_word(67, 'D')
print(f"  Current fill: {word_67d}")

# 67D is at (8,12), length 9, going down to (16,12)
r67, c67, l67 = down_entries[67]
print(f"\n  67D spans rows {r67} to {r67 + l67 - 1} at col {c67}")
print(f"  Known letters by position:")
for i in range(l67):
    letter = grid.get((r67 + i, c67), '?')
    print(f"    pos {i}: row {r67+i}, col {c67} = {letter}")

# What confirmed entries cross 67D?
print(f"\n  Entries crossing 67D:")
for num, (r, c, l) in across_entries.items():
    if c <= c67 < c + l and r67 <= r < r67 + l67:
        pos_in_across = c67 - c
        pos_in_67d = r - r67
        letter = grid.get((r, c67), '?')
        placed = "PLACED" if (num, 'A') in confirmed else ""
        print(f"    {num}A crosses at 67D pos {pos_in_67d} / {num}A pos {pos_in_across} = {letter} {placed}")

# Known pattern for 67D
print(f"\n  Pattern: {word_67d}")
print(f"  Positions filled: {sum(1 for c in word_67d if c != '?')}/{l67}")

# Try to figure out what word this could be
# Pattern from solver results: F??AEOE?O (but let's recalculate)
print(f"\n  67D at (8,12) length 9:")
pattern_67 = []
for i in range(9):
    row = 8 + i
    letter = grid.get((row, 12), '?')
    pattern_67.append(letter)
    # Check what across entry provides this
    for num, (r, c, l) in across_entries.items():
        if r == row and c <= 12 < c + l:
            placed = confirmed.get((num, 'A'), None)
            if placed:
                pos = 12 - c
                print(f"    Row {row}: {letter} <- {num}A[{pos}] = {placed}")
                break
    else:
        print(f"    Row {row}: {letter}")
print(f"  Full pattern: {''.join(pattern_67)}")

# Connection to $673
print(f"\n  '$673 - the elephant ate $673'")
print(f"    67 + 3 = entry 70: ", end="")
for line in entry_info(70):
    print(line)
print(f"    6-7-3 as entries: 6D, 7D, 3D")
for n in [6, 7, 3]:
    for line in entry_info(n):
        print(f"    {line}")

# ===========================================================================
# T8: Tank Number 6601
# ===========================================================================
print("\n" + "=" * 80)
print("T8: TANK NUMBER 6601")
print("=" * 80)

print(f"\nEntry 66:")
for line in entry_info(66):
    print(line)
print(f"  66A = {get_entry_word(66, 'A')}")

print(f"\n6601 decompositions:")
print(f"  66 + 01: Entry 66 (HAFT) + position 1 -> {grid.get((8, 11), '?')}")
print(f"  6 + 601: Entry 6 exists, 601 doesn't")
print(f"  66 + 0 + 1: Entry 66, row 0, col 1? -> {grid.get((0, 1), '?')}")
print(f"  6-6-0-1 as row,col: ({6},{6})={grid.get((6, 6), '?')}, ({0},{1})={grid.get((0, 1), '?')}")
print(f"  Row 6, Col 6, then Row 0, Col 1 -> letters: {grid.get((6,6), '?')}{grid.get((0,1), '?')}")

# Grid coordinate interpretations
print(f"\n  (6,6) = {grid.get((6,6), '?')} (in 50A)")
print(f"  (6,0) = {grid.get((6,0), '?')} (start of 50A)")
print(f"  (6,1) = {grid.get((6,1), '?')}")

# 6601 as entry pairs
print(f"\n  As paired entries: (66, 01) -> entry 66 HAFT + entry 1:")
for line in entry_info(1):
    print(f"    {line}")

# 6601 in hex
print(f"\n  6601 decimal = {hex(6601)} hex")
print(f"  6601 in base36: ", end="")
def to_base36(n):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n == 0:
        return "0"
    result = ""
    while n:
        result = chars[n % 36] + result
        n //= 36
    return result
print(to_base36(6601))

# Connection to 67?
print(f"\n  6601 -> 66+01=67? -> Entry 67D (the 'don't say 67' entry)")
print(f"  This could be linking tank 6601 -> entry 67!")

# ===========================================================================
# T9: "17 STOP NOW HERE"
# ===========================================================================
print("\n" + "=" * 80)
print("T9: '17 STOP NOW HERE'")
print("=" * 80)

print(f"\nEntry 17:")
for line in entry_info(17):
    print(line)
print(f"  17D = {get_entry_word(17, 'D')}")

print(f"\nRow 17 entries:")
for num, (r, c, l) in across_entries.items():
    if r == 17:
        word = get_entry_word(num, 'A')
        print(f"  {num}A at ({r},{c}), length {l}: {word}")

print(f"\n  '17 STOP NOW HERE' -> 'STOP NOWHERE' or 'STOP NOW HERE'?")
print(f"  'NOWHERE' (7 letters) -> any 7-letter entries?")
print(f"  'STOPNOWHERE' (11 letters) -> 94A is the only 11-letter entry: CIRCLEABOUT")
print(f"  'STOP' (4 letters) - could be entry 17D (length 3, too short)")
print(f"  Column 17 entries:")
for num, (r, c, l) in down_entries.items():
    if c == 17:
        word = get_entry_word(num, 'D')
        print(f"  {num}D at ({r},{c}), length {l}: {word}")

# Number 17 appears EVERYWHERE
print(f"\n  Number 17 frequency analysis:")
print(f"  - Entry 17D at (0,20), length 3")
print(f"  - Vehicle plates: JP1117 (ends in 17)")
print(f"  - Instagram numbers: 17 appears at index 7")
print(f"  - '17 STOP NOW HERE' repeated in frames 491, 540")
print(f"  - Row 17 of grid: entries 127A, 129A, 132A, 134A")
print(f"  - Countdown sum: 7+5+3+1 = 16, but 17 = 16+1")

# ===========================================================================
# BONUS THEORIES
# ===========================================================================

print("\n" + "=" * 80)
print("BONUS: ADDITIONAL NUMBER ANALYSES")
print("=" * 80)

# B1: Phone number as entry sequence
print("\n--- B1: Phone 704-BEAST-23 as entries ---")
phone_digits = "7042327823"
print(f"  Phone: {phone_digits}")
# As single digits -> entries
print(f"  Single digits: {[int(d) for d in phone_digits]}")
# As pairs
pairs = [int(phone_digits[i:i+2]) for i in range(0, len(phone_digits), 2)]
print(f"  Digit pairs: {pairs}")
pair_letters = []
for p in pairs:
    fl = get_first_letter(p)
    pair_letters.append(fl)
    exists = "YES" if p in all_entries else "NO"
    print(f"    {p}: entry exists? {exists}, first letter = {fl}")
print(f"  First letters from pairs: {''.join(pair_letters)}")

# B2: ENDGAME number
print(f"\n--- B2: ENDGAME = 3634826 ---")
print(f"  As digit pairs: ", end="")
endgame_str = str(endgame)
for i in range(0, len(endgame_str) - 1, 2):
    pair = int(endgame_str[i:i+2])
    exists = "YES" if pair in all_entries else "NO"
    fl = get_first_letter(pair)
    print(f"{pair}({exists},{fl}) ", end="")
print()
print(f"  3-6-3-4-8-2-6 as entries:")
for d in [3, 6, 3, 4, 8, 2, 6]:
    for line in entry_info(d):
        print(f"    {line}")

# B3: Countdown -> 16 circled cells
print(f"\n--- B3: Countdown [7,5,3,1] sum=16 = number of circled cells ---")
print(f"  Sum = {sum(countdown)} = 16 circled cells? YES!")
print(f"  Could mean: read 7 letters, skip 5, read 3, skip 1? Or groups of circled cells?")
print(f"  Circled cells grouped 7-5-3-1:")
groups = []
idx = 0
for size in countdown:
    group = circled_cells[idx:idx+size]
    groups.append(group)
    letters = [grid.get((r, c), '?') for r, c, _ in group]
    print(f"    Group of {size}: {['({},{})={}'.format(r,c,grid.get((r,c),'?')) for r,c,_ in group]}")
    print(f"    Letters: {''.join(letters)}")
    idx += size

# B4: Belt code 3X771
print(f"\n--- B4: Belt code '3X771' ---")
print(f"  3, X=24(?), 7, 7, 1 as entries:")
for n in [3, 7, 7, 1]:
    for line in entry_info(n):
        print(f"    {line}")
print(f"  X = 24th letter. Entry 24:")
for line in entry_info(24):
    print(f"    {line}")
print(f"  37 as entry: ", end="")
for line in entry_info(37):
    print(line)
print(f"  37D = {get_entry_word(37, 'D')}")
print(f"  77 as entry: ", end="")
for line in entry_info(77):
    print(line)
print(f"  71 as entry: ", end="")
for line in entry_info(71):
    print(line)
print(f"  3X771 -> 3*771 = {3*771}")
print(f"  3+7+7+1 = {3+7+7+1}")

# B5: Plates analysis
print(f"\n--- B5: Vehicle plates ---")
for plate in plates:
    print(f"\n  Plate: {plate}")
    # Extract numbers
    nums = ''.join(c for c in plate if c.isdigit())
    lets = ''.join(c for c in plate if c.isalpha())
    print(f"    Letters: {lets}, Numbers: {nums}")
    if len(nums) >= 2:
        # Try as entry numbers
        for i in range(0, len(nums)-1, 2):
            pair = int(nums[i:i+2])
            if pair in all_entries:
                print(f"    Number pair {pair}: valid entry!")
                for line in entry_info(pair):
                    print(f"      {line}")
    # A1Z26 on letters
    a1z26_vals = [ord(c) - 64 for c in lets]
    print(f"    Letters as A1Z26: {lets} -> {a1z26_vals}")

# B6: All entry numbers at circled cells -> deeper analysis
print(f"\n--- B6: Circled cell positions as numbers ---")
print(f"  Row numbers of circled cells: {[r for r,c,_ in circled_cells]}")
print(f"  Col numbers of circled cells: {[c for r,c,_ in circled_cells]}")
rows_c = [r for r,c,_ in circled_cells]
cols_c = [c for r,c,_ in circled_cells]
print(f"  Row sum: {sum(rows_c)}, Col sum: {sum(cols_c)}")
print(f"  Row+Col pairs: {[(r,c) for r,c,_ in circled_cells]}")
print(f"  (Row*25+Col) = linear position: {[r*25+c for r,c,_ in circled_cells]}")
linear_pos = [r*25+c for r,c,_ in circled_cells]
print(f"  Linear positions: {linear_pos}")
print(f"  Linear pos mod 26: {[p%26 for p in linear_pos]} -> {''.join(a1z26(p%26) if p%26 > 0 else '?' for p in linear_pos)}")

# B7: Camera code B002C004
print(f"\n--- B7: Camera code B002C004 ---")
print(f"  B=2, C=3 in A1Z26. So: 2-002-3-004 = ?")
print(f"  Entry 2:")
for line in entry_info(2):
    print(f"    {line}")
print(f"  Entry 3:")
for line in entry_info(3):
    print(f"    {line}")
print(f"  (0,0) to (2,4) path? Letters: ", end="")
for r in range(3):
    for c in range(5):
        print(grid.get((r,c), '?'), end="")
print()

# B8: Timecode 4:11:44:18
print(f"\n--- B8: Timecode 4:11:44:18 ---")
tc_nums = [4, 11, 44, 18]
print(f"  Numbers: {tc_nums}")
for n in tc_nums:
    if n in all_entries:
        for line in entry_info(n):
            print(f"    {line}")
    else:
        print(f"    {n}: not a valid entry")
print(f"  First letters: {''.join(get_first_letter(n) for n in tc_nums)}")
print(f"  A1Z26: {''.join(a1z26(n) if 1<=n<=26 else f'[{n}]' for n in tc_nums)}")

# B9: Super Bowl date 020826
print(f"\n--- B9: Super Bowl date 020826 ---")
sb_pairs = [int(super_bowl_date[i:i+2]) for i in range(0, 6, 2)]
print(f"  As pairs: {sb_pairs}")
for p in sb_pairs:
    if p in all_entries:
        for line in entry_info(p):
            print(f"    {line}")
print(f"  As A1Z26: {''.join(a1z26(p) if 1<=p<=26 else f'[{p}]' for p in sb_pairs)}")

# B10: Cross-reference all number sets
print(f"\n--- B10: Numbers appearing in MULTIPLE sources ---")
all_number_sets = {
    'lost': set(lost_numbers),
    'jersey': set(jersey_numbers),
    'instagram': set(instagram_numbers),
    'calendar': set(calendar_entries),
    'key': set(key_numbers),
    'countdown': set(countdown),
}
all_nums_combined = set()
for s in all_number_sets.values():
    all_nums_combined |= s

for num in sorted(all_nums_combined):
    sources = [name for name, s in all_number_sets.items() if num in s]
    if len(sources) > 1:
        print(f"  {num:4d} appears in: {', '.join(sources)}")

# ===========================================================================
# FINAL SYNTHESIS
# ===========================================================================
print("\n" + "=" * 80)
print("SYNTHESIS: MOST PROMISING FINDINGS")
print("=" * 80)

print("""
KEY OBSERVATIONS:

1. JERSEY 109 = TOLEDO (entry 109A): Direct hit! Jersey number IS an entry number.
   Other jerseys that are valid entries: check above.

2. COUNTDOWN [7,5,3,1] sums to 16 = number of circled cells.
   Could define grouping: 7 cells, then 5, then 3, then 1.

3. VAULT RING sum = """ + str(vr_sum) + """ total cells.
   """ + ("MATCHES 100 (black cells)!" if vr_sum == 100 else
          "MATCHES 625 (full grid)!" if vr_sum == 625 else
          f"Does NOT match 100, 525, or 625. Value {vr_sum} is unusual.") + """

4. 67D is heavily referenced:
   - "Don't say 67" Instagram caption
   - Tank 6601 -> 66+01 = 67
   - "$673" -> entry 67 + position 3
   - 67D pattern from grid: """ + ''.join(pattern_67) + """

5. Calendar entries crossing theme entries: critical for hidden location extraction.
   Each calendar entry number crosses specific theme entries at specific positions.

6. Number 17 is repeated across plates (JP1117), Instagram, "17 STOP NOW HERE",
   and may reference entry 17D or row 17 or column 17.

7. INSTAGRAM numbers as entry numbers yield first letters that may spell something.
   Current: """ + ''.join(insta_letters) + """

8. LOST NUMBERS [4,8,15,16,23,42] as entries - first letters: """ +
    ''.join(first_letters_across) + """ (across) / """ + ''.join(first_letters_down) + """ (down)
""")

# Additional pattern check: do jersey numbers, when sorted, form an arithmetic sequence?
sorted_jerseys = sorted(jersey_numbers)
diffs = [sorted_jerseys[i+1] - sorted_jerseys[i] for i in range(len(sorted_jerseys)-1)]
print(f"Sorted jerseys: {sorted_jerseys}")
print(f"Jersey diffs: {diffs}")
print(f"Jersey digits sum: {[sum(int(d) for d in str(j)) for j in jersey_numbers]}")

# Check if any jersey number, when decomposed as entry+position, gives a
# confirmed letter match
print("\n--- Jersey validation: entry(first2)+pos(last1) vs confirmed grid ---")
hits = []
for j in jersey_numbers:
    s = str(j)
    entry_num = int(s[:2])
    pos = int(s[2])
    # Try across
    if entry_num in across_entries:
        r, c, l = across_entries[entry_num]
        if pos < l:
            letter = grid.get((r, c + pos), '?')
            if letter != '?':
                hits.append((j, f"{entry_num}A[{pos}]", letter))
                print(f"  {j} -> {entry_num}A pos {pos} = {letter} (CONFIRMED)")
    # Try down
    if entry_num in down_entries:
        r, c, l = down_entries[entry_num]
        if pos < l:
            letter = grid.get((r + pos, c), '?')
            if letter != '?':
                hits.append((j, f"{entry_num}D[{pos}]", letter))
                print(f"  {j} -> {entry_num}D pos {pos} = {letter} (CONFIRMED)")

if hits:
    print(f"\n  CONFIRMED HITS: {len(hits)}")
    print(f"  Letters: {''.join(h[2] for h in hits)}")
else:
    print("  No confirmed hits from jerseys yet (most grid cells unknown)")

print("\n" + "=" * 80)
print("END OF NUMBER THEORY ANALYSIS")
print("=" * 80)
