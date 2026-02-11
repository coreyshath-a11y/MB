#!/usr/bin/env python3
"""
Exhaustive analysis of column letter sequences from the MrBeast $1M staircase puzzle.
Tests: Caesar shifts, Atbash, anagrams, first/last letter patterns, letter-number,
reversed sections, cross-staircase patterns, and Vigenere decryption.
"""

import itertools
from collections import Counter

# ---------------------------------------------------------------------------
# Load dictionary
# ---------------------------------------------------------------------------
def load_dict(path="/home/user/MB/puzzle/words.txt"):
    words = set()
    with open(path) as f:
        for line in f:
            w = line.strip().lower()
            if w:
                words.add(w)
    return words

WORDS = load_dict()

# Also build a set of words length >= 3 for substring/anagram checks
WORDS3 = {w for w in WORDS if len(w) >= 3}
WORDS4 = {w for w in WORDS if len(w) >= 4}
WORDS5 = {w for w in WORDS if len(w) >= 5}

def is_word(s):
    return s.lower() in WORDS

def is_word_min3(s):
    return len(s) >= 3 and s.lower() in WORDS

def is_word_min4(s):
    return len(s) >= 4 and s.lower() in WORDS

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
# Small sections (broken by gaps between words)
small_sections = ["GI", "RT", "OEAKAP", "ACYP", "NE", "RPV", "AKA", "CNEO"]

# Full columns (ignoring gaps)
full_columns = ["GIIHL", "RTRAKA", "OEAJAPCNEO", "ACYPRPVY", "NEANAA"]

# Main extraction
main_extraction = "MELANESIANS"

# AROUNDWORLD staircase small sections
aw_sections = ["MHGSAA", "LASD", "EUA", "GEEA", "IN", "NH", "GDH", "TL", "EH"]

# All items to test individually
all_items = {
    "small_sections": small_sections,
    "full_columns": full_columns,
}

print("=" * 80)
print("COLUMN SEQUENCE ANALYSIS - MrBeast $1M Puzzle")
print("=" * 80)

# ---------------------------------------------------------------------------
# 1. Caesar / ROT shifts (1-25)
# ---------------------------------------------------------------------------
def caesar(text, shift):
    result = []
    for c in text.upper():
        if c.isalpha():
            result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

print("\n" + "=" * 80)
print("1. CAESAR / ROT SHIFTS (1-25)")
print("=" * 80)

for label, items in all_items.items():
    for item in items:
        hits = []
        for shift in range(1, 26):
            shifted = caesar(item, shift)
            sl = shifted.lower()
            # Check if whole thing is a word
            if sl in WORDS and len(sl) >= 3:
                hits.append((shift, shifted, "WHOLE WORD"))
            # Check substrings of length >= 4
            for start in range(len(sl)):
                for end in range(start + 4, len(sl) + 1):
                    sub = sl[start:end]
                    if sub in WORDS4:
                        hits.append((shift, shifted, f"substring '{sub}' at [{start}:{end}]"))
        if hits:
            print(f"\n  [{label}] '{item}':")
            seen = set()
            for shift, shifted, note in hits:
                key = (shift, note)
                if key not in seen:
                    seen.add(key)
                    print(f"    ROT-{shift:2d}: {shifted}  -- {note}")

# Also test concatenation of all small sections and all full columns
concat_small = ''.join(small_sections)
concat_full = ''.join(full_columns)

for label, text in [("all_small_concat", concat_small), ("all_full_concat", concat_full)]:
    hits = []
    for shift in range(1, 26):
        shifted = caesar(text, shift).lower()
        # Look for words of length >= 5 in the shifted text
        for start in range(len(shifted)):
            for end in range(start + 5, min(start + 16, len(shifted) + 1)):
                sub = shifted[start:end]
                if sub in WORDS5:
                    hits.append((shift, caesar(text, shift), f"substring '{sub}' at [{start}:{end}]"))
    if hits:
        print(f"\n  [{label}] '{text}':")
        seen = set()
        for shift, shifted, note in hits:
            key = (shift, note)
            if key not in seen:
                seen.add(key)
                print(f"    ROT-{shift:2d}: {shifted}  -- {note}")

