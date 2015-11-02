from copy import deepcopy
from functools import partial

import primitives


class TurtleSimulator(object):
    directions = ['north', 'east', 'south', 'west']
    dir_row = [-1, 0, 1, 0]
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
        self.matrix = deepcopy(self.base_matrix)
        self.distance = self.find_distance_to_gem()

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
            elif self.matrix[new_row][new_col] == 'box':
                row_after_new = new_row + self.dir_row[self.dir]
                col_after_new = new_col + self.dir_col[self.dir]
                if row_after_new >= 0 and row_after_new < self.rows and \
                        col_after_new >= 0 and col_after_new < self.cols and \
                        self.matrix[row_after_new][col_after_new] == 'empty':
                    self.matrix[row_after_new][col_after_new] = 'box'
                    self.matrix[new_row][new_col] = 'empty'
                    self.row = new_row
                    self.col = new_col

            self.distance = self.find_distance_to_gem()

    def shoot_blaster(self):
        if self.moves < self.max_moves:
            self.moves += 1

            ahead_row = self.row + self.dir_row[self.dir]
            ahead_col = self.col + self.dir_col[self.dir]
            while ahead_row < self.rows and ahead_row >= 0 and ahead_col < self.cols and ahead_col >= 0 and self.matrix[ahead_row][ahead_col] in ['empty', 'ice']:
                if self.matrix[ahead_row][ahead_col] == 'ice':
                    self.matrix[ahead_row][ahead_col] = 'empty'
                    break

                ahead_row = ahead_row + self.dir_row[self.dir]
                ahead_col = ahead_col + self.dir_col[self.dir]

    def gem_ahead(self):
        ahead_row = self.row + self.dir_row[self.dir]
        ahead_col = self.col + self.dir_col[self.dir]
        while ahead_row < self.rows and ahead_row >= 0 and ahead_col < self.cols and ahead_col >= 0:
            if self.matrix[ahead_row][ahead_col] == 'gem':
                return True
            ahead_row = ahead_row + self.dir_row[self.dir]
            ahead_col = ahead_col + self.dir_col[self.dir]
        return False

    def ice_in_sight(self):
        ahead_row = self.row + self.dir_row[self.dir]
        ahead_col = self.col + self.dir_col[self.dir]
        while ahead_row < self.rows and ahead_row >= 0 and ahead_col < self.cols and ahead_col >= 0 and self.matrix[ahead_row][ahead_col] in ['empty', 'ice']:
            if self.matrix[ahead_row][ahead_col] == 'ice':
                return True
            ahead_row = ahead_row + self.dir_row[self.dir]
            ahead_col = ahead_col + self.dir_col[self.dir]
        return False

    def if_gem_ahead(self, out1, out2):
        return partial(primitives.if_then_else, self.gem_ahead, out1, out2)

    def if_ice_in_sight(self, out1, out2):
        return partial(primitives.if_then_else, self.ice_in_sight, out1, out2)

    def blocked_next(self):
        next_row = self.row + self.dir_row[self.dir]
        if next_row >= self.rows or next_row < 0: return True
        next_col = self.col + self.dir_col[self.dir]
        if next_col >= self.cols or next_col < 0: return True
        if self.matrix[next_row][next_col] in ['tower', 'ice']: return True
        if self.matrix[next_row][next_col] == 'box':
            row_after_next = next_row + self.dir_row[self.dir]
            if row_after_next >= self.rows or row_after_next < 0: return True
            col_after_next = next_col + self.dir_col[self.dir]
            if col_after_next >= self.cols or col_after_next < 0: return True
            if self.matrix[row_after_next][col_after_next] != 'empty':
                return True

        return False

    def if_blocked_next(self, out1, out2):
        return partial(primitives.if_then_else, self.blocked_next, out1, out2)

    def if_tower_next(self, out1, out2):
        return partial(primitives.if_then_else, self.tower_next, out1, out2)

    def run(self, routine):
        self._reset()
        while self.moves < self.max_moves and not self.success:
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
                elif col == 'I':
                    self.base_matrix[-1].append('ice')
                elif col == 'B':
                    self.base_matrix[-1].append('box')
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
