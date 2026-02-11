#!/usr/bin/env python3
"""
Follow-up analysis on the most interesting findings from the first pass.
"""
from collections import Counter

def load_dict(path="/home/user/MB/puzzle/words.txt"):
    words = set()
    with open(path) as f:
        for line in f:
            w = line.strip().lower()
            if w:
                words.add(w)
    return words

WORDS = load_dict()

def caesar(text, shift):
    return ''.join(chr((ord(c.upper()) - 65 + shift) % 26 + 65) if c.isalpha() else c for c in text)

def vigenere_decrypt(ct, key):
    result, ki = [], 0
    for c in ct.upper():
        if c.isalpha():
            result.append(chr((ord(c) - ord(key[ki % len(key)].upper())) % 26 + 65))
            ki += 1
        else:
            result.append(c)
    return ''.join(result)

small_sections = ["GI", "RT", "OEAKAP", "ACYP", "NE", "RPV", "AKA", "CNEO"]
full_columns = ["GIIHL", "RTRAKA", "OEAJAPCNEO", "ACYPRPVY", "NEANAA"]

print("=" * 80)
print("FOLLOW-UP ANALYSIS")
print("=" * 80)

# -----------------------------------------------------------------------
# 1. Deep dive: CACIQUE finding from Vigenere
# -----------------------------------------------------------------------
print("\n--- CACIQUE VIGENERE FINDING ---")
concat = ''.join(small_sections)
key = "MELANESIANS"
dec = vigenere_decrypt(concat, key)
print(f"Cipher: {concat}")
print(f"Key:    {''.join(key[i % len(key)] for i in range(len(concat)))}")
print(f"Plain:  {dec}")
print(f"CACIQUE found at positions 7-13")
print(f"This corresponds to sections: ", end="")
pos = 0
for i, s in enumerate(small_sections):
    end = pos + len(s)
    if pos <= 7 < end or pos <= 13 < end or (7 <= pos and end <= 13):
        print(f"section[{i}]='{s}' (pos {pos}-{end-1})", end=" ")
    pos = end
print()

# What if we apply the key per-section rather than continuously?
print(f"\n--- Vigenere per-section (key restarts each section) ---")
for key_name, key in [("MELANESIANS", "MELANESIANS"), ("AROUNDWORLD", "AROUNDWORLD")]:
    print(f"  Key: {key_name}")
    for s in small_sections:
        dec = vigenere_decrypt(s, key)
        dl = dec.lower()
        note = f" *** WORD ***" if dl in WORDS and len(dl) >= 3 else ""
        print(f"    '{s}' -> {dec}{note}")
    # full columns too
    for c in full_columns:
        dec = vigenere_decrypt(c, key)
        dl = dec.lower()
        note = f" *** WORD ***" if dl in WORDS and len(dl) >= 3 else ""
        print(f"    '{c}' -> {dec}{note}")
        # check for sub-words
        for start in range(len(dl)):
            for end in range(start+4, len(dl)+1):
                sub = dl[start:end]
                if sub in WORDS and len(sub) >= 4:
                    print(f"      substring: '{sub}'")

# -----------------------------------------------------------------------
# 2. Deep dive: GROAN from full column first letters
# -----------------------------------------------------------------------
print("\n--- GROAN - FULL COLUMN FIRST LETTERS ---")
print("Full columns and their first letters:")
for c in full_columns:
    print(f"  {c[0]} <- {c}")
print("Spells: GROAN")
print("This is a real English word.")

# What about full column LAST letters?
last_fc = ''.join(c[-1] for c in full_columns)
print(f"\nFull column last letters: {last_fc}")
print(f"Anagrams: ", end="")
tc = Counter(last_fc.lower())
for w in WORDS:
    if len(w) == len(last_fc) and Counter(w) == tc:
        print(w, end=" ")
print()

# What about second letters?
second_fc = ''.join(c[1] for c in full_columns)
print(f"Full column 2nd letters: {second_fc}")

# -----------------------------------------------------------------------
# 3. Deep dive: ACYP -> ROT24 -> YAWN
# -----------------------------------------------------------------------
print("\n--- ACYP ROT-24 = YAWN ---")
print("Applying ROT-24 (same as ROT -2) to each small section:")
for s in small_sections:
    dec = caesar(s, 24)
    dl = dec.lower()
    note = f" *** WORD ***" if dl in WORDS and len(dl) >= 3 else ""
    print(f"  '{s}' ROT-24 -> {dec}{note}")