# ---------------------------------------------------------------------------
# 2. Atbash cipher (A<->Z, B<->Y, etc.)
# ---------------------------------------------------------------------------
def atbash(text):
    result = []
    for c in text.upper():
        if c.isalpha():
            result.append(chr(ord('Z') - (ord(c) - ord('A'))))
        else:
            result.append(c)
    return ''.join(result)

print("\n" + "=" * 80)
print("2. ATBASH CIPHER")
print("=" * 80)

for label, items in all_items.items():
    for item in items:
        ab = atbash(item)
        abl = ab.lower()
        hits = []
        if abl in WORDS and len(abl) >= 3:
            hits.append(f"WHOLE WORD: {ab}")
        for start in range(len(abl)):
            for end in range(start + 4, len(abl) + 1):
                sub = abl[start:end]
                if sub in WORDS4:
                    hits.append(f"substring '{sub}' at [{start}:{end}]")
        if hits:
            print(f"\n  [{label}] '{item}' -> Atbash: {ab}")
            for h in hits:
                print(f"    {h}")

# Also test concatenations
for label, text in [("all_small_concat", concat_small), ("all_full_concat", concat_full)]:
    ab = atbash(text).lower()
    hits = []
    for start in range(len(ab)):
        for end in range(start + 5, min(start + 16, len(ab) + 1)):
            sub = ab[start:end]
            if sub in WORDS5:
                hits.append(f"substring '{sub}' at [{start}:{end}]")
    if hits:
        print(f"\n  [{label}] '{text}' -> Atbash: {atbash(text)}")
        for h in hits:
            print(f"    {h}")

# ---------------------------------------------------------------------------
# 3. Anagrams of each section
# ---------------------------------------------------------------------------
print("\n" + "=" * 80)
print("3. ANAGRAMS")
print("=" * 80)

def find_anagrams(text, wordset):
    """Find words in wordset that are anagrams of text."""
    text_lower = text.lower()
    text_sorted = ''.join(sorted(text_lower))
    results = []
    for w in wordset:
        if len(w) == len(text_lower) and ''.join(sorted(w)) == text_sorted:
            results.append(w)
    return results

# For short strings, find full anagrams
# For longer strings, also find partial anagrams (subsets)
for label, items in all_items.items():
    for item in items:
        anags = find_anagrams(item, WORDS3)
        if anags:
            print(f"\n  [{label}] '{item}' anagrams: {', '.join(sorted(anags))}")

# Also check if any subset of letters from longer sections form words
print("\n  --- Subset anagrams (words using subset of letters, len >= 4) ---")
for label, items in all_items.items():
    for item in items:
        if len(item) < 5:
            continue
        item_lower = item.lower()
        item_counter = Counter(item_lower)
        found = []
        for w in WORDS5:
            if len(w) > len(item):
                continue
            w_counter = Counter(w)
            if all(w_counter[c] <= item_counter[c] for c in w_counter):
                found.append(w)
        # Only show the longest / most interesting ones
        found.sort(key=len, reverse=True)
        if found:
            top = found[:15]
            print(f"\n  [{label}] '{item}' subset words (top by length): {', '.join(top)}")

# ---------------------------------------------------------------------------
# 4. First letters of each section
# ---------------------------------------------------------------------------
print("\n" + "=" * 80)
print("4. FIRST LETTER OF EACH SECTION")
print("=" * 80)

first_letters = ''.join(s[0] for s in small_sections)
print(f"  Small sections first letters: {first_letters}")
fl_anags = find_anagrams(first_letters, WORDS3)
print(f"  Full anagrams: {fl_anags if fl_anags else 'None'}")

