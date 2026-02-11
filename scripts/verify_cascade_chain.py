#!/usr/bin/env python3
"""
Verify the cascade chain and investigate suspicious patterns.
Key question: Are ORIENT (141D) and HOODIE (142D) correct?
"""

# The cascade chain:
# HULAHOOP (133D) → RACE (153A) → TEAMSEAS (174A) → ORIENT (141D) + HOODIE (142D) + MUSTERS (137D)
#
# Suspicious results:
# 171A = NI????RR (8 letters) - very unusual
# 165A = ED????CE (8 letters) - unusual
#
# Let me verify each placement in the chain.

print("=" * 70)
print("CASCADE CHAIN VERIFICATION")
print("=" * 70)

# 1. HULAHOOP at 133D
print("\n1. HULAHOOP at 133D: (17,15) down, len 8")
print("   Pattern: ?????O?? where O at pos 5 from ?")
print("   Let me trace where the O comes from:")
print("   132A at (17,13) len 4 = cols 13-16")
print("   Col 15 = pos 2 of 132A")
print("   132A has V at col 13 (from DENVER at 110D)")
print("   DENVER: (14,13) down, len 6 = rows 14-19")
print("   Row 17 = pos 3 = V (D-E-N-V-E-R)")
print("   So 132A = V?H? (V at pos 0 from DENVER, H at pos 2 from HULAHOOP)")
print("   Wait, I need to check what puts O at (22,15)")
print()
print("   133D cells: (17,15),(18,15),(19,15),(20,15),(21,15),(22,15),(23,15),(24,15)")
print("   SUPERBOWLSTADIUM at (22,9) = cols 9-24")
print("   Col 15 = pos 6 = O (S-U-P-E-R-B-O-W-L-S-T-A-D-I-U-M)")
print("   Wait: S(0)U(1)P(2)E(3)R(4)B(5)O(6)... pos 6 = O, col = 9+6 = 15")
print("   YES: O at (22,15) from SUPERBOWLSTADIUM")
print("   Pattern: ?????(22,15=O)?? = ?????O??")
print("   HULAHOOP = H-U-L-A-H-O-O-P. O at pos 5 ✓")
print("   Other 8-letter words matching ?????O??:")

# Check all 8-letter answers
answers_8 = ['HOODWINK', 'HULAHOOP', 'SCENARIO', 'NEUROTIC', 'SCREENER', 'ABSOLUTE',
             'TEAMSEAS', 'DURATION', 'CARBLITE', 'POSITRON', 'ROUTINES', 'FLAMINGO',
             'CASHTENT', 'ADELAIDE']
matches = [a for a in answers_8 if a[5] == 'O']
print(f"   Matches from our bank: {matches}")
print("   Only HULAHOOP has O at pos 5. UNIQUE ✓")

# But wait, need to check ALL constraints on 133D
print("\n   Additional constraints on 133D:")
print("   pos 2 = (19,15) - in 19A row: (19,5-6 black)(19,7-10 = 143A)(19,11 black)(19,12-15 = 145A)")
print("   145A at (19,12) len 4 = cols 12-15. Col 15 = pos 3.")
print("   133D pos 2 = 145A pos 3. If HULAHOOP[2]=L, then 145A ends in L.")
print("   Solver showed 145A: ?R?L (R from where?)")
print("   139D at (18,12) len 7 = rows 18-24. Row 19 = pos 1. Col 12, 145A pos 0 = 139D[1].")
print("   Actually: DENVER at 110D ends at row 19. 110D (14,13) len 6 = rows 14-19.")
print("   Row 19, col 13 = pos 5 = R. 145A at (19,12) len 4 = cols 12-15. Col 13 = pos 1 = R.")
print("   So 145A = ?R?L. What 4-letter words match ?R?L?")
print()

words_4 = ['DHOW', 'RACE', 'NOTE']
m4 = [w for w in words_4 if len(w)==4 and w[1]=='R' and w[3]=='L']
print(f"   4-letter matches for ?R?L from our bank: {m4}")
print("   None from our bank. But common English: ORAL, GRIL, TRAWL(5)...")
print("   ORAL? O-R-A-L. Doesn't match... wait, ORAL has R at 1 and L at 3. Matches ?R?L!")
print("   But ORAL is not in our answer bank. Could be a standard crossword word though.")
print()

