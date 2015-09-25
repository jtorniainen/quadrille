import curses
import time
import random


def popup(scr, message_string):
    scr.clear()
    scr.border(0)
    scr.addstr(1, 1, message_string)
    scr.refresh()
    scr.getch()


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
    def __init__(self, scr, location, symbol, move_function,
                 is_target=False):
        self.scr = scr
        self.x = location[0]
        self.y = location[1]
        self.location = location
        self.symbol = symbol
        self.move_function = move_function
        self.is_target = is_target

    def draw(self, goal_location, offset_x=0, offset_y=0):
        if self.is_target:
            self.scr.addstr(self.location[1] + offset_y,
                            self.location[0] + offset_x,
                            self.symbol,
                            curses.color_pair(1))

        elif self.location == goal_location:
            self.scr.addstr(self.location[1] + offset_y,
                            self.location[0] + offset_x,
                            self.symbol,
                            curses.color_pair(2))

        else:
            self.scr.addstr(self.location[1] + offset_y,
                            self.location[0] + offset_x,
                            self.symbol,
                            curses.color_pair(3))

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
        self.free_space = (0, 0)
        self.goal_location = random.choice([(0, 0), (0, 3), (3, 0), (3, 3)])
        self.target_location = (1, 1)

        self.setup()
        # Need to make sure game does not start from winning condition
        while self.target_location == self.goal_location:
            self.setup()

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

    def draw_board(self):
        columns = ['a', 'b', 'c', 'd']
        for idx, column_name in enumerate(columns):
            self.scr.addstr(0, idx + self.offset_x, column_name, curses.color_pair(4))
        for idx in range(self.height):
            self.scr.addstr(idx + self.offset_y, 0, str(idx), curses.color_pair(4))
        for piece in self.pieces:
            piece.draw(self.goal_location, offset_x=1, offset_y=1)

        if self.free_space == self.goal_location:
            self.scr.addstr(self.offset_y + self.free_space[1], self.offset_x + self.free_space[0], ' ', curses.color_pair(2))

    def move(self, move):
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

    def move2(self, move):
        for idx, piece in enumerate(self.pieces):
            if move == piece.location:
                break
        is_valid_move = piece.move(self.free_space)

        if is_valid_move:
            old_free_space = self.free_space
            self.free_space = piece.location
            piece = old_free_space


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
        board.draw_board()
        time.sleep(.5)
        scr.addstr(5, 0, '>')
        if board.check_for_victory():
            time.sleep(2)
            popup(scr, 'YOU ARE VICTORY!')
            running = False
        else:
            move_str = scr.getstr(5, 1, 2).decode(encoding='utf-8')
            move = parse_move(move_str)
            if move:
                board.move(move)
            else:
                popup(scr, 'Invalid move!')

        scr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