# Also check subsets
fl_lower = first_letters.lower()
fl_counter = Counter(fl_lower)
fl_subset = []
for w in WORDS4:
    if len(w) > len(fl_lower):
        continue
    w_counter = Counter(w)
    if all(w_counter[c] <= fl_counter[c] for c in w_counter):
        fl_subset.append(w)
fl_subset.sort(key=len, reverse=True)
print(f"  Subset words (len>=4): {fl_subset[:20] if fl_subset else 'None'}")

# Also try Caesar on first letters
print(f"  Caesar shifts of '{first_letters}':")
for shift in range(1, 26):
    shifted = caesar(first_letters, shift)
    sl = shifted.lower()
    if sl in WORDS:
        print(f"    ROT-{shift}: {shifted} -- WORD!")
    # Check substrings
    for start in range(len(sl)):
        for end in range(start + 4, len(sl) + 1):
            sub = sl[start:end]
            if sub in WORDS4:
                print(f"    ROT-{shift}: {shifted} -- substring '{sub}'")

# First letters of full columns
fc_first = ''.join(c[0] for c in full_columns)
print(f"\n  Full columns first letters: {fc_first}")
fc_anags = find_anagrams(fc_first, WORDS3)
print(f"  Full anagrams: {fc_anags if fc_anags else 'None'}")

# ---------------------------------------------------------------------------
# 5. Last letters of each section
# ---------------------------------------------------------------------------
print("\n" + "=" * 80)
print("5. LAST LETTER OF EACH SECTION")
print("=" * 80)

last_letters = ''.join(s[-1] for s in small_sections)
print(f"  Small sections last letters: {last_letters}")
ll_anags = find_anagrams(last_letters, WORDS3)
print(f"  Full anagrams: {ll_anags if ll_anags else 'None'}")

ll_lower = last_letters.lower()
ll_counter = Counter(ll_lower)
ll_subset = []
for w in WORDS4:
    if len(w) > len(ll_lower):
        continue
    w_counter = Counter(w)
    if all(w_counter[c] <= ll_counter[c] for c in w_counter):
        ll_subset.append(w)
ll_subset.sort(key=len, reverse=True)
print(f"  Subset words (len>=4): {ll_subset[:20] if ll_subset else 'None'}")

# Caesar on last letters
print(f"  Caesar shifts of '{last_letters}':")
for shift in range(1, 26):
    shifted = caesar(last_letters, shift)
    sl = shifted.lower()
    if sl in WORDS:
        print(f"    ROT-{shift}: {shifted} -- WORD!")
    for start in range(len(sl)):
        for end in range(start + 4, len(sl) + 1):
            sub = sl[start:end]
            if sub in WORDS4:
                print(f"    ROT-{shift}: {shifted} -- substring '{sub}'")

# Last letters of full columns
fc_last = ''.join(c[-1] for c in full_columns)
print(f"\n  Full columns last letters: {fc_last}")
fc_l_anags = find_anagrams(fc_last, WORDS3)
print(f"  Full anagrams: {fc_l_anags if fc_l_anags else 'None'}")

# ---------------------------------------------------------------------------
# 6. Letter-number patterns (A=1, B=2, ... Z=26)
# ---------------------------------------------------------------------------
print("\n" + "=" * 80)
print("6. LETTER-NUMBER PATTERNS (A=1 ... Z=26)")
print("=" * 80)

def letters_to_numbers(text):
    return [ord(c.upper()) - ord('A') + 1 for c in text if c.isalpha()]

for label, items in all_items.items():
    for item in items:
        nums = letters_to_numbers(item)
        total = sum(nums)
        print(f"  [{label}] '{item}': {nums}  sum={total}  mean={total/len(nums):.1f}")

# Check if sums spell something
print(f"\n  Sums of small sections: {[sum(letters_to_numbers(s)) for s in small_sections]}")
section_sums = [sum(letters_to_numbers(s)) for s in small_sections]
print(f"  Sums mod 26 as letters: {''.join(chr((s-1)%26 + ord('A')) for s in section_sums)}")

