import random
import threading
from game_logic import GameLogic


class AIPlayer:
    def __init__(self, player, difficulty="medium"):
        self.player = player
        self.difficulty = difficulty
        self.depths = {'easy': 2, 'medium': 3, 'hard': 4}
        self.max_depth = self.depths[difficulty]

    def get_move(self, board):
        candidates = self._generate_candidates(board)
        return random.choice(candidates) if candidates else None

    def _generate_candidates(self, board, radius=1):
        candidates = set()
        size = len(board)
        for i in range(size):
            for j in range(size):
                if board[i][j] != 0:
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            x = i + dx * radius
                            y = j + dy * radius
                            if 0 <= x < size and 0 <= y < size and board[x][y] == 0:
                                candidates.add((x, y))
        return list(candidates) if candidates else [(size // 2, size // 2)]