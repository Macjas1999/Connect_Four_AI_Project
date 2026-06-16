class Referee:
    @staticmethod
    def find_all_connect_fours(board):
        """Find all connect-four positions and return list of (player, start_pos, direction)"""
        connects = []
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        
        for row in range(rows - 3):
            for col in range(cols):
                if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col]:
                    if board[row][col] != 0:
                        connects.append((board[row][col], (row, col), 'vertical'))
        
        for row in range(rows):
            for col in range(cols - 3):
                if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3]:
                    if board[row][col] != 0:
                        connects.append((board[row][col], (row, col), 'horizontal'))
        
        for row in range(rows - 3):
            for col in range(cols - 3):
                if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3]:
                    if board[row][col] != 0:
                        connects.append((board[row][col], (row, col), 'diag_f'))
        
        for row in range(3, rows):
            for col in range(cols - 3):
                if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3]:
                    if board[row][col] != 0:
                        connects.append((board[row][col], (row, col), 'diag_b'))
        
        return connects

    @staticmethod
    def check_draw(board):
        return all(all(cell != 0 for cell in row) for row in board)

    @staticmethod
    def find_and_mark_connect_fours(board):
        """Scan left-to-right, top-to-bottom. When a connect-four is found,
        immediately mark its four cells as disabled ('N1'/'N2') so they
        won't be counted again. Returns (p1_count, p2_count)."""
        rows = len(board)
        cols = len(board[0]) if rows > 0 else 0
        p1 = 0
        p2 = 0

        for row in range(rows):
            for col in range(cols):
                cell = board[row][col]
                # only integer pieces can start a new connect
                if not isinstance(cell, int) or cell == 0:
                    continue
                player = cell

                # check horizontal (left-to-right)
                if col + 3 < cols:
                    coords = [(row, col + d) for d in range(4)]
                    if all(isinstance(board[r][c], int) and board[r][c] == player for r, c in coords):
                        for r, c in coords:
                            board[r][c] = f'N{player}'
                        if player == 1:
                            p1 += 1
                        else:
                            p2 += 1
                        continue

                # check vertical (top-to-bottom)
                if row + 3 < rows:
                    coords = [(row + d, col) for d in range(4)]
                    if all(isinstance(board[r][c], int) and board[r][c] == player for r, c in coords):
                        for r, c in coords:
                            board[r][c] = f'N{player}'
                        if player == 1:
                            p1 += 1
                        else:
                            p2 += 1
                        continue

                # check diagonal down-right
                if row + 3 < rows and col + 3 < cols:
                    coords = [(row + d, col + d) for d in range(4)]
                    if all(isinstance(board[r][c], int) and board[r][c] == player for r, c in coords):
                        for r, c in coords:
                            board[r][c] = f'N{player}'
                        if player == 1:
                            p1 += 1
                        else:
                            p2 += 1
                        continue

                # check diagonal up-right
                if row - 3 >= 0 and col + 3 < cols:
                    coords = [(row - d, col + d) for d in range(4)]
                    if all(isinstance(board[r][c], int) and board[r][c] == player for r, c in coords):
                        for r, c in coords:
                            board[r][c] = f'N{player}'
                        if player == 1:
                            p1 += 1
                        else:
                            p2 += 1
                        continue

        return p1, p2