# Check differences between consecutive letters
print("\n  Differences between consecutive letters in each section:")
for label, items in all_items.items():
    for item in items:
        nums = letters_to_numbers(item)
        diffs = [nums[i+1] - nums[i] for i in range(len(nums)-1)]
        # See if diffs map to letters (mod 26)
        if diffs:
            diff_letters = ''.join(chr((d % 26) + ord('A') - 1) if 1 <= (d % 26) <= 26 else '?' for d in diffs)
            # Actually use mod properly
            diff_letters2 = []
            for d in diffs:
                m = d % 26
                if m == 0:
                    m = 26
                diff_letters2.append(chr(m + ord('A') - 1))
            dl = ''.join(diff_letters2).lower()
            print(f"  [{label}] '{item}': diffs={diffs}, as letters: {''.join(diff_letters2)}")
            if dl in WORDS and len(dl) >= 3:
                print(f"    *** WORD FOUND: {dl} ***")

# ---------------------------------------------------------------------------
# 7. Reading sections backwards
# ---------------------------------------------------------------------------
print("\n" + "=" * 80)
print("7. REVERSED SECTIONS")
print("=" * 80)

reversed_small = [s[::-1] for s in small_sections]
reversed_full = [s[::-1] for s in full_columns]

print(f"  Reversed small sections: {reversed_small}")
print(f"  Reversed full columns: {reversed_full}")

for item in reversed_small + reversed_full:
    il = item.lower()
    if il in WORDS and len(il) >= 3:
        print(f"    '{item}' is a WORD!")

# Concatenate reversed smalls
rev_concat = ''.join(reversed_small)
print(f"\n  Reversed small sections concatenated: {rev_concat}")
rcl = rev_concat.lower()
for start in range(len(rcl)):
    for end in range(start + 5, min(start + 16, len(rcl) + 1)):
        sub = rcl[start:end]
        if sub in WORDS5:
            print(f"    substring '{sub}' at [{start}:{end}]")

# Caesar on reversed
print(f"\n  Caesar on reversed small sections:")
for item in reversed_small:
    for shift in range(1, 26):
        shifted = caesar(item, shift).lower()
        if shifted in WORDS and len(shifted) >= 3:
            print(f"    '{item}' ROT-{shift}: {shifted} -- WORD!")

print(f"\n  Caesar on reversed full columns:")
for item in reversed_full:
    for shift in range(1, 26):
        shifted = caesar(item, shift).lower()
        if shifted in WORDS and len(shifted) >= 3:
            print(f"    '{item}' ROT-{shift}: {shifted} -- WORD!")
    # Also check substrings
    for shift in range(1, 26):
        shifted = caesar(item, shift).lower()
        for start in range(len(shifted)):
            for end in range(start + 4, min(start + 12, len(shifted) + 1)):
                sub = shifted[start:end]
                if sub in WORDS4:
                    print(f"    '{item}' ROT-{shift}: {caesar(item,shift)} -- substring '{sub}' at [{start}:{end}]")

# Anagrams of reversed (same as forward anagrams, skip)

# ---------------------------------------------------------------------------
# 8. Cross-staircase patterns (combining with AROUNDWORLD sections)
# ---------------------------------------------------------------------------
print("\n" + "=" * 80)
print("8. CROSS-STAIRCASE PATTERNS (MELANESIANS + AROUNDWORLD)")
print("=" * 80)

print(f"  MELANESIANS small sections: {small_sections}")
print(f"  AROUNDWORLD small sections:  {aw_sections}")

# Interleave first letters
mel_firsts = ''.join(s[0] for s in small_sections)
aw_firsts = ''.join(s[0] for s in aw_sections)
print(f"\n  MEL first letters: {mel_firsts}")
print(f"  AW  first letters: {aw_firsts}")

# Combine them
combined_firsts = mel_firsts + aw_firsts
print(f"  Combined first letters: {combined_firsts}")
cf_anags = find_anagrams(combined_firsts, WORDS3)
print(f"  Combined anagrams: {cf_anags if cf_anags else 'None'}")

