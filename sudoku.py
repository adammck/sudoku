#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import re


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

    def __unicode__(self):
        return unicode(self.value) if (self.value is not None) else " "


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

TMPL = """
 2 | 3 | 4 
   |   |   
   |   |   
---+---+---
   |   |   
   |   |   
   |   |   
---+---+---
   |   |   
   |   |   
   |   |   
"""

COMPLETE = """
123456789
456789123
789123456
234567891
567891234
891234567
345678912
678912345
912345678
"""

class Board(object):
    """
    Boards contain nine rows, nine columns, and nine blocks.

    >>> Board.parse(TMPL)
     2 | 3 | 4 
       |   |   
       |   |   
    ---+---+---
       |   |   
       |   |   
       |   |   
    ---+---+---
       |   |   
       |   |   
       |   |   

    >>> Board.parse(TMPL).is_row_valid(0)
    True

    >>> Board.parse(TMPL).is_row_complete(0)
    False

    >>> b = Board()
    >>> b[1,1] = 1
    >>> b[4,4] = 2
    >>> b[7,7] = 3
    >>> b
       |   |   
     1 |   |   
       |   |   
    ---+---+---
       |   |   
       | 2 |   
       |   |   
    ---+---+---
       |   |   
       |   | 3 
       |   |   
    """

    NUM_CELLS = 81
    BLOCK_MAP = {
        0: (0, 0),
        1: (3, 0),
        2: (6, 0),
        3: (0, 3),
        4: (3, 3),
        5: (6, 3),
        6: (0, 6),
        7: (3, 6),
        8: (6, 6),
    }

    def __init__(self, data=None):
        self.data = data if (data is not None) else\
            [None for x in range(0, self.NUM_CELLS)]

    @classmethod
    def parse(cls, tmpl):
        return cls([
            None if (x==" ") else int(x)
            for x in list(re.sub(r'[^0-9 ]', '', tmpl))])

    def _index(self, x, y):
        return (y*9)+x

    def _row(self, y):
        i = self._index(0, y)
        return self.data[i:9]

    def _column(self, x):
        cells = [self._index(x, y) for y in range(0, 9)]
        return [self.data[i] for index in cells]

    def _block(self, n):
        """
        >>> Board.parse(COMPLETE)._block(0)
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        >>> Board.parse(COMPLETE)._block(8)
        [9, 1, 2, 3, 4, 5, 6, 7, 8]
        """

        cells = []
        
        pos = self.BLOCK_MAP[n]
        for y in range(pos[1], pos[1]+3):
            for x in range(pos[0], pos[0]+3):
                i = self._index(x, y)
                cells.append(self.data[i])

        return cells

    def __getitem__(self, pos):
        i = self._index(*pos)
        return self.data[i]

    def __setitem__(self, pos, value):
        i = self._index(*pos)
        self.data[i] = value

    def is_row_valid(self, row):
        seen = []

        for cell in self._row(row):
            if cell is not None:
                if cell not in seen:
                    seen.append(cell)

                else:
                    return False

        return True

    def is_row_complete(self, y):
        return sorted(self._row(y)) == range(1, 9)

    def is_column_complete(self, x):
        return sorted(self._column(x)) == range(1, 9)

    def is_block_complete(self, n):
        """
        Return True if block *n* is completed.
        
        >>> b = Board.parse(COMPLETE)
        >>> b.is_block_complete(0)
        True
        """

        return sorted(self._block(n)) == range(1, 9)

    def __repr__(self):
        x = ""

        for row in range(0, 9):
            if (row==3) or (row==6):
                x += "---+---+---\n"

            for col in range(0, 9):
                if (col==3) or (col==6):
                    x += "|"

                d = self[col, row]
                x += unicode(d) if d is not None else " "

            if row != 8:
                x += "\n"

        return x


if __name__ == "__main__":
    import doctest
    doctest.testmod()