# 2. ACCRA at 151D
print("\n2. ACCRA at 151D: (20,6) down, len 5")
print("   Pattern: A???? where A from BEASTLAND")
print("   149A = BEASTLAND at (20,4) len 9 = cols 4-12")
print("   Col 6 = pos 2 = A (B-E-A-S-T-L-A-N-D)")
print("   Wait! BEASTLAND[2] = A at col 4+2 = col 6. YES!")
print()
print("   151D cells: (20,6),(21,6),(22,6),(23,6),(24,6)")
print("   Any other constraints?")
print("   (22,6) = 165A at (22,0) len 8. Col 6 = pos 6.")
print("   (24,6) = 174A at (24,0) len 8. Col 6 = pos 6.")
print()
print("   5-letter words matching A????:")
answers_5 = ['WAHOO', 'OPERA', 'LECAR', 'TEMPE', 'DOVER', 'ACCRA']
m5 = [w for w in answers_5 if w[0] == 'A']
print(f"   From our bank: {m5}")
print("   Only ACCRA starts with A. UNIQUE ✓")

# 3. RACE at 153A
print("\n3. RACE at 153A: (20,14) len 4")
print("   Pattern: ?A?? where A at pos 1 from HULAHOOP")
print("   133D = HULAHOOP at (17,15) down. Row 20 = pos 3 = A.")
print("   But 133D is at col 15! 153A at (20,14) col 14 = pos 0, col 15 = pos 1.")
print("   So 153A pos 1 = A from HULAHOOP. Pattern = ?A??")
m4_a = [w for w in words_4 if w[1] == 'A']
print(f"   Matches: {m4_a}")
print("   Only RACE. UNIQUE ✓")

# 4. TEAMSEAS at 174A
print("\n4. TEAMSEAS at 174A: (24,0) len 8")
print("   Pattern: ??????A? where A at pos 6 from ACCRA")
print("   ACCRA at 151D row 24 = pos 4 = A at (24,6). 174A col 6 = pos 6. ✓")
m8_a = [w for w in answers_8 if len(w)==8 and w[6]=='A']
print(f"   Matches: {m8_a}")
print("   Only TEAMSEAS. UNIQUE ✓")

# 5. ORIENT at 141D
print("\n5. ORIENT at 141D: (19,0) down, len 6")
print("   Pattern: ?????T where T at pos 5 from TEAMSEAS")
print("   TEAMSEAS at (24,0) = T at pos 0 = col 0. 141D at col 0, row 24 = pos 5.")
answers_6 = ['SCHOOL', 'OHIOAN', 'HOODIE', 'MATTER', 'ECLAIR', 'OPTION', 'ORIENT',
             'CHAIRS', 'CONVEX', 'WARSAW', 'OTTAWA', 'AUBURN']
m6_t = [w for w in answers_6 if w[5] == 'T']
print(f"   Matches: {m6_t}")
print("   Only ORIENT ends in T. UNIQUE ✓")

# 6. HOODIE at 142D
print("\n6. HOODIE at 142D: (19,1) down, len 6")
print("   Pattern: ?????E where E at pos 5 from TEAMSEAS")
print("   TEAMSEAS[1] = E at (24,1). 142D at col 1, row 24 = pos 5.")
m6_e = [w for w in answers_6 if w[5] == 'E']
print(f"   Matches: {m6_e}")
print("   Only HOODIE ends in E. UNIQUE ✓")