print("\nApplying ROT-24 to each full column:")
for c in full_columns:
    dec = caesar(c, 24)
    dl = dec.lower()
    note = f" *** WORD ***" if dl in WORDS and len(dl) >= 3 else ""
    print(f"  '{c}' ROT-24 -> {dec}{note}")

# -----------------------------------------------------------------------
# 4. Check: does each column have its own shift?
# -----------------------------------------------------------------------
print("\n--- DIFFERENT SHIFT PER COLUMN ---")
print("Testing if each full column uses a different Caesar shift to produce a word:")
for c in full_columns:
    for shift in range(0, 26):
        dec = caesar(c, shift).lower()
        if dec in WORDS:
            print(f"  '{c}' ROT-{shift} -> {dec} *** FULL WORD ***")

# -----------------------------------------------------------------------
# 5. Check: use MELANESIANS letters as shift values per column
# -----------------------------------------------------------------------
print("\n--- USE MELANESIANS LETTERS AS PER-CHARACTER SHIFTS ---")
mel = "MELANESIANS"
mel_shifts = [ord(c) - 65 for c in mel]
print(f"MELANESIANS shift values: {mel_shifts}")

# Apply each MELANESIANS letter as a shift to corresponding position in columns
# First, try: each column gets shifted by the corresponding MELANESIANS letter
print("\nEach full column shifted by corresponding MELANESIANS letter:")
for i, c in enumerate(full_columns):
    if i < len(mel):
        shift = mel_shifts[i]
        dec = caesar(c, -shift)
        dl = dec.lower()
        note = f" *** WORD ***" if dl in WORDS and len(dl) >= 3 else ""
        print(f"  Column '{c}' shift by -{mel[i]}({shift}) -> {dec}{note}")
        # Check substrings
        for start in range(len(dl)):
            for end in range(start+4, len(dl)+1):
                sub = dl[start:end]
                if sub in WORDS and len(sub) >= 4:
                    print(f"    substring: '{sub}'")

# -----------------------------------------------------------------------
# 6. Per-letter shift using MELANESIANS (letter-by-letter across all columns)
# -----------------------------------------------------------------------
print("\n--- MELANESIANS LETTER-BY-LETTER SHIFT ACROSS ALL FULL COLUMNS ---")
all_col_letters = ''.join(full_columns)
print(f"All column letters: {all_col_letters} (len={len(all_col_letters)})")
key = "MELANESIANS"
# Forward shift
dec_fwd = ''
for i, c in enumerate(all_col_letters):
    shift = ord(key[i % len(key)]) - 65
    dec_fwd += chr((ord(c) - 65 + shift) % 26 + 65)
print(f"Forward Vigenere (add): {dec_fwd}")
dl = dec_fwd.lower()
for start in range(len(dl)):
    for end in range(start+5, min(start+15, len(dl)+1)):
        sub = dl[start:end]
        if sub in WORDS and len(sub) >= 5:
            print(f"  substring: '{sub}'")

# Backward shift
dec_bwd = vigenere_decrypt(all_col_letters, key)
print(f"Backward Vigenere (sub): {dec_bwd}")
dl = dec_bwd.lower()
for start in range(len(dl)):
    for end in range(start+5, min(start+15, len(dl)+1)):
        sub = dl[start:end]
        if sub in WORDS and len(sub) >= 5:
            print(f"  substring: '{sub}'")

# -----------------------------------------------------------------------
# 7. GIRT analysis
# -----------------------------------------------------------------------
print("\n--- GIRT (GI + RT) ---")
print("First two small sections GI + RT = GIRT")
print("GIRT is a real word (past tense of 'gird')")
print("Remaining sections after GIRT: OEAKAP, ACYP, NE, RPV, AKA, CNEO")

# Do remaining sections also pair up?
remaining = ["OEAKAP", "ACYP", "NE", "RPV", "AKA", "CNEO"]
print("\nConsecutive pairs of remaining sections:")
for i in range(0, len(remaining)-1, 2):
    pair = remaining[i] + remaining[i+1]
    pl = pair.lower()
    note = f" *** WORD ***" if pl in WORDS else ""
    print(f"  {remaining[i]} + {remaining[i+1]} = {pair}{note}")

