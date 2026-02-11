#!/usr/bin/env python3
"""
Final targeted analysis on strongest findings.
"""
from collections import Counter

def load_dict(path="/home/user/MB/puzzle/words.txt"):
    words = set()
    with open(path) as f:
        for w in f:
            w = w.strip().lower()
            if w:
                words.add(w)
    return words

WORDS = load_dict()

def vigenere_decrypt(ct, key):
    result, ki = [], 0
    for c in ct.upper():
        if c.isalpha():
            result.append(chr((ord(c) - ord(key[ki % len(key)].upper())) % 26 + 65))
            ki += 1
        else:
            result.append(c)
    return ''.join(result)

def caesar(text, shift):
    return ''.join(chr((ord(c.upper()) - 65 + shift) % 26 + 65) if c.isalpha() else c for c in text)

print("=" * 80)
print("FINAL TARGETED ANALYSIS")
print("=" * 80)

# -----------------------------------------------------------------------
# A. KRAAL deep dive (position 4 across full columns = LKARA)
# -----------------------------------------------------------------------
print("\n--- KRAAL: Position 4 across full columns ---")
full_columns = ["GIIHL", "RTRAKA", "OEAJAPCNEO", "ACYPRPVY", "NEANAA"]
pos4 = ''.join(c[4] for c in full_columns if len(c) > 4)
print(f"Position 4 letters: {pos4}")
print(f"LKARA anagrams to KRAAL (a livestock enclosure / village in South Africa)")
print(f"This is thematically connected to MELANESIANS (both indigenous peoples/cultures)")

# Check all positions for words and anagram words
print("\n--- ALL POSITION READS across full columns ---")
max_len = max(len(c) for c in full_columns)
for pos in range(max_len):
    letters = ''.join(c[pos] for c in full_columns if len(c) > pos)
    if len(letters) < 3:
        continue
    ll = letters.lower()
    # Direct
    if ll in WORDS:
        print(f"  Pos {pos}: {letters} -- DIRECT WORD")
    # Anagram
    tc = Counter(ll)
    anags = [w for w in WORDS if len(w) == len(ll) and Counter(w) == tc]
    if anags:
        print(f"  Pos {pos}: {letters} -- anagrams: {anags}")
    # Caesar
    for s in range(1, 26):
        shifted = caesar(letters, s).lower()
        if shifted in WORDS:
            print(f"  Pos {pos}: {letters} ROT-{s} -> {shifted}")

# -----------------------------------------------------------------------
# B. GROAN context - what does it mean in context?
# -----------------------------------------------------------------------
print("\n--- GROAN ANALYSIS ---")
print("Full column first letters: G R O A N = GROAN")
print("Also anagrams to: ORGAN, ARGON, ORANG, GRANO, NAGOR, AGRON")
print()
print("Could GROAN be a clue word? Or ORGAN?")
print("ORANG = orangutan (relevant to wildlife/geography theme?)")
print("ARGON = chemical element #18")

# -----------------------------------------------------------------------
# C. CACIQUE significance test - how likely is this by chance?
# -----------------------------------------------------------------------
print("\n--- CACIQUE PROBABILITY ANALYSIS ---")
print("Vigenere(concat_small_sections, MELANESIANS) = UEGTBAICACIQUENRNXNAXIQJTO")
print("CACIQUE (7 letters) appears at position 7")
print("A cacique is a chief of an indigenous people, especially in Latin America")
print("This is thematically linked to MELANESIANS (indigenous Pacific Islanders)")
print()
# Count 7-letter words in dictionary
seven_letter = [w for w in WORDS if len(w) == 7]
print(f"Total 7-letter words in dictionary: {len(seven_letter)}")
# Probability of random 7-letter sequence being a word
print(f"Random chance: {len(seven_letter)}/26^7 = {len(seven_letter)/(26**7):.6%}")
print("However, this appears within a 26-letter decrypted string, so there are ~20 possible")
print("starting positions for a 7-letter word, increasing the chance somewhat.")
print(f"Adjusted: ~{20 * len(seven_letter)/(26**7):.4%}")

# -----------------------------------------------------------------------
# D. What if the AROUNDWORLD columns also spell something?
# -----------------------------------------------------------------------
print("\n--- AROUNDWORLD STAIRCASE SECTIONS FIRST/LAST LETTERS ---")
aw_sections = ["MHGSAA", "LASD", "EUA", "GEEA", "IN", "NH", "GDH", "TL", "EH"]
aw_firsts = ''.join(s[0] for s in aw_sections)
aw_lasts = ''.join(s[-1] for s in aw_sections)
print(f"AW first letters: {aw_firsts}")
print(f"AW last letters:  {aw_lasts}")

