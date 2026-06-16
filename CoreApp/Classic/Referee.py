
class Referee:
    @staticmethod
    def check_vertical(board):
        for i in range(0, 3):
            for j in range(0, 7):
                if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j]:
                    if board[i][j] != 0:
                        return board[i][j]
        return 0

    @staticmethod
    def check_horizontal(board):
        for i in range(0, 6):
            for j in range(0, 4):
                if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3]:
                    if board[i][j] != 0:
                        return board[i][j]
        return 0

    @staticmethod
    def check_diagonal_f(board):
        for i in range(0, 3):
            for j in range(0, 4):
                if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3]:
                    if board[i][j] != 0:
                        return board[i][j]
        return 0

    @staticmethod
    def check_diagonal_b(board):
        for i in range(3, 6):
            for j in range(0, 4):
                if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3]:
                    if board[i][j] != 0:
                        return board[i][j]
        return 0

    @staticmethod
    def check_draw(board):
        return all(all(cell != 0 for cell in row) for row in board)

    @staticmethod
    def find_winner(board):
        for check in (
            Referee.check_vertical,
            Referee.check_horizontal,
            Referee.check_diagonal_b,
            Referee.check_diagonal_f,
        ):
            winner = check(board)
            if winner != 0:
                return winner
        return 0