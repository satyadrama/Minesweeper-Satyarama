import random

def new_board_dict(size=5, mine_count=5):
    board = Board(size=size, mine_count=mine_count)
    return board.to_dict()


class Board:
    def __init__(self, size=1, mine_count=1):
        self.size = size
        self.mine_count = mine_count

        #TILE PROPERTIES
        self.mines = [[False] * size for _ in range(size)]
        self.flagged = [[False] * size for _ in range(size)]
        self.numbers = [[0] * size for _ in range(size)]
        self.revealed = [[False] * size for _ in range(size)]

        #WIN/LOSE CONDITIONS
        self.game_over = False
        self.won = False

        #METHODS
        self._place_mines()
        self._calculate_numbers()

    def _place_mines(self):
        cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        for r, c in random.sample(cells, self.mine_count):
            self.mines[r][c] = True

    #nentuin angka yang akan ditampil
    def _calculate_numbers(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.mines[r][c]:
                    self.numbers[r][c] = -1
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.size and 0 <= nc < self.size:
                            if self.mines[nr][nc]:
                                count += 1
                self.numbers[r][c] = count

    def to_dict(self):
        return {
            "size": self.size,
            "mine_count": self.mine_count,
            "mines": self.mines,
            "flagged": self.flagged,
            "numbers": self.numbers,
            "revealed": self.revealed,
            "game_over": self.game_over,
            "won": self.won,
        }

    @classmethod
    def from_dict(cls, data):
        board = cls.__new__(cls)  #skip __init__ so we don't re-place mines
        board.size = data["size"]
        board.mine_count = data["mine_count"]
        board.mines = data["mines"]
        board.flagged = data["flagged"]
        board.numbers = data["numbers"]
        board.revealed = data["revealed"]
        board.game_over = data["game_over"]
        board.won = data["won"]
        return board

def toggle_flag(board_dict, r, c):
    board = Board.from_dict(board_dict)
    if board.game_over or board.won:
        return board.to_dict()
    if board.revealed[r][c]:
        return board.to_dict()
    board.flagged[r][c] = not board.flagged[r][c]
    return board.to_dict()

def reveal_cell(board_dict, r, c):
    board = Board.from_dict(board_dict)

    if board.game_over or board.won:
        return board.to_dict()
    if board.revealed[r][c]:
        return board.to_dict()

    if board.flagged[r][c]:
        return board.to_dict()

    if board.mines[r][c]:
        board.revealed[r][c] = True
        board.game_over = True
        return board.to_dict()

    _flood_reveal(board, r, c)

    if _is_won(board):
        board.won = True

    return board.to_dict()


def _flood_reveal(board, r, c):
    """Reveal a cell; if it has 0 adjacent mines, reveal its neighbors too."""
    if not (0 <= r < board.size and 0 <= c < board.size):
        return
    if board.revealed[r][c]:
        return
    if board.mines[r][c]:
        return

    board.revealed[r][c] = True

    if board.numbers[r][c] == 0:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                _flood_reveal(board, r + dr, c + dc)


def _is_won(board):
    for r in range(board.size):
        for c in range(board.size):
            if not board.mines[r][c] and not board.revealed[r][c]:
                return False
    return True