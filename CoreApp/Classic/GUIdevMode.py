import tkinter as tk
from tkinter import messagebox

class ConnectFourGUI:
    def __init__(self, board):
        self.board = board
        self.root = tk.Tk()
        self.root.title('Connect Four')
        self.rows = getattr(board, 'rows', len(board.array))
        self.cols = getattr(board, 'cols', len(board.array[0]) if board.array else 0)
        if hasattr(self.board.move_analyzer, 'set_board_size'):
            self.board.move_analyzer.set_board_size(self.rows, self.cols)
        self.cell_labels = [[None] * self.cols for _ in range(self.rows)]
        self._create_widgets()
        self._update_gui()

        if hasattr(self.board, 'ai_player') and self.board.player_turn == self.board.ai_player:
            self.root.after(250, self._ai_move)

    def _create_widgets(self):
        self.board_area = tk.Frame(self.root)
        self.board_area.pack(padx=8, pady=8)

        button_font_size = max(8, min(12, 14 - self.board.cols // 2))
        button_font = ('Arial', button_font_size, 'bold')

        self.column_buttons = []
        for col in range(self.board.cols):
            btn = tk.Button(
                self.board_area,
                text=str(col + 1),
                width=4,
                height=2,
                font=button_font,
                command=lambda c=col: self._drop_piece(c)
            )
            btn.grid(row=0, column=col, padx=0, pady=(0, 0), sticky='nsew')
            self.column_buttons.append(btn)

        for col in range(self.board.cols):
            self.board_area.grid_columnconfigure(col, weight=1)

        for row in range(self.board.rows):
            for col in range(self.board.cols):
                label = tk.Label(
                    self.board_area,
                    text=' ',
                    width=4,
                    height=2,
                    relief='ridge',
                    borderwidth=1,
                    font=('Arial', 14, 'bold')
                )
                label.grid(row=row + 1, column=col, padx=0, pady=0, sticky='nsew')
                self.cell_labels[row][col] = label

        self.info_label = tk.Label(self.root, text='', font=('Arial', 12))
        self.info_label.pack(pady=4)

        self.weights_frame = tk.Frame(self.root)
        self.weights_frame.pack(padx=8, pady=4)

        #Weights analyze disp

        self.weight_title_1 = tk.Label(self.weights_frame, text='Player 1 (X) move weights', font=('Arial', 11, 'bold'))
        self.weight_title_1.grid(row=0, column=0, padx=8)
        self.weight_title_2 = tk.Label(self.weights_frame, text='Player 2 (O) move weights', font=('Arial', 11, 'bold'))
        self.weight_title_2.grid(row=0, column=1, padx=8)

        self.weights_text_1 = tk.Text(self.weights_frame, width=self.board.cols * 4 + 4, height=self.board.rows + 2, state='disabled', font=('Courier', 10))
        self.weights_text_1.grid(row=1, column=0, padx=8)
        self.weights_text_2 = tk.Text(self.weights_frame, width=self.board.cols * 4 + 4, height=self.board.rows + 2, state='disabled', font=('Courier', 10))
        self.weights_text_2.grid(row=1, column=1, padx=8)

        self.best_move_label = tk.Label(self.root, text='', font=('Arial', 12, 'bold'))
        self.best_move_label.pack(pady=4)

    def _drop_piece(self, column):
        if not self.board.run:
            return

        if self.board.add_piece(column, self.board.player_turn):
            if hasattr(self.board, 'handle_connect_fours'):
                self.board.handle_connect_fours()
            elif hasattr(self.board, 'look_for_win_move'):
                self.board.look_for_win_move()

            if hasattr(self.board, 'check_board_state'):
                self.board.check_board_state()

            if self.board.run:
                self.board.player_turn = 2 if self.board.player_turn == 1 else 1
        else:
            messagebox.showwarning('Invalid move', 'Column is full!')

        self._update_gui()

        if self.board.run and hasattr(self.board, 'ai_player') and self.board.player_turn == self.board.ai_player:
            self.root.after(300, self._ai_move)

        if not self.board.run:
            self._end_game()

    def _update_gui(self):
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                value = self.board.array[row][col]
                label = self.cell_labels[row][col]
                if value == 0:
                    label.config(text=' ', bg='white', fg='black')
                elif value == 1:
                    label.config(text='X', bg='yellow', fg='black')
                elif value == 2:
                    label.config(text='O', bg='cyan', fg='black')
                elif isinstance(value, str) and value.startswith('N'):
                    owner = value[1:]
                    if owner == '1':
                        label.config(text='N', bg='orange', fg='black')
                    elif owner == '2':
                        label.config(text='N', bg='purple', fg='white')
                    else:
                        label.config(text='N', bg='grey', fg='white')
                else:
                    label.config(text=' ', bg='white', fg='black')

        self.info_label.config(
            text=f'Player: {self.board.player_turn}   Scores - P1: {self.board.player_one_wins} | P2: {self.board.player_two_wins}'
        )
        #self._update_weights()

    def _update_weights(self):
        if hasattr(self.board.move_analyzer, 'set_board_size'):
            self.board.move_analyzer.set_board_size(self.rows, self.cols)
        self.board.move_analyzer.analyze(self.board.array)
        best_one = self.board.move_analyzer.best_move(1, self.board.array)
        best_two = self.board.move_analyzer.best_move(2, self.board.array)

        self._write_weight_text(self.weights_text_1, self.board.move_analyzer.player_one_weights)
        self._write_weight_text(self.weights_text_2, self.board.move_analyzer.player_two_weights)

        best_text = f'Best move P1: Column {best_one + 1 if best_one is not None else "N/A"}    '
        best_text += f'Best move P2: Column {best_two + 1 if best_two is not None else "N/A"}'
        self.best_move_label.config(text=best_text)

    def _end_game(self):
        for btn in self.column_buttons:
            btn.config(state='disabled')

        if hasattr(self.board, 'player_one_wins') and hasattr(self.board, 'player_two_wins'):
            final_text = f'Final Scores:\nPlayer 1: {self.board.player_one_wins}\nPlayer 2: {self.board.player_two_wins}'
        elif getattr(self.board, 'winning', 0) != 0:
            final_text = f'Winner is Player {self.board.winning}'
        else:
            final_text = 'Game Over'

        messagebox.showinfo('Game Over', final_text)

    def _ai_move(self):
        if not self.board.run or not hasattr(self.board, 'ai_player'):
            return

        if self.board.player_turn != self.board.ai_player:
            return

        column = self.board.move_analyzer.best_move(self.board.ai_player, self.board.array)
        if column is None:
            messagebox.showwarning('AI move', 'AI has no valid moves!')
            return

        if self.board.add_piece(column, self.board.player_turn):
            if hasattr(self.board, 'handle_connect_fours'):
                self.board.handle_connect_fours()
            elif hasattr(self.board, 'look_for_win_move'):
                self.board.look_for_win_move()

            if hasattr(self.board, 'check_board_state'):
                self.board.check_board_state()

            if self.board.run:
                self.board.player_turn = 2 if self.board.player_turn == 1 else 1
        else:
            messagebox.showwarning('Invalid move', 'AI made an invalid move')

        self._update_gui()
        if not self.board.run:
            self._end_game()

    @staticmethod
    def _write_weight_text(widget, weights):
        widget.config(state='normal')
        widget.delete('1.0', tk.END)
        for row in weights:
            widget.insert(tk.END, ' '.join(f'{w:4d}' if w != 0 else '   .' for w in row) + '\n')
        widget.config(state='disabled')