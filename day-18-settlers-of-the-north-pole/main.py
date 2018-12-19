from collections import Counter
from itertools import product

area = """..|..|.|.|.||..#.#|...|..#.|.........|.......|..#.
#.|.........|||....#....|....##||.....|.|.........
..||......#.#||#.#.......#..#.#.###...|.#..#...#..
|....#....|.##.##.....##...##|..|....|..|#||...###
#|...|.#|..|......#.##....#|....|...|#......|.#|.|
..|....##.##.#..||##...#..##|......|...|#.||.#.#..
.#...#||...........#|.....|##....#.#...|#.|###..|.
||....#.#.|...||...###|.|#.....#.|#.|#...#.#.|...#
...#.....||.......#....#|###|####..|#|.###..||.#.#
|#|...||..##.||.||..#.#.|..#...#..|........#..|#..
#....||.|.....|.|.#|.##.|..|.#.....|..|.....#|.|..
|..||#........|#.|..|.|...#..#....#.|.....||#.#...
..|...||.|##||##..|...#|.....|#.|....#....||#.##..
#|..#|..||...|..|.|#|..##.#.......#|#....#||...#..
|#|.|...|..##...|.#||#..#...#....||.#.|...##..|..#
|..||.#.#..|....#...#.#..#..#...||.|.#.#.#.....#|.
.|##.####..||.#.|#.###....#...#.|..#.#.##.|..##..#
#|.......#......|.#..|.....||.|.#||#.#.##.#|....|.
.|..#.|#.##|....#......|.#||..|#..##.|..#......###
..###....#.||.#..|##.##..#|.#...|#|...#.|.|...#|#.
........||......|##||##..###|..|.##.#..#|##...|..#
.#....|....|...##.#.||##.....#|...|#.#||...#.....|
#...#|...###.|.|..|..#.|###.|.#.|.####|...|.#..|#.
...#..|.....|.#.##.|.#.#..|..##.##.#..|...#...|#..
..###.#|##|#.#.......|.|...||###|.#.........#..|..
..|#...||.#.#..|...|..#||...|.#.#......#...|..#...
.||..........|.#....|.||...|#.|.|||..||........|#.
#.##.#||..|.|#...|..#|.|#......|.||.......|...|#..
#.||.||#...#|||.....|.|.|.|...||.#..#.#.#|..|||.|.
.#...#...||||#...##.#.#......#|......#.|.....|#||.
.#|.###|#||.|#...#.|..|.|#.|#..#..#...|.|.|...|.|.
..#|.|#|..##|.||.|.....|#...#..|.|#....|.|..|..|#.
#....|..#.#.......#||..#....|.|..#.#|..#...|#.#.|.
#.#.|..|...#|.###||.#.....#|#|#.##..|.|#|....|....
....|#.#.||..|..#...|...|..|...|..#..#......#|.#..
..#..#|.|.|#.#.|.|.#.#.....#..|..#..|.......||#|#.
#|......|#..|.#...##|....|..|#||..|..||...||.#....
#..|#.......||.....|.||||#.|#.|....#|#....|#.#....
#.##.#.#..||......#...|......|#|...|.||.#.|..|....
####.|...||##|#|.......|||.#.#.....#...##.#|..#...
..|..|||..|.||#|#.|..#.|..#.|........###......#..|
..#|.....|||||#..||.....##..#...|||.....#......#.#
.#.|.||#.##.......||.#.||..#...|##..|.#.#...|...|.
.##........|..||.|.#|.|.||||..#...#..|..|#|#..|#|.
.#.#.....#|||..|...#.|...|...#.||..||###|.#|......
|.|#..#.#.|||||.#|.|......#.|#.||.....#..#...|#.|.
...|....#.###|.#.##......|#.##.....#.|.##.#......#
.#.#.....|..#.##..#|#|..#.#|##..##|..##.#..#....||
..#.#.|.....#.|..#.|.|#...|....#...|..|.|..#||...|
|.||.|...|...|##..||....|#.|..#..##....|#.#|##..|.
""".splitlines()

OPEN = '.'
TREES = '|'
LUMBERYARD = '#'

CHANGES = {
    OPEN: lambda adjacent: TREES if adjacent.count(TREES) >= 3 else OPEN,
    TREES: lambda adjacent: LUMBERYARD if adjacent.count(LUMBERYARD) >= 3 else TREES,
    LUMBERYARD: lambda adjacent: LUMBERYARD if adjacent.count(LUMBERYARD) >= 1 and adjacent.count(TREES) >= 1 else OPEN,
}

def adjacent_acres(area, x, y):
    for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
        if (dx, dy) != (0, 0) and y + dy >= 0 and y + dy < len(area) and x + dx >= 0 and x + dx < len(area[y + dy]):
            yield area[y + dy][x + dx]

def apply_changes(area):
    new_area = []
    for y, row in enumerate(area):
        new_row = ""
        for x, acre in enumerate(row):
            new_row += CHANGES[acre](list(adjacent_acres(area, x, y)))
        new_area.append(new_row)
    return new_area

def calculate_resource_value(area):
    cnt = Counter(acre for row in area for acre in row)
    return cnt[TREES] * cnt[LUMBERYARD]

def detect_change_cycle(area):
    cycle = []
    while True:
        area = apply_changes(area)
        value = calculate_resource_value(area)
        if value in cycle:
            return cycle
        cycle.append(value)

for i in range(10):
    area = apply_changes(area)

print('Total resource value after 10 minutes:', calculate_resource_value(area))

for i in range(490):
    area = apply_changes(area)

cycle = detect_change_cycle(area)
print('Total resource value after 1 billion minutes:', cycle[(1_000_000_000 - 500) % len(cycle) - 1])