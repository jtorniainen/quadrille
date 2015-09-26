#!/usr/env python3

# Jari Torniainen 2015
# MIT License (see LICENSE for details)

import curses
import time
import random


def move_queen(own_position, free_position):
    x = own_position[0]
    y = own_position[1]
    possible_positions = [(x + 1, y),
                          (x - 1, y),
                          (x, y + 1),
                          (x, y - 1),
                          (x + 1, y + 1),
                          (x + 1, y - 1),
                          (x - 1, y + 1),
                          (x - 1, y - 1)]
    if free_position in possible_positions:
        return True
    else:
        return False


def move_king(own_position, free_position):
    x = own_position[0]
    y = own_position[1]
    possible_positions = [(x + 1, y),
                          (x - 1, y),
                          (x, y + 1),
                          (x, y - 1)]
    if free_position in possible_positions:
        return True
    else:
        return False


def move_rook(own_position, free_position):
    x = own_position[0]
    y = own_position[1]
    possible_positions = [(x + 1, y),
                          (x - 1, y),
                          (x, y + 1),
                          (x, y - 1)]
    if free_position in possible_positions:
        return True
    else:
        return False


def move_bishop(own_position, free_position):
    x = own_position[0]
    y = own_position[1]

    possible_positions = [(x + 1, y + 1),
                          (x + 1, y - 1),
                          (x - 1, y + 1),
                          (x - 1, y - 1)]
    if free_position in possible_positions:
        return True
    else:
        return False


def move_knight(own_position, free_position):
    x = own_position[0]
    y = own_position[1]

    possible_positions = [(x + 1, y - 2), (x - 1, y - 2),  # UP
                          (x + 1, y + 2), (x - 1, y + 2),  # DOWN
                          (x - 2, y + 1), (x - 2, y - 1),  # LEFT
                          (x + 2, y - 1), (x + 2, y + 1)]  # RIGHT
    if free_position in possible_positions:
        return True
    else:
        return False


class Piece(object):
    """ Container class for pieces (location, symbol, etc) """

    def __init__(self, scr, location, symbol, move_function,
                 is_target=False):
        self.scr = scr
        self.x = location[0]
        self.y = location[1]
        self.location = location
        self.symbol = symbol
        self.move_function = move_function
        self.is_target = is_target

    def move(self, free_position):
        return self.move_function(self.location, free_position)


class ChessBoard(object):

    def __init__(self, scr):
        self.scr = scr
        self.width = 4
        self.height = 4
        self.offset_x = 1
        self.offset_y = 1

        self.pieces = []
        self.reset()

    def setup(self):
        locations = []
        self.pieces = []
        for x in range(self.width):
            for y in range(self.height):
                locations.append((x, y))
        random.shuffle(locations)
        self.target_location = locations[0]
        self.pieces.append(Piece(self.scr, locations[0], 'Q', move_queen, True))
        self.pieces.append(Piece(self.scr, locations[1], 'K', move_king))
        self.pieces.append(Piece(self.scr, locations[2], 'K', move_king))
        self.pieces.append(Piece(self.scr, locations[3], 'r', move_rook))
        self.pieces.append(Piece(self.scr, locations[4], 'r', move_rook))
        self.pieces.append(Piece(self.scr, locations[5], 'r', move_rook))
        self.pieces.append(Piece(self.scr, locations[6], 'r', move_rook))
        self.pieces.append(Piece(self.scr, locations[7], 'k', move_knight))
        self.pieces.append(Piece(self.scr, locations[8], 'k', move_knight))
        self.pieces.append(Piece(self.scr, locations[9], 'k', move_knight))
        self.pieces.append(Piece(self.scr, locations[10], 'k', move_knight))
        self.pieces.append(Piece(self.scr, locations[11], 'b', move_bishop))
        self.pieces.append(Piece(self.scr, locations[12], 'b', move_bishop))
        self.pieces.append(Piece(self.scr, locations[13], 'b', move_bishop))
        self.pieces.append(Piece(self.scr, locations[14], 'b', move_bishop))

        self.free_space = locations[15]

    def check_for_victory(self):
        if self.target_location == self.goal_location:
            return True
        else:
            return False

    def move(self, move):
        # TODO: make it easier to lookup piece locations, some kind of table?
        for idx, piece in enumerate(self.pieces):
            if move == piece.location:
                break
        is_valid_move = self.pieces[idx].move(self.free_space)

        if is_valid_move:
            old_free_space = self.free_space
            self.free_space = self.pieces[idx].location
            self.pieces[idx].location = old_free_space
            if piece.is_target:
                self.target_location = self.pieces[idx].location

    def reset(self):
        self.free_space = (0, 0)
        self.goal_location = random.choice([(0, 0), (0, 3), (3, 0), (3, 3)])
        self.target_location = (1, 1)

        self.setup()
        # Need to make sure game does not start from winning condition
        while self.target_location == self.goal_location:
            self.setup()


def popup(scr, message_string):
    scr.clear()
    scr.border(0)
    scr.addstr(1, 1, message_string)
    scr.refresh()
    scr.getch()


def draw_board(scr, board):
    columns = ['a', 'b', 'c', 'd']
    for idx, column_name in enumerate(columns):
        scr.addstr(0, idx + board.offset_x + 1, column_name, curses.color_pair(4))
        scr.addstr(board.offset_y + 2 + board.height, idx + board.offset_x + 1, column_name, curses.color_pair(4))
    for idx in range(board.height):
        scr.addstr(idx + board.offset_y + 1, 0, str(idx), curses.color_pair(4))
        scr.addstr(idx + board.offset_y + 1, board.offset_x + 2 + board.height, str(idx), curses.color_pair(4))
    for piece in board.pieces:
        if piece.is_target:
            color = curses.color_pair(1)
        elif piece.location == board.goal_location:
            color = curses.color_pair(2)
        else:
            color = curses.color_pair(3)

        scr.addstr(
            board.offset_y + 1 +
            piece.location[1],
            board.offset_x + 1 +
            piece.location[0],
            piece.symbol,
            color)

    if board.free_space == board.goal_location:
        scr.addstr(board.offset_y  + 1 +board.free_space[1],
                   board.offset_x + 1 + board.free_space[0],
                   ' ', curses.color_pair(2))


def parse_move(move):
    if len(move) != 2:
        return False
    else:
        column = move[0]
        row = move[1]

        if column == 'a':
            column = 0
        elif column == 'b':
            column = 1
        elif column == 'c':
            column = 2
        elif column == 'd':
            column = 3
        else:
            return False

        row = int(row)
        if row < 0 or row > 3:
            return False

    return column, row


def main(scr):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    board = ChessBoard(scr)
    curses.echo()

    running = True
    while running:
        scr.clear()
        draw_board(scr, board)
        time.sleep(.5)
        scr.addstr(8, 0, '>')
        if board.check_for_victory():
            time.sleep(.5)
            popup(scr, 'YOU ARE VICTORY!')
            board.reset()
        else:
            move_str = scr.getstr(8, 1, 2).decode(encoding='utf-8')
            move = parse_move(move_str)
            if move:
                board.move(move)
            else:
                popup(scr, 'Invalid move!')

        scr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
