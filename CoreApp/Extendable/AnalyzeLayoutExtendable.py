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

CENTER_WEIGHTS_BASE = [3, 4, 5, 7, 5, 4, 3]
OPEN_THREE_BONUS = 120
NON_PLAYABLE_MULTIPLIER = 0.35
DOUBLE_THREAT_BONUS = 80


class AnalyzeLayout:
    def __init__(self):
        self.playerONEscore = 0
        self.playerTWOscore = 0
        self.center_weights = CENTER_WEIGHTS_BASE

    def set_board_size(self, rows, cols):
        """Set board dimensions and compute center weights for dynamic board size"""
        self.rows = rows
        self.cols = cols
        self._compute_center_weights(cols)

    def _compute_center_weights(self, cols):
        """Compute center weights for board of given column count"""
        if cols == 7:
            self.center_weights = [3, 4, 5, 7, 5, 4, 3]
        else:
            mid = cols / 2.0
            self.center_weights = [max(1, int(7 - abs(i - mid))) for i in range(cols)]

    def analyzeBoard(self, board):
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        
        if cols != len(self.center_weights):
            self._compute_center_weights(cols)
        
        self.rows = rows
        self.cols = cols
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
        """Generate all 4-cell windows in all directions"""
        windows = []
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        
        for row in range(rows):
            for col in range(cols - 3):
                windows.append([(row, col + d) for d in range(4)])
        
        for row in range(rows - 3):
            for col in range(cols):
                windows.append([(row + d, col) for d in range(4)])
        
        for row in range(rows - 3):
            for col in range(cols - 3):
                windows.append([(row + d, col + d) for d in range(4)])
        
        for row in range(3, rows):
            for col in range(cols - 3):
                windows.append([(row - d, col + d) for d in range(4)])
        
        return windows

    def _evaluate_window(self, board, window):
        count_one = 0
        count_two = 0
        empty_cells = []

        for row, col in window:
            value = board[row][col]
            # skip windows that contain disabled markers (e.g. 'N1','N2')
            if isinstance(value, str) and value.startswith('N'):
                return
            if value == 1:
                count_one += 1
            elif value == 2:
                count_two += 1
            elif value == 0:
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
        """Compute center proximity factor for a window"""
        total_weight = sum(self.center_weights[col] for _, col in window)
        max_weight = sum(self.center_weights) / len(self.center_weights) * 4
        return total_weight / max_weight if max_weight > 0 else 0

    def _window_has_playable_empty(self, board, empty_cells):
        """Check if any empty cell in window is playable (at bottom or has piece below)"""
        rows = len(board)
        for row, col in empty_cells:
            below = board[row + 1][col] if row + 1 < rows else None
            if row == rows - 1 or (below is not None and below != 0):
                return True
        return False

    def _window_playable_multiplier(self, board, empty_cells):
        """Return playability multiplier"""
        if not empty_cells:
            return 1.0
        return 1.0 if self._window_has_playable_empty(board, empty_cells) else NON_PLAYABLE_MULTIPLIER

    def _add_center_control(self, board):
        """Reward center column control"""
        for row in range(len(board)):
            for col in range(len(board[0])):
                value = board[row][col]
                if isinstance(value, int):
                    if value == 1:
                        self.playerONEscore += self.center_weights[col]
                    elif value == 2:
                        self.playerTWOscore += self.center_weights[col]

    def _add_threat_density(self, board):
        """Reward threat density (number of playable positions with own pieces)"""
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        
        player_one_threats = 0
        player_two_threats = 0
        for row in range(rows):
            for col in range(cols):
                # only consider truly empty playable slots (not disabled 'N')
                cell = board[row][col]
                if cell != 0:
                    continue
                if row < rows - 1 and board[row + 1][col] == 0:
                    continue
                for window in self._windows_containing_cell(board, row, col):
                    count_one, count_two = 0, 0
                    skip_window = False
                    for r, c in window:
                        v = board[r][c]
                        if isinstance(v, str) and v.startswith('N'):
                            skip_window = True
                            break
                        if v == 1:
                            count_one += 1
                        elif v == 2:
                            count_two += 1
                    if skip_window:
                        continue
                    if count_two == 0 and count_one > 0:
                        player_one_threats += 1
                    if count_one == 0 and count_two > 0:
                        player_two_threats += 1
        self.playerONEscore += player_one_threats * 2
        self.playerTWOscore += player_two_threats * 2

    def _windows_containing_cell(self, board, row, col):
        """Get all 4-cell windows containing a specific cell"""
        windows = []
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        
        for offset in range(4):
            start = col - offset
            if 0 <= start <= cols - 4:
                windows.append([(row, start + d) for d in range(4)])
        
        for offset in range(4):
            start = row - offset
            if 0 <= start <= rows - 4:
                windows.append([(start + d, col) for d in range(4)])
        
        for offset in range(4):
            start_row = row - offset
            start_col = col - offset
            if 0 <= start_row <= rows - 4 and 0 <= start_col <= cols - 4:
                windows.append([(start_row + d, start_col + d) for d in range(4)])
        
        for offset in range(4):
            start_row = row + offset
            start_col = col - offset
            if rows - 4 <= start_row < rows and 0 <= start_col <= cols - 4:
                windows.append([(start_row - d, start_col + d) for d in range(4)])
        
        return windows

    def check_draw(self, board):
        """Check for draw (board full)"""
        if all(all(cell != 0 for cell in row) for row in board):
            self.playerONEscore = 0
            self.playerTWOscore = 0

