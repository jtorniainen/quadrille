import curses
import time


class ChessBoard(object):
    def __init__(self, scr):
        self.scr = scr
        self.width = 4
        self.height = 4
        self.start_x = 1
        self.start_y = 1

    def draw_board(self):
        for x in range(self.width):
            for y in range(self.height):
                self.scr.addstr(self.start_y + y, self.start_x + x, '*')


def main(scr):
    board = ChessBoard(scr)
    while True:
        scr.clear()
        scr.border(0)
        board.draw_board()
        time.sleep(.5)
        scr.refresh()

if __name__ == '__main__':
    curses.wrapper(main)
    main()