# 7. MUSTERS at 137D
print("\n7. MUSTERS at 137D: (18,7) down, len 7")
print("   Pattern: ??S???S where:")
print("   S at pos 2 from BEASTLAND: (20,7) = BEASTLAND[3] = S. 137D row 20 = pos 2.")
print("   S at pos 6 from TEAMSEAS: (24,7) = TEAMSEAS[7] = S. 137D row 24 = pos 6.")
answers_7 = ['TYPHOON', 'OHSHOOT', 'HEARTED', 'MUSTERS', 'CALIBER', 'PORTION',
             'INUTERO', 'QUORUMS', 'HIRPLED', 'TORONTO', 'ROSWELL', 'DRESDEN',
             'SANJUAN', 'SEVILLE', 'ORLANDO', 'WOODWAY']
m7_ss = [w for w in answers_7 if w[2] == 'S' and w[6] == 'S']
print(f"   Matches: {m7_ss}")
print("   Only MUSTERS. UNIQUE ✓")

# ============================================================
print("\n" + "=" * 70)
print("SUSPICIOUS PATTERN INVESTIGATION")
print("=" * 70)

# 171A = NI????RR
print("\n171A at (23,0) len 8:")
print("  N at (23,0) from ORIENT[4]=N")
print("  I at (23,1) from HOODIE[4]=I")
print("  R at (23,6) from ACCRA[3]=R")
print("  R at (23,7) from MUSTERS[5]=R")
print("  Pattern: NI????RR")
print()
print("  Is there ANY 8-letter word matching NI????RR?")
# Think harder...
# NIGHTJAR? N-I-G-H-T-J-A-R → ends in AR not RR
# NIGHTMARE → 9 letters
# NICEHERR → not a word
# What about with double R at end:
# Words ending in RR: BURR, PURR, STARR...
# 8-letter words ending RR?
# NIGHTMARRR? No
# ABHORRER → A-B-H-O-R-R-E-R → no, ends ER
# DEFERRER → 8 but starts with D
# INCURRER → I-N-C-U-R-R-E-R → 8 letters, starts IN not NI
# NIFTIERR → not a word
# Wait: the pattern is NI????RR, not NI????R?
# Words matching NI_____RR:
# Could be a proper noun or creative fill
# NIAGARARR? No
# What if the penultimate position is not R? Let me recheck.
# 171A at (23,0) len 8 = cols 0-7
# Col 6 = pos 6: ACCRA[3] at row 23. ACCRA at (20,6) down. Row 23 = pos 3 = R. Yes.
# Col 7 = pos 7: MUSTERS[5] at row 23. MUSTERS at (18,7) down. Row 23 = pos 5 = R. Yes.
# Hmm, so we have R at pos 6 AND R at pos 7. Very unusual.
print("  Possible issue: RR ending is extremely rare in English")
print("  This MIGHT indicate an error in ACCRA or MUSTERS")
print()
print("  ALTERNATIVE: What if 151D ≠ ACCRA?")
print("  151D pattern was A????. Other 5-letter words starting A:")
print("  From full P1+P3+P8+P9 bank: ABASH(placed), ADORN(placed), ACHOO(placed), ACCRA")
print("  Only ACCRA starts with A and is unplaced. But bank is incomplete!")
print("  Common 5-letter words starting A: ABOUT, ABOVE, AFTER, AGAIN, ALONG, ...")
print("  Many possibilities from answers we don't know yet")
print()

# 165A = ED????CE
print("165A at (22,0) len 8:")
print("  E at (22,0) from ORIENT[3]=E")
print("  D at (22,1) from HOODIE[3]=D")
print("  C at (22,6) from ACCRA[2]=C")
print("  E at (22,7) from MUSTERS[4]=E")
print("  Pattern: ED????CE")
print()
print("  8-letter words matching ED????CE:")
# EDIFERCE? No
# EDDIANCE? No
# Let me think systematically...
# ED + 4 chars + CE
# EDDIANCE → not a word
# EDGIANCE → not a word
# EDUCANCE → not a word
# EDURANCE → not a word
# EDUCIBLE → ends LE not CE
# EDINONCE → not a word
# What about EDDYCCE → no
# EDIFANCE → no
# ED????CE...
# EDULCECE? No...

