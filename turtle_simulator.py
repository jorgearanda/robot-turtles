from copy import deepcopy
from functools import partial

import primitives


class TurtleSimulator(object):
    directions = ['north', 'east', 'south', 'west']
    dir_row = [1, 0, -1, 0]
    dir_col = [0, 1, 0, -1]

    def __init__(self, max_moves):
        self.max_moves = max_moves
        self.moves = 0
        self.success = False
        self.routine = None

    def _reset(self):
        self.row = self.row_start
        self.col = self.col_start
        self.dir = 1
        self.moves = 0
        self.success = False
        self.matrix = deepcopy(self.matrix)

    @property
    def position(self):
        return (self.row, self.col, self.directions[self.dir])

    def find_distance_to_gem(self):
        return abs(self.row - self.gem_row) + abs(self.col - self.gem_col)

    def turn_left(self):
        if self.moves < self.max_moves:
            self.moves += 1
            self.dir = (self.dir - 1) % 4

    def turn_right(self):
        if self.moves < self.max_moves:
            self.moves += 1
            self.dir = (self.dir + 1) % 4

    def move_forward(self):
        if self.moves < self.max_moves:
            self.moves += 1

            new_row = self.row + self.dir_row[self.dir]
            if new_row < 0:
                new_row = 0
            if new_row >= self.rows:
                new_row = self.rows - 1

            new_col = self.col + self.dir_col[self.dir]
            if new_col < 0:
                new_col = 0
            if new_col >= self.cols:
                new_col = self.cols - 1

            if self.matrix[new_row][new_col] in ['empty', 'gem']:
                self.row = new_row
                self.col = new_col
                if self.matrix[self.row][self.col] == 'gem':
                    self.success = True
                self.distance = self.find_distance_to_gem()

    def gem_ahead(self):
        ahead_row = self.row + self.dir_row[self.dir]
        ahead_col = self.col + self.dir_col[self.dir]
        while ahead_row < self.rows and ahead_row >= 0 and ahead_col < self.cols and ahead_col >= 0:
            if self.matrix[ahead_row][ahead_col] == 'gem':
                return True
            ahead_row = ahead_row + self.dir_row[self.dir]
            ahead_col = ahead_col + self.dir_col[self.dir]
        return False

    def if_gem_ahead(self, out1, out2):
        return partial(primitives.if_then_else, self.gem_ahead, out1, out2)

    def tower_next(self):
        next_row = self.row + self.dir_row[self.dir]
        next_col = self.col + self.dir_col[self.dir]
        return next_row >= self.rows or next_row < 0 or next_col >= self.cols or next_col < 0 or self.matrix[next_row][next_col] == 'tower'

    def if_tower_next(self, out1, out2):
        return partial(primitives.if_then_else, self.tower_next, out1, out2)

    def run(self, routine):
        self._reset()
        while self.moves < self.max_moves:
            routine()

    def parse_matrix(self, matrix):
        self.base_matrix = list()
        for i, line in enumerate(matrix):
            self.base_matrix.append(list())
            for j, col in enumerate(line):
                if col == 'G':
                    self.base_matrix[-1].append('gem')
                    self.gem_row = i
                    self.gem_col = j
                elif col == 'T':
                    self.base_matrix[-1].append('tower')
                elif col == '.':
                    self.base_matrix[-1].append('empty')
                elif col == 'S':
                    self.base_matrix[-1].append('empty')
                    self.row_start = self.row = i
                    self.col_start = self.col = j
                    self.dir = 1
        self.rows = len(self.base_matrix)
        self.cols = len(self.base_matrix[0])
        self.matrix = deepcopy(self.base_matrix)
