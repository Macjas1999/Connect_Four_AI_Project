import tkinter as tk
from tkinter import messagebox, simpledialog

class ConnectFourGUI:
    def __init__(self, board):
        self.board = board
        self.root = tk.Tk()
        self.root.title('Connect Four Extended Map')
        self.rows = getattr(board, 'rows', len(board.array))
        self.cols = getattr(board, 'cols', len(board.array[0]) if board.array else 0)
        if hasattr(self.board.move_analyzer, 'set_board_size'):
            self.board.move_analyzer.set_board_size(self.rows, self.cols)
        self.cell_size = 60
        self.piece_radius = 25
        self.cell_canvases = [[None] * self.cols for _ in range(self.rows)]
        self._winning_cells = []
        self._game_mode = None  # 'human_vs_human' or 'human_vs_ai'
        self._create_widgets()
        self._show_game_mode_selection()
        self._update_gui()

        if hasattr(self.board, 'ai_player') and self.board.player_turn == self.board.ai_player:
            self.root.after(250, self._ai_move)

    def _create_widgets(self):
        self.board_area = tk.Frame(self.root, bg='lightgray')
        self.board_area.pack(padx=8, pady=8)

        button_font_size = max(8, min(12, 14 - self.cols // 2))
        button_font = ('Arial', button_font_size, 'bold')

        # Insert piece buttons with down arrow
        self.column_buttons = []
        for col in range(self.cols):
            btn = tk.Button(
                self.board_area,
                text='↓',
                width=4,
                height=2,
                font=button_font,
                command=lambda c=col: self._drop_piece(c)
            )
            btn.grid(row=0, column=col, padx=2, pady=(0, 2), sticky='nsew')
            self.column_buttons.append(btn)

        # Board grid creation with canvases for circular pieces
        for col in range(self.cols):
            self.board_area.grid_columnconfigure(col, weight=1)

        for row in range(self.rows):
            for col in range(self.cols):
                canvas = tk.Canvas(
                    self.board_area,
                    width=self.cell_size,
                    height=self.cell_size,
                    bg='lightgray',
                    highlightthickness=1,
                    highlightbackground='darkgray'
                )
                canvas.grid(row=row + 1, column=col, padx=2, pady=2, sticky='nsew')
                self.cell_canvases[row][col] = canvas

        self.info_label = tk.Label(self.root, text='', font=('Arial', 12))
        self.info_label.pack(pady=4)

    def _show_game_mode_selection(self):
        """Show dialog to select game mode at startup"""
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno('Game Mode', 'Do you want to play vs AI?')
        root.destroy()
        
        if result:
            self._game_mode = 'human_vs_ai'
            # Ask which player the human wants to be
            root2 = tk.Tk()
            root2.withdraw()
            while True:
                try:
                    choice = simpledialog.askinteger('Player Selection', 'Which player do you want to play as? (1 or 2)')
                    if choice is None:
                        self._game_mode = 'human_vs_human'
                        root2.destroy()
                        break
                    if choice in (1, 2):
                        self.board.ai_player = 2 if choice == 1 else 1
                        self.board.human_player = choice
                        self.board.player_turn = 1
                        root2.destroy()
                        break
                except Exception:
                    root2.destroy()
                    break
        else:
            self._game_mode = 'human_vs_human'

    def _drop_piece(self, column):
        if not self.board.run:
            return

        drop_row = self._find_drop_row(column)
        if drop_row is None:
            messagebox.showwarning('Invalid move', 'Column is full!')
            return

        player = self.board.player_turn
        self._set_buttons_state('disabled')
        self._animate_drop(column, drop_row, player)

    def _update_cell(self, row, col):
        value = self.board.array[row][col]
        canvas = self.cell_canvases[row][col]
        canvas.delete('all')
        
        # Highlight winning cells with a different background
        if (row, col) in getattr(self, '_winning_cells', []):
            canvas.config(bg='gold')
        else:
            canvas.config(bg='lightgray')
        
        if value == 0:
            # Empty cell - draw nothing
            pass
        elif value == 1:
            # Player 1 - blue circle
            self._draw_circle(canvas, '#0066FF', '#003399')
        elif value == 2:
            # Player 2 - red circle
            self._draw_circle(canvas, 'red', 'darkred')
        elif isinstance(value, str) and value.startswith('N'):
            # Special piece (N for Network/AI)
            owner = value[1:]
            if owner == '1':
                self._draw_circle(canvas, 'yellow', 'orange')
            elif owner == '2':
                self._draw_circle(canvas, 'lightgreen', 'green')
            else:
                self._draw_circle(canvas, 'gray', 'darkgray')

    def _draw_circle(self, canvas, fill_color, outline_color):
        """Draw a circle in the center of the canvas"""
        x0 = self.cell_size / 2 - self.piece_radius
        y0 = self.cell_size / 2 - self.piece_radius
        x1 = self.cell_size / 2 + self.piece_radius
        y1 = self.cell_size / 2 + self.piece_radius
        canvas.create_oval(x0, y0, x1, y1, fill=fill_color, outline=outline_color, width=2)

    def _update_gui(self):
        # Update cached winning cells when game finished
        if getattr(self.board, 'winning', 0) != 0:
            self._winning_cells = self._get_winning_cells()
        else:
            self._winning_cells = []

        for row in range(self.rows):
            for col in range(self.cols):
                self._update_cell(row, col)

        self.info_label.config(
            text=f'Player: {self.board.player_turn}   Scores - P1: {self.board.player_one_wins} | P2: {self.board.player_two_wins}'
        )

    def _get_winning_cells(self):
        b = self.board.array
        rows = self.rows
        cols = self.cols
        # vertical
        for i in range(0, rows - 3):
            for j in range(0, cols):
                v = b[i][j]
                if v != 0 and b[i + 1][j] == v and b[i + 2][j] == v and b[i + 3][j] == v:
                    return [(i + k, j) for k in range(4)]
        # horizontal
        for i in range(0, rows):
            for j in range(0, cols - 3):
                v = b[i][j]
                if v != 0 and b[i][j + 1] == v and b[i][j + 2] == v and b[i][j + 3] == v:
                    return [(i, j + k) for k in range(4)]
        # diagonal backward (\)
        for i in range(3, rows):
            for j in range(0, cols - 3):
                v = b[i][j]
                if v != 0 and b[i - 1][j + 1] == v and b[i - 2][j + 2] == v and b[i - 3][j + 3] == v:
                    return [(i - k, j + k) for k in range(4)]
        # diagonal forward (/)
        for i in range(0, rows - 3):
            for j in range(0, cols - 3):
                v = b[i][j]
                if v != 0 and b[i + 1][j + 1] == v and b[i + 2][j + 2] == v and b[i + 3][j + 3] == v:
                    return [(i + k, j + k) for k in range(4)]
        return []

    def _find_drop_row(self, column):
        for row in range(self.rows - 1, -1, -1):
            if self.board.array[row][column] == 0:
                return row
        return None

    def _piece_style(self, player):
        if player == 1:
            return '#0066FF', '#003399'
        elif player == 2:
            return 'red', 'darkred'
        else:
            raise Exception('Invalid player number')

    def _set_buttons_state(self, state):
        for button in self.column_buttons:
            button.config(state=state)

    def _animate_drop(self, column, target_row, player):
        fill_color, outline_color = self._piece_style(player)
        self._animate_drop_step(column, target_row, 0, fill_color, outline_color, player)

    def _animate_drop_step(self, column, target_row, current_row, fill_color, outline_color, player):
        if current_row > 0:
            self._update_cell(current_row - 1, column)

        canvas = self.cell_canvases[current_row][column]
        canvas.delete('all')
        canvas.config(bg='lightgray')
        self._draw_circle(canvas, fill_color, outline_color)

        if current_row < target_row:
            self.root.after(80, lambda: self._animate_drop_step(column, target_row, current_row + 1, fill_color, outline_color, player))
        else:
            self.root.after(120, lambda: self._commit_move(column, player))

    def _commit_move(self, column, player):
        self.board.add_piece(column, player)

        if hasattr(self.board, 'handle_connect_fours'):
            self.board.handle_connect_fours()

        if hasattr(self.board, 'check_board_state'):
            self.board.check_board_state()

        if self.board.run:
            self.board.player_turn = 2 if self.board.player_turn == 1 else 1

        self._update_gui()
        self._set_buttons_state('normal')

        if self.board.run and hasattr(self.board, 'ai_player') and self.board.player_turn == self.board.ai_player:
            self.root.after(300, self._ai_move)

        if not self.board.run:
            self._end_game()

    def _end_game(self):
        for btn in self.column_buttons:
            btn.config(state='disabled')

        if hasattr(self.board, 'player_one_wins') and hasattr(self.board, 'player_two_wins'):
            final_text = f'Final Scores:\nPlayer 1: {self.board.player_one_wins}\nPlayer 2: {self.board.player_two_wins}'
        elif getattr(self.board, 'winning', 0) != 0:
            final_text = f'Winner is Player {self.board.winning}'
        else:
            final_text = 'Game Over'

        # Show final message and offer to start a new game
        start_again = messagebox.askyesno('Game Over', final_text + '\n\nStart a new game?')
        if start_again:
            self._start_new_game()
        else:
            self.root.quit()

    def _start_new_game(self):
        # Reset board array and state
        self.board.array = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.board.winning = 0
        self.board.run = True
        self.board.player_one_wins = 0
        self.board.player_two_wins = 0
        self.board.player_turn = 1

        # Show game mode selection again
        result = messagebox.askyesno('Game Mode', 'Human vs AI?\n\nYes = Human vs AI\nNo = Human vs Human')

        if result:
            # Ask which player the human wants to be
            while True:
                try:
                    choice = simpledialog.askinteger('Player Selection', 'Which player do you want to play as? (1 or 2)')
                    if choice is None:
                        self._game_mode = 'human_vs_human'
                        if hasattr(self.board, 'ai_player'):
                            delattr(self.board, 'ai_player')
                        break
                    if choice in (1, 2):
                        self.board.ai_player = 2 if choice == 1 else 1
                        self.board.human_player = choice
                        self._game_mode = 'human_vs_ai'
                        break
                except Exception:
                    break
        else:
            self._game_mode = 'human_vs_human'
            if hasattr(self.board, 'ai_player'):
                delattr(self.board, 'ai_player')

        # Clear cached winning cells and refresh GUI
        self._winning_cells = []
        self._update_gui()
        self._set_buttons_state('normal')

        # If AI starts, schedule its move
        if hasattr(self.board, 'ai_player') and self.board.player_turn == self.board.ai_player:
            self.root.after(250, self._ai_move)

    def _ai_move(self):
        if not self.board.run or not hasattr(self.board, 'ai_player'):
            return

        if self.board.player_turn != self.board.ai_player:
            return

        # Ensure analysis is up-to-date before asking AI for best move
        if hasattr(self.board.move_analyzer, 'analyze'):
            self.board.move_analyzer.analyze(self.board.array)
        column = self.board.move_analyzer.best_move(self.board.ai_player, self.board.array)
        if column is None:
            messagebox.showwarning('AI move', 'AI has no valid moves!')
            return

        drop_row = self._find_drop_row(column)
        if drop_row is None:
            messagebox.showwarning('Invalid move', 'AI made an invalid move')
            return

        self._set_buttons_state('disabled')
        self._animate_drop(column, drop_row, self.board.player_turn)