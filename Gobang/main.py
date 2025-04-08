
import pygame
import sys
import copy
import threading
from config import *
from game_logic import GameLogic
from board import BoardManager
from ui import UIManager
from ai import AIPlayer


class GomokuGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("五子棋")
        self.clock = pygame.time.Clock()

        self.ui = UIManager()
        self.settings = DEFAULT_SETTINGS.copy()
        self._init_game_state()

        self.game_state = "main_menu"
        self.ai_thread = None
        self.ai_move = None
        self.ai_thinking = False

    def _init_game_state(self):
        self.board = BoardManager(self.settings["board_size"])
        self.logic = GameLogic()
        self.ai = AIPlayer(AI_PLAYER, self.settings["ai_difficulty"])
        self.current_player = 1
        self.game_over = False
        self.history = []

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)

            if self.game_state == "gaming" and not self.game_over:
                self._process_ai_move()

            self._update_display()
            pygame.display.flip()
            self.clock.tick(60)

    def _handle_click(self, pos):
        if self.game_state == "main_menu":
            self._handle_main_menu_click(pos)
        elif self.game_state == "settings":
            self._handle_settings_click(pos)
        elif self.game_state == "gaming":
            self._handle_game_click(pos)

    def _handle_main_menu_click(self, pos):
        if self.ui.start_btn.collidepoint(pos):
            self._start_new_game()
        elif self.ui.settings_btn.collidepoint(pos):
            self.game_state = "settings"
        elif self.ui.exit_btn.collidepoint(pos):
            pygame.quit()
            sys.exit()

    def _handle_settings_click(self, pos):
        action = self.ui.handle_settings_click(pos)
        if action == 'back':
            self.game_state = "main_menu"
        elif action == 'change_difficulty':
            self._cycle_setting('ai_difficulty', ['easy', 'medium', 'hard'])
        elif action == 'change_board_size':
            self._cycle_setting('board_size', [11, 13, 15, 17, 19])
        elif action == 'toggle_sound':
            self.settings['sound_enabled'] = not self.settings['sound_enabled']

    def _handle_game_click(self, pos):
        if self.current_player == AI_PLAYER or self.game_over:
            return

        board_pos = self.board.coord_to_pos(*pos)
        if board_pos:
            self._place_stone(*board_pos)

    def _cycle_setting(self, key, options):
        index = options.index(self.settings[key])
        self.settings[key] = options[(index + 1) % len(options)]
        if key == 'board_size':
            self._init_game_state()

    def _start_new_game(self):
        self.game_state = "gaming"
        self._init_game_state()

    def _update_display(self):
        if self.game_state == "main_menu":
            self.ui.draw_main_menu(self.screen)
        elif self.game_state == "settings":
            self.ui.draw_settings_menu(self.screen, self.settings)
        elif self.game_state == "gaming":
            self._draw_game_interface()
            self._draw_game_info()

    def _draw_game_interface(self):
        self.board.draw_board(self.screen)
        # 可以在此处添加游戏内UI元素

    def _draw_game_info(self):
        info_font = pygame.font.SysFont('simhei', 32)
        current_player_text = f"当前玩家: {'黑棋' if self.current_player == 1 else '白棋'}"
        info_surf = info_font.render(current_player_text, True, COLORS["text"])
        self.screen.blit(info_surf, (WIDTH - UI_WIDTH + 20, 20))
        if self.game_over:
            game_over_text = "游戏结束"
            game_over_surf = info_font.render(game_over_text, True, COLORS["text"])
            self.screen.blit(game_over_surf, (WIDTH - UI_WIDTH + 20, 60))

    def _place_stone(self, row, col):
        if self.logic.is_valid_move(self.board.board, row, col):
            self.history.append(copy.deepcopy(self.board.board))
            self.board.board[row][col] = self.current_player
            if self.logic.check_win(self.board.board, row, col):
                self.game_over = True
            else:
                self.current_player = self.logic.switch_player(self.current_player)
                if self.current_player == AI_PLAYER:
                    self._start_ai_thread()

    def _start_ai_thread(self):
        if not self.ai_thinking and not self.game_over:
            self.ai_thinking = True
            self.ai_thread = threading.Thread(target=self._calculate_ai_move)
            self.ai_thread.daemon = True
            self.ai_thread.start()

    def _calculate_ai_move(self):
        try:
            self.ai_move = self.ai.get_move(self.board.board)
        except Exception as e:
            print(f"AI Error: {e}")
            self.ai_move = None
        finally:
            self.ai_thinking = False

    def _process_ai_move(self):
        if self.ai_move is not None:
            row, col = self.ai_move
            self._place_stone(row, col)
            self.ai_move = None


if __name__ == "__main__":
    game = GomokuGame()
    game.run()