#!/usr/bin/env python3
from random import randrange

ROW_COUNT=9
COLUMN_COUNT=10
TARGET_COVERAGE=0.75
SIMULATION_COUNT=100000
MONTH_DAYS=30
DAY_CELLS=5


def simulate_month(grid, count=MONTH_DAYS):
    for i in range(count):
        simulate_day(grid)


def simulate_day(grid, count=DAY_CELLS):
    for i in range(count):
        row_num = randrange(len(grid))
        col_num = randrange(len(grid[0]))
        grid[row_num][col_num] += 1


def update_meta_grid(meta, local):
    for row in range(len(local)):
        for col in range(len(local[row])):
            if local[row][col] != 0:
                meta[row][col] += 1


def print_2d(grid):
    print('[')
    for row in grid:
        print("%s%s" % (" ", row))
    print(']')


def calculate_cell_probability(meta_grid, count):
    results = list(meta_grid)
    for row in range(len(meta_grid)):
        for col in range(len(meta_grid[row])):
            results[row][col] = meta_grid[row][col] / count
    return results


def get_empty_grid(rows, columns):
    return [[0 for j in range(COLUMN_COUNT)] for i in range(ROW_COUNT)]


def coverage(grid):
    total_cells = len(grid) * len(grid[0])
    covered_cells = 0
    for row in grid:
        for cell in row:
            if cell > 0:
                covered_cells += 1
    return covered_cells / total_cells


def main(count=SIMULATION_COUNT):
    meta_grid = get_empty_grid(ROW_COUNT, COLUMN_COUNT)
    print("Beginning %d simulations\n" % count)

    # Run simulations
    cell_coverage = []
    for i in range(count):
        local_grid = get_empty_grid(ROW_COUNT, COLUMN_COUNT)
        simulate_month(local_grid)
        update_meta_grid(meta_grid, local_grid)
        cell_coverage.append(coverage(local_grid))

    print("Completed %d simulations of %d daily characters across %d days\n" % (
        count, DAY_CELLS, MONTH_DAYS
    ))

    print("-------- Cell absolute hit counts ---------")
    print_2d(meta_grid)
    print()

    print("-------- Cell hit probabilities ---------")
    print_2d(calculate_cell_probability(meta_grid, count))
    print()

    print("-------- Probability of finding 75%% of squares ---------")
    covered_total = sum([1 for cover_pct in cell_coverage if cover_pct >= TARGET_COVERAGE])
    print("%d of %d (%0.2f%%) simulations covered %0.0f%%" % (
        covered_total,
        count,
        covered_total / count * 100,
        TARGET_COVERAGE * 100
    ))


if __name__ == '__main__':
    main()
