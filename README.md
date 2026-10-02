# sudoku-solve

Solve a classic 9×9 Sudoku and distinguish a unique solution from a puzzle with multiple solutions.

## Use

Requires Python 3.10+; no packages to install.

```sh
python sudoku_solve.py 530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

Pass exactly 81 digits. Use `0` or `.` for empty cells; whitespace is ignored. Contradictory givens are rejected. The solver stops after finding two solutions, reports no solution, a unique solution, or at least two solutions, and prints the first valid grid.

## License

MIT