# Check both for words / anagrams
for label, text in [("AW firsts", aw_firsts), ("AW lasts", aw_lasts)]:
    tl = text.lower()
    tc = Counter(tl)
    anags = [w for w in WORDS if len(w) == len(tl) and Counter(w) == tc]
    print(f"  {label} ({text}) anagrams: {anags[:10] if anags else 'None'}")
    # Subsets
    subsets = [w for w in WORDS if len(w) >= 5 and len(w) <= len(tl) and all(Counter(w)[c] <= tc[c] for c in Counter(w))]
    subsets.sort(key=len, reverse=True)
    print(f"  {label} subset words: {subsets[:15] if subsets else 'None'}")

# -----------------------------------------------------------------------
# E. Combined first-letter analysis
# -----------------------------------------------------------------------
print("\n--- COMBINED FIRST-LETTER WORDS ---")
mel_firsts = "GROANRAC"  # from MELANESIANS small sections
# Break into meaningful combinations
print(f"MEL firsts: {mel_firsts}")
print(f"Starts with GROAN (5 letters) leaving RAC")
print(f"RAC anagrams: ARC, CAR")
print(f"So: GROAN + ARC, GROAN + CAR")

# -----------------------------------------------------------------------
# F. Comprehensive Vigenere with many keys
# -----------------------------------------------------------------------
print("\n--- VIGENERE WITH ADDITIONAL KEYS ---")
concat_small = "GIRTOEAKAPACYPNERPVAKACNEO"
concat_full = "GIIHLRTRAKAOEAJAPCNEOACYPRPVYNEANAA"

extra_keys = [
    "GROAN", "ORGAN", "ARGON", "KRAAL", "CACIQUE", "ORANG",
    "GIRT", "YAWN", "ONCE", "CONE", "BEAST", "MILLION",
    "PUZZLE", "ANSWER", "SECRET", "HIDDEN", "STAIRCASE",
    "PACIFIC", "ISLANDS", "OCEANIA", "GEOGRAPHY"
]

for key in extra_keys:
    dec_s = vigenere_decrypt(concat_small, key).lower()
    dec_f = vigenere_decrypt(concat_full, key).lower()

    hits_s = []
    for start in range(len(dec_s)):
        for end in range(start+5, min(start+16, len(dec_s)+1)):
            sub = dec_s[start:end]
            if sub in WORDS and len(sub) >= 5:
                hits_s.append(sub)

    hits_f = []
    for start in range(len(dec_f)):
        for end in range(start+5, min(start+16, len(dec_f)+1)):
            sub = dec_f[start:end]
            if sub in WORDS and len(sub) >= 5:
                hits_f.append(sub)

    if hits_s or hits_f:
        print(f"\n  Key: {key}")
        if hits_s:
            print(f"    Small sections -> {dec_s.upper()}")
            print(f"    Hits: {hits_s}")
        if hits_f:
            print(f"    Full columns -> {dec_f.upper()}")
            print(f"    Hits: {hits_f}")

# Also try the main extraction words themselves
for key in ["MELANESIANS", "AROUNDWORLD"]:
    # Try encrypting (adding key) instead of decrypting
    enc_s = ''
    ki = 0
    for c in concat_small:
        shift = ord(key[ki % len(key)]) - 65
        enc_s += chr((ord(c) - 65 + shift) % 26 + 65)
        ki += 1

    enc_f = ''
    ki = 0
    for c in concat_full:
        shift = ord(key[ki % len(key)]) - 65
        enc_f += chr((ord(c) - 65 + shift) % 26 + 65)
        ki += 1

    hits_s = []
    el = enc_s.lower()
    for start in range(len(el)):
        for end in range(start+5, min(start+16, len(el)+1)):
            sub = el[start:end]
            if sub in WORDS and len(sub) >= 5:
                hits_s.append(sub)

    hits_f = []
    el = enc_f.lower()
    for start in range(len(el)):
        for end in range(start+5, min(start+16, len(el)+1)):
            sub = el[start:end]
            if sub in WORDS and len(sub) >= 5:
                hits_f.append(sub)

    if hits_s or hits_f:
        print(f"\n  Key (ENCRYPT): {key}")
        if hits_s:
            print(f"    Small sections -> {enc_s}")
            print(f"    Hits: {hits_s}")
        if hits_f:
            print(f"    Full columns -> {enc_f}")
            print(f"    Hits: {hits_f}")

