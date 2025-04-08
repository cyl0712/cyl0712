class GameLogic:
    @staticmethod
    def check_win(board, row, col):
        directions = [
            [(0, 1), (0, -1)],
            [(1, 0), (-1, 0)],
            [(1, 1), (-1, -1)],
            [(1, -1), (-1, 1)]
        ]
        player = board[row][col]
        for dirs in directions:
            count = 1
            for dx, dy in dirs:
                x, y = row + dx, col + dy
                while 0 <= x < len(board) and 0 <= y < len(board[0]):
                    if board[x][y] == player:
                        count += 1
                        x += dx
                        y += dy
                    else:
                        break
            if count >= 5:
                return True
        return False

    @staticmethod
    def is_valid_move(board, row, col):
        return 0 <= row < len(board) and 0 <= col < len(board[0]) and board[row][col] == 0

    @staticmethod
    def switch_player(current_player):
        return 2 if current_player == 1 else 1