import pygame
from config import *


class BoardManager:
    def __init__(self, board_size=DEFAULT_BOARD_SIZE):
        self.board_size = board_size
        self.board = [[0] * board_size for _ in range(board_size)]
        self.board_start = MARGIN
        self.board_end = MARGIN + (board_size - 1) * GRID_SIZE

    def coord_to_pos(self, x, y):
        if not (self.board_start <= x <= self.board_end and
                self.board_start <= y <= self.board_end):
            return None
        col = round((x - self.board_start) / GRID_SIZE)
        row = round((y - self.board_start) / GRID_SIZE)
        row = max(0, min(row, self.board_size - 1))
        col = max(0, min(col, self.board_size - 1))
        return (row, col)

    def draw_board(self, screen):
        screen.fill(COLORS["board_bg"])
        for i in range(self.board_size):
            offset = self.board_start + i * GRID_SIZE
            pygame.draw.line(screen, COLORS["line"],
                             (self.board_start, offset),
                             (self.board_end, offset))
            pygame.draw.line(screen, COLORS["line"],
                             (offset, self.board_start),
                             (offset, self.board_end))
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] != 0:
                    color = (0, 0, 0) if self.board[row][col] == 1 else (255, 255, 255)
                    center = (
                        self.board_start + col * GRID_SIZE,
                        self.board_start + row * GRID_SIZE
                    )
                    pygame.draw.circle(screen, color, center, GRID_SIZE // 2 - 2)

    def reset(self):
        self.board = [[0] * self.board_size for _ in range(self.board_size)]