# Interleaved
interleaved = []
for i in range(max(len(small_sections), len(aw_sections))):
    if i < len(small_sections):
        interleaved.append(small_sections[i])
    if i < len(aw_sections):
        interleaved.append(aw_sections[i])
int_firsts = ''.join(s[0] for s in interleaved)
print(f"  Interleaved first letters: {int_firsts}")

# XOR / combine letter by letter (where lengths match)
print(f"\n  Pair first letters (MEL then AW):")
min_len = min(len(small_sections), len(aw_sections))
for i in range(min_len):
    m = small_sections[i][0]
    a = aw_sections[i][0]
    m_n = ord(m) - ord('A')
    a_n = ord(a) - ord('A')
    added = chr((m_n + a_n) % 26 + ord('A'))
    xored = chr((m_n ^ a_n) % 26 + ord('A'))
    print(f"    {m} + {a} = add:{added}  xor:{xored}")

add_result = ''.join(chr(((ord(small_sections[i][0])-65) + (ord(aw_sections[i][0])-65)) % 26 + 65) for i in range(min_len))
print(f"  Addition result: {add_result}")
if add_result.lower() in WORDS:
    print(f"    *** WORD: {add_result} ***")

# Combine all section text
mel_all = ''.join(small_sections)
aw_all = ''.join(aw_sections)
print(f"\n  MEL all text: {mel_all}")
print(f"  AW  all text: {aw_all}")
combined_all = mel_all + aw_all
print(f"  Combined length: {len(combined_all)}")

# Look for words in combined text
cal = combined_all.lower()
print(f"  Words (len>=6) found as substrings in combined text:")
for w in WORDS:
    if len(w) >= 6 and w in cal:
        print(f"    '{w}' found at position {cal.index(w)}")

# ---------------------------------------------------------------------------
# 9. Vigenere cipher with keys MELANESIANS and AROUNDWORLD
# ---------------------------------------------------------------------------
print("\n" + "=" * 80)
print("9. VIGENERE DECRYPTION")
print("=" * 80)

def vigenere_decrypt(ciphertext, key):
    result = []
    ki = 0
    for c in ciphertext.upper():
        if c.isalpha():
            shift = ord(key[ki % len(key)].upper()) - ord('A')
            plain = chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
            result.append(plain)
            ki += 1
        else:
            result.append(c)
    return ''.join(result)

def vigenere_encrypt(plaintext, key):
    result = []
    ki = 0
    for c in plaintext.upper():
        if c.isalpha():
            shift = ord(key[ki % len(key)].upper()) - ord('A')
            cipher = chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
            result.append(cipher)
            ki += 1
        else:
            result.append(c)
    return ''.join(result)

keys = ["MELANESIANS", "AROUNDWORLD", "MELANESIAN", "MRBEAST"]

for key in keys:
    print(f"\n  Key: {key}")
    print(f"  --- Decrypting small sections ---")
    for item in small_sections:
        dec = vigenere_decrypt(item, key)
        dl = dec.lower()
        note = ""
        if dl in WORDS and len(dl) >= 3:
            note = " *** WORD! ***"
        print(f"    '{item}' -> {dec}{note}")

    print(f"  --- Decrypting full columns ---")
    for item in full_columns:
        dec = vigenere_decrypt(item, key)
        dl = dec.lower()
        note = ""
        if dl in WORDS and len(dl) >= 3:
            note = " *** WORD! ***"
        print(f"    '{item}' -> {dec}{note}")
        # Check substrings
        for start in range(len(dl)):
            for end in range(start + 4, len(dl) + 1):
                sub = dl[start:end]
                if sub in WORDS4:
                    print(f"      substring '{sub}' at [{start}:{end}]")

    print(f"  --- Decrypting concatenated small sections ---")
    dec = vigenere_decrypt(concat_small, key)
    print(f"    '{concat_small}' -> {dec}")
    dl = dec.lower()
    for start in range(len(dl)):
        for end in range(start + 5, min(start + 16, len(dl) + 1)):
            sub = dl[start:end]
            if sub in WORDS5:
                print(f"      substring '{sub}' at [{start}:{end}]")

    print(f"  --- Decrypting concatenated full columns ---")
    dec = vigenere_decrypt(concat_full, key)
    print(f"    '{concat_full}' -> {dec}")
    dl = dec.lower()
    for start in range(len(dl)):
        for end in range(start + 5, min(start + 16, len(dl) + 1)):
            sub = dl[start:end]
            if sub in WORDS5:
                print(f"      substring '{sub}' at [{start}:{end}]")

