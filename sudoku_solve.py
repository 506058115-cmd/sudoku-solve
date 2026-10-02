#!/usr/bin/env python3
"""Solve a classic 9x9 Sudoku and report whether the solution is unique."""

import argparse
import sys


FULL = (1 << 9) - 1


class PuzzleError(ValueError):
    pass


def prepare(text):
    puzzle = "".join(text.split())
    if len(puzzle) != 81 or any(char not in "0123456789." for char in puzzle):
        raise PuzzleError("puzzle must contain exactly 81 digits, dots, or zeros")

    grid = [0] * 81
    rows = [0] * 9
    columns = [0] * 9
    boxes = [0] * 9
    for index, char in enumerate(puzzle):
        if char in "0.":
            continue
        row, column = divmod(index, 9)
        box = (row // 3) * 3 + column // 3
        bit = 1 << (int(char) - 1)
        if rows[row] & bit or columns[column] & bit or boxes[box] & bit:
            raise PuzzleError("given digits violate a row, column, or box rule")
        grid[index] = int(char)
        rows[row] |= bit
        columns[column] |= bit
        boxes[box] |= bit
    return grid, rows, columns, boxes


def solve(grid, rows, columns, boxes):
    solutions = 0
    first_solution = None

    def search():
        nonlocal solutions, first_solution
        if solutions >= 2:
            return

        best_index = -1
        best_candidates = 0
        fewest = 10
        for index, value in enumerate(grid):
            if value:
                continue
            row, column = divmod(index, 9)
            box = (row // 3) * 3 + column // 3
            candidates = FULL & ~(rows[row] | columns[column] | boxes[box])
            count = candidates.bit_count()
            if count < fewest:
                best_index, best_candidates, fewest = index, candidates, count
                if count <= 1:
                    break
        if best_index < 0:
            solutions += 1
            if first_solution is None:
                first_solution = grid.copy()
            return
        if not best_candidates:
            return

        row, column = divmod(best_index, 9)
        box = (row // 3) * 3 + column // 3
        while best_candidates and solutions < 2:
            bit = best_candidates & -best_candidates
            best_candidates ^= bit
            value = bit.bit_length()
            grid[best_index] = value
            rows[row] |= bit
            columns[column] |= bit
            boxes[box] |= bit
            search()
            grid[best_index] = 0
            rows[row] ^= bit
            columns[column] ^= bit
            boxes[box] ^= bit

    search()
    return solutions, first_solution


def format_grid(grid):
    lines = ["+-------+-------+-------+"]
    for row in range(9):
        values = [str(value) for value in grid[row * 9 : row * 9 + 9]]
        lines.append("| " + " ".join(values[:3]) + " | " + " ".join(values[3:6]) + " | " + " ".join(values[6:]) + " |")
        if row % 3 == 2:
            lines.append("+-------+-------+-------+")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Solve a 9x9 Sudoku from an 81-cell digit string.")
    parser.add_argument("puzzle", help="81 digits; use 0 or . for empty cells (whitespace is ignored)")
    args = parser.parse_args()
    try:
        grid, rows, columns, boxes = prepare(args.puzzle)
    except PuzzleError as error:
        print(f"sudoku-solve: {error}", file=sys.stderr)
        return 2

    count, solution = solve(grid, rows, columns, boxes)
    if solution is None:
        print("No solution.")
        return 1
    print("Solution: unique" if count == 1 else "Solution: multiple (at least two)")
    print(format_grid(solution))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
