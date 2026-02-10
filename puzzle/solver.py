#!/usr/bin/env python3
"""
Crossword Solver Engine for the MrBeast $1M Puzzle.

Supports:
- Dictionary-based backtracking solve
- Constraint propagation (arc consistency)
- Known answer injection
- Partial solve (fill what we can)
- Letter extraction from circled/numbered cells
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

PUZZLE_PATH = Path(__file__).parent / "puzzle.json"

# ============================================================
# Known/confirmed answers (add as discovered)
# Format: {entry_number: "ANSWER"} for across and down separately
# ============================================================
KNOWN_ACROSS = {
    # Example: 1: "EXAMPLE",
}

KNOWN_DOWN = {
    # Example: 1: "EXAMPLE",
}

def load_puzzle():
    with open(PUZZLE_PATH) as f:
        return json.load(f)

def load_dictionary(paths=None):
    """Load word list(s). Tries multiple common locations."""
    if paths is None:
        paths = [
            "/usr/share/dict/words",
            "/usr/share/dict/american-english",
            Path(__file__).parent / "words.txt",
        ]
    words = set()
    for p in paths:
        p = Path(p)
        if p.exists():
            with open(p) as f:
                for line in f:
                    w = line.strip().upper()
                    if w.isalpha() and len(w) >= 1:
                        words.add(w)
            print(f"Loaded {len(words)} words from {p}")
            break
    return words

def build_word_bank(words):
    """Group words by length."""
    bank = defaultdict(list)
    for w in words:
        bank[len(w)].append(w)
    return bank

class CrosswordSolver:
    def __init__(self, puzzle, word_bank=None):
        self.size = puzzle["grid_size"]
        self.grid_data = puzzle["grid"]
        self.entries = puzzle["entries"]

        # Build cell grid: maps (row, col) -> current letter or None
        self.cells = {}
        for r in range(self.size):
            for c in range(self.size):
                if self.grid_data[r][c] != 1:  # not black
                    self.cells[(r, c)] = None

        # Parse entries into solver format
        self.across_entries = {}
        self.down_entries = {}
        self._parse_entries()

        # Word bank for solving
        self.word_bank = word_bank or {}

        # Track which entries are filled
        self.filled = {}

    def _parse_cell(self, cell_str):
        col = ord(cell_str[0]) - 65
        row = int(cell_str[1:]) - 1
        return (row, col)

    def _parse_entries(self):
        for num_str, entry in self.entries.get("across", {}).items():
            num = int(num_str)
            cells = [self._parse_cell(c) for c in entry["cells"]]
            self.across_entries[num] = {
                "cells": cells,
                "length": entry["length"],
                "start": entry["start"],
            }

        for num_str, entry in self.entries.get("down", {}).items():
            num = int(num_str)
            cells = [self._parse_cell(c) for c in entry["cells"]]
            self.down_entries[num] = {
                "cells": cells,
                "length": entry["length"],
                "start": entry["start"],
            }

    def place_known_answers(self):
        """Place all known answers into the grid."""
        placed = 0
        for num, answer in KNOWN_ACROSS.items():
            if num in self.across_entries:
                entry = self.across_entries[num]
                if len(answer) == entry["length"]:
                    for i, (r, c) in enumerate(entry["cells"]):
                        self.cells[(r, c)] = answer[i]
                    self.filled[("across", num)] = answer
                    placed += 1
                else:
                    print(f"WARNING: ACROSS #{num} answer '{answer}' length {len(answer)} != expected {entry['length']}")

        for num, answer in KNOWN_DOWN.items():
            if num in self.down_entries:
                entry = self.down_entries[num]
                if len(answer) == entry["length"]:
                    for i, (r, c) in enumerate(entry["cells"]):
                        self.cells[(r, c)] = answer[i]
                    self.filled[("down", num)] = answer
                    placed += 1
                else:
                    print(f"WARNING: DOWN #{num} answer '{answer}' length {len(answer)} != expected {entry['length']}")

        return placed

    def get_current_pattern(self, entry):
        """Get the current letter pattern for an entry (e.g., 'H_LL_')."""
        pattern = ""
        for r, c in entry["cells"]:
            letter = self.cells.get((r, c))
            pattern += letter if letter else "_"
        return pattern

    def word_fits(self, word, entry):
        """Check if a word can be placed in an entry without conflicts."""
        if len(word) != entry["length"]:
            return False
        for i, (r, c) in enumerate(entry["cells"]):
            current = self.cells.get((r, c))
            if current is not None and current != word[i]:
                return False
        return True

    def get_candidates(self, entry, max_results=100):
        """Get candidate words for an entry based on current grid state and dictionary."""
        length = entry["length"]
        if length not in self.word_bank:
            return []
        pattern = self.get_current_pattern(entry)
        candidates = []
        for word in self.word_bank[length]:
            if self.word_fits(word, entry):
                candidates.append(word)
                if len(candidates) >= max_results:
                    break
        return candidates

    def place_word(self, word, entry):
        """Place a word, return backup for undo."""
        backup = {}
        for i, (r, c) in enumerate(entry["cells"]):
            backup[(r, c)] = self.cells[(r, c)]
            self.cells[(r, c)] = word[i]
        return backup

    def undo_place(self, backup):
        """Undo a word placement."""
        for (r, c), val in backup.items():
            self.cells[(r, c)] = val

    def solve_backtrack(self, entries_to_solve=None, max_depth=None, used_words=None):
        """Backtracking solver. Returns True if solution found."""
        if entries_to_solve is None:
            # Combine all unfilled entries, sorted by constraint (most constrained first)
            entries_to_solve = []
            for num, entry in self.across_entries.items():
                if ("across", num) not in self.filled:
                    entries_to_solve.append(("across", num, entry))
            for num, entry in self.down_entries.items():
                if ("down", num) not in self.filled:
                    entries_to_solve.append(("down", num, entry))

            # Sort by number of candidates (most constrained first = MRV heuristic)
            entries_to_solve.sort(key=lambda x: len(self.get_candidates(x[2])))

        if used_words is None:
            used_words = set()

        if not entries_to_solve:
            return True

        if max_depth is not None and max_depth <= 0:
            return False

        direction, num, entry = entries_to_solve[0]
        remaining = entries_to_solve[1:]
        candidates = self.get_candidates(entry)

        for word in candidates:
            if word in used_words:
                continue
            backup = self.place_word(word, entry)
            used_words.add(word)
            self.filled[(direction, num)] = word

            next_depth = max_depth - 1 if max_depth is not None else None
            if self.solve_backtrack(remaining, next_depth, used_words):
                return True

            self.undo_place(backup)
            used_words.discard(word)
            del self.filled[(direction, num)]

        return False

    def extract_circled_letters(self):
        """Extract letters from circled cells."""
        letters = {}
        for r in range(self.size):
            for c in range(self.size):
                if self.grid_data[r][c] == 2:  # circled
                    cell_ref = f"{chr(65+c)}{r+1}"
                    letter = self.cells.get((r, c))
                    letters[cell_ref] = letter or "?"
        return letters

    def print_grid(self):
        """Print the current grid state."""
        print("   " + " ".join(chr(65+c) for c in range(self.size)))
        for r in range(self.size):
            row_str = f"{r+1:2d} "
            for c in range(self.size):
                if self.grid_data[r][c] == 1:
                    row_str += "# "
                else:
                    letter = self.cells.get((r, c))
                    row_str += f"{letter} " if letter else ". "
            print(row_str)

    def stats(self):
        """Print solver statistics."""
        total_cells = len(self.cells)
        filled_cells = sum(1 for v in self.cells.values() if v is not None)
        total_entries = len(self.across_entries) + len(self.down_entries)
        filled_entries = len(self.filled)

        print(f"Grid: {filled_cells}/{total_cells} cells filled ({100*filled_cells/total_cells:.1f}%)")
        print(f"Entries: {filled_entries}/{total_entries} filled ({100*filled_entries/total_entries:.1f}%)")
        print(f"  Across: {len(self.across_entries)} entries")
        print(f"  Down: {len(self.down_entries)} entries")

        circled = self.extract_circled_letters()
        if circled:
            print(f"\nCircled cells: {circled}")

def main():
    print("=" * 60)
    print("Crossword Solver Engine")
    print("=" * 60)

    puzzle = load_puzzle()
    words = load_dictionary()
    word_bank = build_word_bank(words) if words else {}

    solver = CrosswordSolver(puzzle, word_bank)

    # Place known answers
    placed = solver.place_known_answers()
    if placed:
        print(f"\nPlaced {placed} known answers")

    solver.stats()
    print()

    # Show entry analysis
    print("Entry length distribution:")
    lengths_across = defaultdict(int)
    lengths_down = defaultdict(int)
    for num, entry in solver.across_entries.items():
        lengths_across[entry["length"]] += 1
    for num, entry in solver.down_entries.items():
        lengths_down[entry["length"]] += 1

    all_lengths = sorted(set(lengths_across.keys()) | set(lengths_down.keys()))
    for l in all_lengths:
        a = lengths_across.get(l, 0)
        d = lengths_down.get(l, 0)
        candidates = len(word_bank.get(l, []))
        print(f"  Length {l:2d}: {a:2d} across, {d:2d} down = {a+d:3d} entries ({candidates:6d} dictionary words)")

    # Show most constrained entries (fewest candidates)
    print("\nMost constrained entries (fewest dictionary matches):")
    entry_constraints = []
    for num, entry in solver.across_entries.items():
        n_cands = len(solver.get_candidates(entry, max_results=1000))
        entry_constraints.append((n_cands, "ACROSS", num, entry["length"], entry["start"]))
    for num, entry in solver.down_entries.items():
        n_cands = len(solver.get_candidates(entry, max_results=1000))
        entry_constraints.append((n_cands, "DOWN", num, entry["length"], entry["start"]))

    entry_constraints.sort()
    for n_cands, direction, num, length, start in entry_constraints[:15]:
        print(f"  {direction:6s} #{num:3d} at {start:4s} (len={length:2d}): {n_cands:5d} candidates")

    # Try to solve (with depth limit for safety)
    if "--solve" in sys.argv:
        print("\nAttempting solve with backtracking...")
        max_depth = 10
        if "--depth" in sys.argv:
            idx = sys.argv.index("--depth")
            max_depth = int(sys.argv[idx + 1])
        solved = solver.solve_backtrack(max_depth=max_depth)
        if solved:
            print("SOLVED!")
            solver.print_grid()
        else:
            print(f"No solution found within depth {max_depth}")
            solver.print_grid()

    solver.print_grid()

if __name__ == "__main__":
    main()