# Also try Vigenere on AW sections with both keys
print(f"\n  --- Decrypting AROUNDWORLD small sections ---")
aw_concat = ''.join(aw_sections)
for key in keys:
    dec = vigenere_decrypt(aw_concat, key)
    print(f"    Key={key}: '{aw_concat}' -> {dec}")
    dl = dec.lower()
    for start in range(len(dl)):
        for end in range(start + 5, min(start + 16, len(dl) + 1)):
            sub = dl[start:end]
            if sub in WORDS5:
                print(f"      substring '{sub}' at [{start}:{end}]")

# ---------------------------------------------------------------------------
# BONUS: Additional tests
# ---------------------------------------------------------------------------
print("\n" + "=" * 80)
print("BONUS: ADDITIONAL TESTS")
print("=" * 80)

# Test: read every Nth letter from concatenated sections
print("\n  --- Every Nth letter from small sections concat ---")
for n in range(2, 6):
    for offset in range(n):
        letters = concat_small[offset::n]
        ll = letters.lower()
        if ll in WORDS and len(ll) >= 3:
            print(f"    Every {n}th letter, offset {offset}: {letters} -- WORD!")
        for start in range(len(ll)):
            for end in range(start + 4, min(start + 12, len(ll) + 1)):
                sub = ll[start:end]
                if sub in WORDS4:
                    print(f"    Every {n}th letter, offset {offset}: {letters} -- substring '{sub}'")

# Test: rail fence / zigzag reads
print("\n  --- Column readings combined with MELANESIANS ---")
# What if we interleave MELANESIANS with the columns?
mel = "MELANESIANS"
for item in full_columns:
    min_l = min(len(mel), len(item))
    interleaved = ''.join(mel[i] + item[i] for i in range(min_l))
    il = interleaved.lower()
    print(f"    MEL interleaved with '{item}': {interleaved}")
    for start in range(len(il)):
        for end in range(start + 5, min(start + 14, len(il) + 1)):
            sub = il[start:end]
            if sub in WORDS5:
                print(f"      substring '{sub}'")

# Test: sections as coordinates
print("\n  --- Section lengths ---")
sec_lens = [len(s) for s in small_sections]
print(f"    Small section lengths: {sec_lens}")
print(f"    As letters (A=1): {''.join(chr(n + ord('A') - 1) for n in sec_lens if 1 <= n <= 26)}")

aw_lens = [len(s) for s in aw_sections]
print(f"    AW section lengths: {aw_lens}")
print(f"    As letters (A=1): {''.join(chr(n + ord('A') - 1) for n in aw_lens if 1 <= n <= 26)}")

# Test: ROT-13 specifically (common cipher)
print("\n  --- ROT-13 of all sections ---")
for item in small_sections + full_columns:
    r13 = caesar(item, 13)
    r13l = r13.lower()
    if r13l in WORDS and len(r13l) >= 3:
        print(f"    '{item}' -> ROT13: {r13} -- WORD!")

# Test: Pairs of sections
print("\n  --- Concatenating consecutive pairs of small sections ---")
for i in range(len(small_sections) - 1):
    pair = small_sections[i] + small_sections[i+1]
    pl = pair.lower()
    if pl in WORDS:
        print(f"    '{pair}' -- WORD!")
    anags = find_anagrams(pair, WORDS3)
    if anags:
        print(f"    '{pair}' anagrams: {', '.join(anags)}")

