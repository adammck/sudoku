#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


class Cell(object):
    """
    Cells contain either None, or an integer 0-9.
    """


class Column(object):
    """
    Columns contain nine cells.
    """


class Row(object):
    """
    Rows contain nine cells.
    """


class Block(object):
    """
    Blocks contain nine cells.
    """


class Board(object):
    """
    Boards contain nine rows, nine columns, and nine blocks.
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