# -----------------------------------------------------------------------
# 8. ROT shift per section using position number
# -----------------------------------------------------------------------
print("\n--- SHIFT EACH SECTION BY ITS POSITION (1-indexed) ---")
for i, s in enumerate(small_sections):
    dec = caesar(s, -(i+1))
    dl = dec.lower()
    note = f" *** WORD ***" if dl in WORDS and len(dl) >= 3 else ""
    print(f"  Section {i+1}: '{s}' ROT-{-(i+1)%26} -> {dec}{note}")

print("\n--- SHIFT EACH SECTION BY ITS POSITION (0-indexed) ---")
for i, s in enumerate(small_sections):
    dec = caesar(s, -i)
    dl = dec.lower()
    note = f" *** WORD ***" if dl in WORDS and len(dl) >= 3 else ""
    print(f"  Section {i}: '{s}' ROT-{-i%26} -> {dec}{note}")

# -----------------------------------------------------------------------
# 9. Take one letter from each section at various positions
# -----------------------------------------------------------------------
print("\n--- DIAGONAL READS (letter i from section i) ---")
diag = ''
for i, s in enumerate(small_sections):
    if i < len(s):
        diag += s[i]
print(f"Forward diagonal: {diag}")
da = []
for w in WORDS:
    if len(w) == len(diag) and Counter(w) == Counter(diag.lower()):
        da.append(w)
if da:
    print(f"  Anagrams: {da}")

diag2 = ''
for i, s in enumerate(small_sections):
    idx = len(s) - 1 - (i % len(s))
    diag2 += s[idx]
print(f"Reverse diagonal: {diag2}")

# -----------------------------------------------------------------------
# 10. Interleave the two staircase extractions
# -----------------------------------------------------------------------
print("\n--- INTERLEAVE MELANESIANS + AROUNDWORLD ---")
m = "MELANESIANS"
a = "AROUNDWORLD"
interleaved = ''.join(m[i] + a[i] for i in range(min(len(m), len(a))))
print(f"Interleaved: {interleaved}")
il = interleaved.lower()
for start in range(len(il)):
    for end in range(start+5, min(start+14, len(il)+1)):
        sub = il[start:end]
        if sub in WORDS and len(sub) >= 5:
            print(f"  substring: '{sub}'")

# XOR the two extractions
print("\nAdd MELANESIANS + AROUNDWORLD (mod 26):")
added = ''.join(chr((ord(m[i])-65 + ord(a[i])-65) % 26 + 65) for i in range(min(len(m), len(a))))
print(f"  Result: {added}")
al = added.lower()
if al in WORDS:
    print(f"  *** WORD ***")
for start in range(len(al)):
    for end in range(start+4, len(al)+1):
        sub = al[start:end]
        if sub in WORDS and len(sub) >= 4:
            print(f"  substring: '{sub}'")

# Subtract
print("\nSubtract MELANESIANS - AROUNDWORLD (mod 26):")
subbed = ''.join(chr((ord(m[i])-65 - (ord(a[i])-65)) % 26 + 65) for i in range(min(len(m), len(a))))
print(f"  Result: {subbed}")
sl = subbed.lower()
if sl in WORDS:
    print(f"  *** WORD ***")
for start in range(len(sl)):
    for end in range(start+4, len(sl)+1):
        sub = sl[start:end]
        if sub in WORDS and len(sub) >= 4:
            print(f"  substring: '{sub}'")

print("\nSubtract AROUNDWORLD - MELANESIANS (mod 26):")
subbed2 = ''.join(chr((ord(a[i])-65 - (ord(m[i])-65)) % 26 + 65) for i in range(min(len(m), len(a))))
print(f"  Result: {subbed2}")
sl2 = subbed2.lower()
if sl2 in WORDS:
    print(f"  *** WORD ***")
for start in range(len(sl2)):
    for end in range(start+4, len(sl2)+1):
        sub = sl2[start:end]
        if sub in WORDS and len(sub) >= 4:
            print(f"  substring: '{sub}'")

# -----------------------------------------------------------------------
# 11. Check CNEO specifically since it anagrams to ONCE/CONE
# -----------------------------------------------------------------------
print("\n--- CNEO ANALYSIS ---")
print("CNEO anagrams: ONCE, CONE, ECON")
print("Could be significant - 'ONCE' as a keyword?")