# Test: All section text as one string, look for hidden words
print("\n  --- Hidden words in small sections concat ---")
csl = concat_small.lower()
print(f"    Concat: {concat_small}")
hidden = []
for w in WORDS:
    if len(w) >= 5 and w in csl:
        hidden.append(w)
hidden.sort(key=len, reverse=True)
if hidden:
    print(f"    Hidden words (len>=5): {hidden[:20]}")

print(f"\n  --- Hidden words in full columns concat ---")
cfl = concat_full.lower()
print(f"    Concat: {concat_full}")
hidden2 = []
for w in WORDS:
    if len(w) >= 5 and w in cfl:
        hidden2.append(w)
hidden2.sort(key=len, reverse=True)
if hidden2:
    print(f"    Hidden words (len>=5): {hidden2[:20]}")

# Test: Take Nth letter of each section
print("\n  --- Nth letter of each small section ---")
for n in range(10):
    letters = ''
    for s in small_sections:
        if n < len(s):
            letters += s[n]
    if letters:
        ll = letters.lower()
        print(f"    Position {n}: {letters}", end="")
        if ll in WORDS and len(ll) >= 3:
            print(f" -- WORD!", end="")
        # Check anagrams
        anags = find_anagrams(letters, WORDS3)
        if anags:
            print(f" -- anagrams: {', '.join(anags)}", end="")
        print()

# Test: Middle letters
print("\n  --- Middle letter of each small section ---")
middles = ''
for s in small_sections:
    mid = len(s) // 2
    middles += s[mid]
print(f"    Middles: {middles}")
mid_anags = find_anagrams(middles, WORDS3)
if mid_anags:
    print(f"    Anagrams: {', '.join(mid_anags)}")

# Double-check: GRONARAC anagram search more carefully
print("\n  --- Exhaustive anagram check for GRONARAC ---")
target = "GRONARAC"
tl = target.lower()
tc = Counter(tl)
# Find all words that can be made from these letters
possible = []
for w in WORDS:
    if len(w) >= 4 and len(w) <= len(tl):
        wc = Counter(w)
        if all(wc[c] <= tc[c] for c in wc):
            possible.append(w)
possible.sort(key=len, reverse=True)
print(f"    Words from letters of '{target}': {possible[:30]}")

# Two-word anagram split
print(f"\n  --- Two-word anagram of GRONARAC ---")
possible_set = set(possible)
for w1 in possible:
    if len(w1) < 2:
        continue
    remaining = list(tl)
    for c in w1:
        remaining.remove(c)
    rem_sorted = ''.join(sorted(remaining))
    for w2 in possible:
        if ''.join(sorted(w2)) == rem_sorted:
            print(f"    {w1.upper()} + {w2.upper()}")

# Same for ITPPEVAO
print(f"\n  --- Exhaustive anagram check for ITPPEVAO ---")
target2 = "ITPPEVAO"
tl2 = target2.lower()
tc2 = Counter(tl2)
possible2 = []
for w in WORDS:
    if len(w) >= 4 and len(w) <= len(tl2):
        wc = Counter(w)
        if all(wc[c] <= tc2[c] for c in wc):
            possible2.append(w)
possible2.sort(key=len, reverse=True)
print(f"    Words from letters of '{target2}': {possible2[:30]}")

# Two-word anagram split
print(f"\n  --- Two-word anagram of ITPPEVAO ---")
for w1 in possible2:
    if len(w1) < 3:
        continue
    remaining = list(tl2)
    valid = True
    for c in w1:
        if c in remaining:
            remaining.remove(c)
        else:
            valid = False
            break
    if not valid:
        continue
    rem_sorted = ''.join(sorted(remaining))
    for w2 in possible2:
        if len(w2) < 2:
            continue
        if ''.join(sorted(w2)) == rem_sorted:
            print(f"    {w1.upper()} + {w2.upper()}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
