#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

import re
import random

COMPLETE = """
123|456|789
456|789|123
789|123|456
---+---+---
234|567|891
567|891|234
891|234|567
---+---+---
345|678|912
678|912|345
912|345|678
"""

# on a completed board, rows and columns within the same block can be
# swapped without invalidating the board. these tuples represent the
# valid swaps, without crossing blocks.
SWAPS = (
    (0,1), (1,2),
    (3,4), (4,5),
    (6,7), (7,8))

def parse_board(tmpl):
    """
    Return a list of cells from a completed board template. Ignore any
    characters other than 0-9, for now.
    """
    chars = re.sub(r'\D', '', tmpl)
    return [int(x) for x in list(chars)]

def render_board(board):
    x = ""

    for row in range(0, 9):
        if (row==3) or (row==6):
            x += "---+---+---\n"

        for col in range(0, 9):
            if (col==3) or (col==6):
                x += "|"

            x += unicode(board[(row*9)+col])

        if row != 8:
            x += "\n"

    return x

def swap_row(board, a, b):
    """
    Swap in place two rows of *board*.
    """

    sa = slice((a*9), (a+1)*9)
    sb = slice((b*9), (b+1)*9)

    board[sa], board[sb] =\
        board[sb], board[sa]

def shuffle_row(board):
    """
    Swap two random rows of *board*, keeping the board valid.
    """

    sw = random.choice(SWAPS)
    swap_row(board, *sw)

def swap_column(board, a, b):
    """
    Swap in place two columns of *board*.
    """

    sa = slice(a, 81+a, 9)
    sb = slice(b, 81+b, 9)

    board[sa], board[sb] =\
        board[sb], board[sa]

def shuffle_column(board):
    """
    Swap two random columns of *board*, keeping the board valid.
    """

    sw = random.choice(SWAPS)
    swap_column(board, *sw)


if __name__ == "__main__":
    board = parse_board(COMPLETE)

    for n in range(999):
        random.choice([
            shuffle_row,
            shuffle_column])(board)

    print render_board(board)
