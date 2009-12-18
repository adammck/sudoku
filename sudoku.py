#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4


import re


INCOMPLETE = """
123   789
456   123
789   456
234567891
   891   
891234567
345   912
678   345
912   678
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

    def next_move(self):
        """
        >>> b = Board.parse(INCOMPLETE)
        >>> b.next_move()
        [(0, 4, 5), (1, 4, 6), (2, 4, 7), (6, 4, 2), (7, 4, 3), (8, 4, 4)]
        """

        x = set(range(1, 10))
        moves = []

        for row in range(0, 9):
            for col in range(0, 9):

                # ignore this cell if it's already filled
                i = self._index(col, row)
                if self.data[i] is not None:
                    continue

                row_values = set(self._row(row))
                col_values = set(self._column(col))
                bck_values = set(self._block(col, row))

                missing = x.difference(row_values, col_values, bck_values)

                if len(missing) == 1:
                    moves.append((col, row, missing.pop()))

        return moves


    def _index(self, x, y):
        return (y*9)+x

    def _row(self, y):
        i = self._index(0, y)
        return self.data[i:i+9]

    def _column(self, x):
        cells = [self._index(x, y) for y in range(0, 9)]
        return [self.data[index] for index in cells]

    def _block(self, x, y):
        """
        >>> Board.parse(COMPLETE)._block(0, 0)
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
        >>> Board.parse(COMPLETE)._block(8, 8)
        [9, 1, 2, 3, 4, 5, 6, 7, 8]
        """

        cells = []

        ix = x - (x%3)
        iy = y - (y%3)

        for y in range(iy, iy+3):
            for x in range(ix, ix+3):
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

    def _complete(self, data):
        return sorted(data) == range(1, 10)

    def is_row_complete(self, y):
        return self._complete(self._row(y))

    def is_column_complete(self, x):
        return self._complete(self._column(x))

    def is_block_complete(self, n):
        """
        Return True if block *n* is completed. This doesn't necessarily
        mean that it is correct, since the other blocks could be wrong.
        
        >>> b = Board.parse(COMPLETE)
        >>> b.is_block_complete(0)
        True
        """

        return self._complete(self._block(n))

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