# -----------------------------------------------------------------------
# 12. Pattern: ACYP = YAWN (ROT24), what about using this shift on all?
# -----------------------------------------------------------------------
print("\n--- ALL SECTIONS WITH THEIR 'BEST' INDIVIDUAL SHIFTS ---")
# For each section, find if there's a shift making it a word
for s in small_sections:
    for shift in range(0, 26):
        dec = caesar(s, shift).lower()
        if dec in WORDS and len(dec) >= 3:
            print(f"  '{s}' ROT-{shift:2d} -> {dec}")

# -----------------------------------------------------------------------
# 13. Try reading columns in different orders
# -----------------------------------------------------------------------
print("\n--- REORDERING COLUMN FIRST LETTERS ---")
# GROAN already found. What about reordering to make other words?
# The five columns could be read in 5! = 120 orders
import itertools
col_firsts = [c[0] for c in full_columns]
for perm in itertools.permutations(range(5)):
    word = ''.join(col_firsts[i] for i in perm)
    wl = word.lower()
    if wl in WORDS:
        order = [str(i+1) for i in perm]
        print(f"  Order [{','.join(order)}]: {word} -- WORD")

# -----------------------------------------------------------------------
# 14. Column second letters and beyond
# -----------------------------------------------------------------------
print("\n--- COLUMN NTH LETTERS ---")
for n in range(max(len(c) for c in full_columns)):
    letters = ''
    for c in full_columns:
        if n < len(c):
            letters += c[n]
    print(f"  Position {n}: {letters}", end="")
    ll = letters.lower()
    if ll in WORDS and len(ll) >= 3:
        print(f" -- WORD!", end="")
    # Anagram
    anags = []
    tc = Counter(ll)
    for w in WORDS:
        if len(w) == len(ll) and len(w) >= 3 and Counter(w) == tc:
            anags.append(w)
    if anags:
        print(f" -- anagrams: {', '.join(anags[:10])}", end="")
    # Caesar
    for shift in range(1, 26):
        shifted = caesar(letters, shift).lower()
        if shifted in WORDS and len(shifted) >= 3:
            print(f" -- ROT-{shift}: {shifted}", end="")
    print()

# -----------------------------------------------------------------------
# 15. Test if sections encode coordinates (A1, B2 style)
# -----------------------------------------------------------------------
print("\n--- LETTER-NUMBER COORDINATE INTERPRETATION ---")
print("If letters are column coordinates (A-Y) and section index is row:")
for i, s in enumerate(small_sections):
    coords = [(c, i+1) for c in s]
    print(f"  Section {i+1} '{s}': {coords}")

# -----------------------------------------------------------------------
# 16. Check MELANESIANS as key for Beaufort cipher
# -----------------------------------------------------------------------
print("\n--- BEAUFORT CIPHER (key - ciphertext mod 26) ---")
key = "MELANESIANS"
for label, text in [("small_concat", ''.join(small_sections)), ("full_concat", ''.join(full_columns))]:
    result = ''
    for i, c in enumerate(text):
        k = ord(key[i % len(key)].upper()) - 65
        p = ord(c.upper()) - 65
        result += chr((k - p) % 26 + 65)
    print(f"  {label}: {result}")
    rl = result.lower()
    for start in range(len(rl)):
        for end in range(start+5, min(start+15, len(rl)+1)):
            sub = rl[start:end]
            if sub in WORDS and len(sub) >= 5:
                print(f"    substring: '{sub}'")

# -----------------------------------------------------------------------
# 17. Affine cipher with various a,b values
# -----------------------------------------------------------------------
print("\n--- AFFINE CIPHER (common values) ---")
from math import gcd
for a in [1,3,5,7,9,11,15,17,19,21,23,25]:
    if gcd(a, 26) != 1:
        continue
    # Find modular inverse of a
    a_inv = pow(a, -1, 26)
    for b in range(26):
        for s in small_sections:
            if len(s) < 3:
                continue
            dec = ''.join(chr((a_inv * (ord(c.upper())-65 - b)) % 26 + 65) for c in s)
            dl = dec.lower()
            if dl in WORDS and len(dl) >= 4:
                print(f"  a={a}, b={b}: '{s}' -> {dec} *** WORD ***")

print("\n" + "=" * 80)
print("FOLLOW-UP ANALYSIS COMPLETE")
print("=" * 80)
