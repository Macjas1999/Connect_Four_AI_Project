REWARD_ONE = 1
REWARD_TWO = 4
REWARD_THREE = 16
RWARD_WIN = 192
REWARD_WIN = RWARD_WIN

WINDOW_BASE = {
    0: 0,
    1: 5,
    2: 35,
    3: 250,
    4: REWARD_WIN,
}

CENTER_WEIGHTS = [3, 4, 5, 7, 5, 4, 3]
OPEN_THREE_BONUS = 120
NON_PLAYABLE_MULTIPLIER = 0.35
DOUBLE_THREAT_BONUS = 80


class AnalyzeLayout:
    def __init__(self):
        self.playerONEscore = 0
        self.playerTWOscore = 0

    def analyzeBoard(self, board):
        self.playerONEscore = 0
        self.playerTWOscore = 0

        for window in self._all_windows(board):
            self._evaluate_window(board, window)

        self._add_center_control(board)
        self._add_threat_density(board)
        self.check_draw(board)

    def reset_analyzer(self):
        self.playerONEscore = 0
        self.playerTWOscore = 0

    def _all_windows(self, board):
        windows = []
        for row in range(6):
            for col in range(4):
                windows.append([(row, col + d) for d in range(4)])
        for row in range(3):
            for col in range(7):
                windows.append([(row + d, col) for d in range(4)])
        for row in range(3):
            for col in range(4):
                windows.append([(row + d, col + d) for d in range(4)])
        for row in range(3, 6):
            for col in range(4):
                windows.append([(row - d, col + d) for d in range(4)])
        return windows

    def _evaluate_window(self, board, window):
        count_one = 0
        count_two = 0
        empty_cells = []

        for row, col in window:
            value = board[row][col]
            if value == 1:
                count_one += 1
            elif value == 2:
                count_two += 1
            else:
                empty_cells.append((row, col))

        if count_one > 0 and count_two > 0:
            return

        base_score = WINDOW_BASE[count_one or count_two]
        if base_score == 0:
            return

        multiplier = self._window_playable_multiplier(board, empty_cells)
        center_factor = 1 + self._window_center_factor(window)
        window_score = int(base_score * multiplier * center_factor)

        if count_one == 3 and self._window_has_playable_empty(board, empty_cells):
            window_score += OPEN_THREE_BONUS
        if count_two == 3 and self._window_has_playable_empty(board, empty_cells):
            window_score += OPEN_THREE_BONUS

        if count_one > 0:
            self.playerONEscore += window_score
        elif count_two > 0:
            self.playerTWOscore += window_score

    def _window_center_factor(self, window):
        return sum(CENTER_WEIGHTS[col] for _, col in window) / 28.0

    def _window_has_playable_empty(self, board, empty_cells):
        for row, col in empty_cells:
            if row == 5 or board[row + 1][col] != 0:
                return True
        return False

    def _window_playable_multiplier(self, board, empty_cells):
        if not empty_cells:
            return 1.0
        return 1.0 if self._window_has_playable_empty(board, empty_cells) else NON_PLAYABLE_MULTIPLIER

    def _add_center_control(self, board):
        for row in range(6):
            for col in range(7):
                value = board[row][col]
                if value == 1:
                    self.playerONEscore += CENTER_WEIGHTS[col]
                elif value == 2:
                    self.playerTWOscore += CENTER_WEIGHTS[col]

    def _add_threat_density(self, board):
        player_one_threats = 0
        player_two_threats = 0
        for row in range(6):
            for col in range(7):
                if board[row][col] != 0:
                    continue
                if row < 5 and board[row + 1][col] == 0:
                    continue
                for window in self._windows_containing_cell(row, col):
                    count_one, count_two = 0, 0
                    for r, c in window:
                        if board[r][c] == 1:
                            count_one += 1
                        elif board[r][c] == 2:
                            count_two += 1
                    if count_two == 0 and count_one > 0:
                        player_one_threats += 1
                    if count_one == 0 and count_two > 0:
                        player_two_threats += 1
        self.playerONEscore += player_one_threats * 2
        self.playerTWOscore += player_two_threats * 2

    def _windows_containing_cell(self, row, col):
        windows = []
        for offset in range(4):
            start = col - offset
            if 0 <= start <= 3 and start + 3 < 7:
                windows.append([(row, start + d) for d in range(4)])
        for offset in range(4):
            start = row - offset
            if 0 <= start <= 2 and start + 3 < 6:
                windows.append([(start + d, col) for d in range(4)])
        for offset in range(4):
            start_row = row - offset
            start_col = col - offset
            if 0 <= start_row <= 2 and 0 <= start_col <= 3:
                windows.append([(start_row + d, start_col + d) for d in range(4)])
        for offset in range(4):
            start_row = row + offset
            start_col = col - offset
            if 3 <= start_row <= 5 and 0 <= start_col <= 3:
                windows.append([(start_row - d, start_col + d) for d in range(4)])
        return windows

    def check_draw(self, board):
        if all(all(cell != 0 for cell in row) for row in board):
            self.playerONEscore = 0
            self.playerTWOscore = 0
