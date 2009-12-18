#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


class Cell(object):
    """
    Cells contain either None, or an integer 0-9.

    >>> Cell(None)
    <Cell:?>

    >>> Cell(5)
    <Cell:5>

    Attempting to store anything else results in a ValueError.

    >>> Cell(99)
    Traceback (most recent call last):
    ...
    ValueError: Invalid value: 99
    """

    def __init__(self, value=None):
        if (value is None) or ((type(value) is int) and (0 <= value <= 9)):
            self.value = value

        else:
            raise ValueError(
                "Invalid value: %r" % value)

    def __repr__(self):
        return ("<Cell:%s>" %
            (self.value if (self.value is not None) else "?"))


class Column(object):
    """
    Columns contain nine Cells. Each Cell has a vertical index between
    0 (at the top) and 8 (at the bottom).

    >>> Column().cells
    [None, None, None, None, None, None, None, None, None]

    >>> col = Column()
    >>> col[0] = True
    >>> col[8] = False
    >>> col.cells
    [True, None, None, None, None, None, None, None, False]
    """

    def __init__(self):
        self.cells = [None for x in range(0, 9)]

    def __getitem__(self, index):
        return self.cells[index]

    def __setitem__(self, index, value):
        self.cells[index] = value


class Row(object):
    """
    Rows contain nine Cells. Each Cell has a horizontal index between 0
    (at the top) and 8 (at the bottom).
    """

    def __init__(self):
        self.cells = [None for x in range(0, 9)]

    def __getitem__(self, index):
        return self.cells[index]

    def __setitem__(self, index, value):
        self.cells[index] = value


class Block(object):
    """
    Blocks contain nine cells. Each cell has a horizontal and vertical
    index between 0,0 (top left) and 2,2 (bottom right).

    >>> Block().cells
    [None, None, None, None, None, None, None, None, None]

    >>> b = Block()
    >>> b[0,0] = True
    >>> b[2,2] = False
    >>> b.cells
    [True, None, None, None, None, None, None, None, False]
    """

    def __init__(self):
        self.cells = [None for x in range(0, 9)]

    def _index(self, x, y):
        return (x*3)+y

    def __getitem__(self, pos):
        return self.cells[self._index(*pos)]

    def __setitem__(self, pos, value):
        self.cells[self._index(*pos)] = value


class Board(object):
    """
    Boards contain nine rows, nine columns, and nine blocks.
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod()