# Let me try a different approach: what English words match ED____CE?
# With regex: ed[a-z]{4}ce
import re
try:
    with open('/usr/share/dict/words', 'r') as f:
        all_words = [w.strip().upper() for w in f]
    ed_ce = [w for w in all_words if len(w) == 8 and re.match(r'ED....CE', w)]
    print(f"  Dictionary matches: {ed_ce}")
except:
    print("  (No dictionary available)")

# Try: what if it's a compound?
# ED + ???? + CE
# EDICANCE, EDUCANCE... none are words
# What about ending in -ENCE or -ANCE?
# ED????CE - the C and E at positions 6-7 could be part of -ENCE, -ANCE, -ONCE, -INCE
# But then positions 4-5 are part of the root
# EVIDENCE = E-V-I-D-E-N-C-E → but starts EV not ED
# CREDENCE = 8 letters C-R-E-D-E-N-C-E → starts CR not ED
# PRUDENCE = 8 letters P-R-U-D-E-N-C-E → starts PR
# AUDIENCE = A-U-D-I-E-N-C-E → starts AU
# OBEDIENCE = 9 letters
# ADHERENCE = 9 letters

# Wait... EDDYLIKE? No, ends in KE
# EDGEWISE? No, ends in SE

# Hmm, very few words start ED and end CE
# Could be:
# EDDYTRACE → too long
# EDUCIBLE → ends LE

# What about creative crossword fill? EDWARDSCE? EDRICACE?
# These aren't real words.

# Actually: EDEDENCE? EDELENCE?
# What about: ED + obscure + CE?
# EDDYFACE? Not a word
# EDITRICE? E-D-I-T-R-I-C-E = 8 letters!
# EDITRICE is the feminine form of "editor" in Italian
# ED????CE: E-D-I-T-R-I-C-E. I at 2, T at 3, R at 4, I at 5.
# Pattern ED????CE → EDITRICE would be E-D-I-T-R-I-C-E
print("  EDITRICE? (Italian for female editor) - E-D-I-T-R-I-C-E")
print("  Unlikely in an English crossword")
print()
print("  ED????CE is very unusual. Possible conclusions:")
print("  1. One of ORIENT/HOODIE/ACCRA/MUSTERS is wrong")
print("  2. The answer is a proper noun or multi-word phrase")
print("  3. The answer is from a puzzle set we haven't solved")
print()
print("  NOTE: 165A is at row 22, which is also where SUPERBOWLSTADIUM is.")
print("  165A (cols 0-7) is LEFT of 167A (cols 9-24). There's a black cell at (22,8).")

# ============================================================
print("\n" + "=" * 70)
print("CONFIDENCE ASSESSMENT")
print("=" * 70)
print()
print("Chain: HULAHOOP → RACE → TEAMSEAS → ORIENT + HOODIE + MUSTERS")
print()
print("HULAHOOP: HIGH confidence (O from SUPERBOWLSTADIUM, unique in bank)")
print("  RACE: HIGH confidence (A from HULAHOOP, unique in bank)")
print("ACCRA: MEDIUM confidence (A from BEASTLAND, unique in bank)")
print("  TEAMSEAS: MEDIUM confidence (A from ACCRA, unique in bank)")
print("  ORIENT: MEDIUM confidence (T from TEAMSEAS, unique in bank)")
print("  HOODIE: MEDIUM confidence (E from TEAMSEAS, unique in bank)")
print("  MUSTERS: MEDIUM confidence (S+S from BEASTLAND+TEAMSEAS, unique in bank)")
print()
print("ALL are 'unique in our bank' but bank only has ~82 of 176 answers.")
print("The NI????RR (171A) and ED????CE (165A) patterns are SUSPICIOUS.")
print("ORIENT and HOODIE are most likely to be wrong (longest cascade chain).")
print()
print("RECOMMENDATION: Accept HULAHOOP (133D) and RACE (153A) with HIGH confidence.")
print("Accept ACCRA (151D) with MEDIUM confidence.")
print("Accept TEAMSEAS (174A) with MEDIUM-HIGH (Jimmy+Mark's ocean charity is very on-brand).")
print("Flag ORIENT, HOODIE, MUSTERS as SPECULATIVE until we can verify 165A or 171A.")