# -----------------------------------------------------------------------
# G. Test if section lengths encode something
# -----------------------------------------------------------------------
print("\n--- SECTION LENGTH ANALYSIS ---")
small_sections = ["GI", "RT", "OEAKAP", "ACYP", "NE", "RPV", "AKA", "CNEO"]
mel_lens = [len(s) for s in small_sections]
aw_lens = [len(s) for s in aw_sections]
print(f"MEL section lengths: {mel_lens} = {sum(mel_lens)} total")
print(f"AW  section lengths: {aw_lens} = {sum(aw_lens)} total")
print(f"MEL lengths as letters: {''.join(chr(n + 64) for n in mel_lens)}")
print(f"AW  lengths as letters: {''.join(chr(n + 64) for n in aw_lens)}")

# Number of sections
print(f"\nMEL has {len(small_sections)} sections, AW has {len(aw_sections)} sections")

# -----------------------------------------------------------------------
# H. What if each small section is an entry in a substitution table?
# -----------------------------------------------------------------------
print("\n--- SUBSTITUTION TABLE HYPOTHESIS ---")
print("If each section maps to its corresponding MELANESIANS letter:")
for i, (sec, letter) in enumerate(zip(small_sections, "MELANESIA")):
    print(f"  {sec} -> {letter}")
print("  (MELANESIANS has 11 letters, only 8 small sections - checking if N,S are handled differently)")

# Check: first letter of each section vs MELANESIANS
print("\nFirst letters of sections vs MELANESIANS:")
mel = "MELANESIANS"
mel_first = ''.join(s[0] for s in small_sections)
print(f"  Section firsts: {mel_first}")
print(f"  MELANESIANS:    {mel[:len(mel_first)]}")
# Difference
for i in range(len(mel_first)):
    m = mel[i]
    s = mel_first[i]
    diff = (ord(s) - ord(m)) % 26
    print(f"  {m} -> {s} : diff = {diff} ({chr(diff + 65) if diff > 0 else '-'})")

# -----------------------------------------------------------------------
# I. Check: does reading only certain letters from MELANESIANS + other columns give a message?
# -----------------------------------------------------------------------
print("\n--- MELANESIANS PARALLEL READ ---")
# If the main column is MELANESIANS and the other columns are read at same positions
# The grid has specific positions for each column
# MELANESIANS is 11 letters, columns have varying lengths

# What if we take one letter from each column at row corresponding to MELANESIANS letter?
# M=13, E=5, L=12, A=1, N=14, E=5, S=19, I=9, A=1, N=14, S=19
mel_nums = [ord(c) - 64 for c in "MELANESIANS"]
print(f"MELANESIANS as numbers: {mel_nums}")

# -----------------------------------------------------------------------
# J. Complete readout of everything that tested positive
# -----------------------------------------------------------------------
print("\n" + "=" * 80)
print("SUMMARY OF ALL POSITIVE FINDINGS")
print("=" * 80)

findings = [
    ("STRONG", "GROAN", "Full column first letters spell GROAN (also anagram of ORGAN, ARGON, ORANG)"),
    ("STRONG", "CACIQUE", "Vigenere decrypt of concatenated small sections with key MELANESIANS produces CACIQUE at pos 7-13 (a chief of indigenous people)"),
    ("MODERATE", "YAWN", "ACYP under ROT-24 (shift -2) = YAWN"),
    ("MODERATE", "GIRT", "GI + RT concatenated = GIRT (past tense of gird)"),
    ("MODERATE", "ONCE/CONE", "CNEO anagrams to ONCE or CONE"),
    ("MODERATE", "KRAAL", "Position 4 across full columns (LKARA) anagrams to KRAAL (African livestock enclosure)"),
    ("WEAK", "AKA", "AKA is already a word (also known as)"),
    ("WEAK", "GRIS", "CNEO ROT-4 = GRIS (French for gray)"),
    ("WEAK", "AYE", "RPV ROT-9 = AYE"),
    ("WEAK", "MOON", "GIIHL ROT-6 starts with MOON (MOONR)"),
    ("WEAK", "RANCOR/GARCON/ANGORA", "GROANRAC (all small section first letters) forms 2-word anagram pairs"),
    ("WEAK", "POTPIE/OPIATE/PIVOT", "ITPPEVAO (all small section last letters) contains these as subset anagrams"),
    ("WEAK", "ICE", "VPR (reversed RPV) ROT-13 = ICE"),
    ("WEAK", "TROTH", "Vigenere(small_concat, AROUNDWORLD) contains TROTH at pos 14-18"),
    ("WEAK", "PEEP", "Position 5 across full columns (APPA) ROT-15 = PEEP"),
    ("WEAK", "PAPA", "Position 5 across full columns (APPA) anagram = PAPA"),
]

for strength, word, explanation in findings:
    print(f"\n  [{strength:8s}] {word}")
    print(f"           {explanation}")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
