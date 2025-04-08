import pygame
from config import *


class UIManager:
    def __init__(self):
        pygame.font.init()
        self.title_font = pygame.font.SysFont('simhei', 48)
        self.button_font = pygame.font.SysFont('simhei', 32)
        self.small_font = pygame.font.SysFont('simhei', 24)
        self._init_ui_elements()

    def _init_ui_elements(self):
        # 主菜单
        self.start_pvp_btn = pygame.Rect(0, 0, 200, 60)
        self.start_pve_btn = pygame.Rect(0, 0, 200, 60)
        self.settings_btn = pygame.Rect(0, 0, 200, 60)
        self.exit_btn = pygame.Rect(0, 0, 200, 60)

        # 设置菜单
        self.ai_difficulty_btn = pygame.Rect(0, 0, 300, 40)
        self.board_size_btn = pygame.Rect(0, 0, 300, 40)
        self.sound_btn = pygame.Rect(0, 0, 300, 40)
        self.back_btn = pygame.Rect(50, 50, 100, 40)

        self._recalculate_positions()

    def _recalculate_positions(self):
        center_x = WIDTH // 2
        # 主菜单
        self.start_pvp_btn.center = (center_x, 200)
        self.start_pve_btn.center = (center_x, 300)
        self.settings_btn.center = (center_x, 400)
        self.exit_btn.center = (center_x, 500)

        # 设置菜单
        self.ai_difficulty_btn.topleft = (center_x - 150, 200)
        self.board_size_btn.topleft = (center_x - 150, 280)
        self.sound_btn.topleft = (center_x - 150, 360)
        self.back_btn.topleft = (50, 50)

    def draw_main_menu(self, screen):
        screen.fill(COLORS["menu_bg"])
        title = self.title_font.render("五子棋", True, COLORS["text"])
        title_rect = title.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title, title_rect)
        self._draw_button(screen, self.start_pvp_btn, "人人对战")
        self._draw_button(screen, self.start_pve_btn, "人机对战")
        self._draw_button(screen, self.settings_btn, "游戏设置")
        self._draw_button(screen, self.exit_btn, "退出游戏")

    def draw_settings_menu(self, screen, settings):
        screen.fill(COLORS["menu_bg"])
        self._draw_button(screen, self.back_btn, "返回", self.small_font)
        self._draw_setting_item(screen, self.ai_difficulty_btn,
                                f"AI难度: {settings['ai_difficulty']}")
        self._draw_setting_item(screen, self.board_size_btn,
                                f"棋盘尺寸: {settings['board_size']}")
        self._draw_setting_item(screen, self.sound_btn,
                                f"音效: {'开启' if settings['sound_enabled'] else '关闭'}")

    def _draw_button(self, screen, rect, text, font=None):
        font = font or self.button_font
        mouse_pos = pygame.mouse.get_pos()
        color = COLORS["button_hover"] if rect.collidepoint(mouse_pos) else COLORS["button"]
        pygame.draw.rect(screen, color, rect, border_radius=5)
        text_surf = font.render(text, True, COLORS["text"])
        screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def _draw_setting_item(self, screen, rect, text):
        pygame.draw.rect(screen, COLORS["button"], rect, border_radius=3)
        text_surf = self.small_font.render(text, True, COLORS["text"])
        screen.blit(text_surf, (rect.x + 10, rect.centery - 10))
        arrow = self.small_font.render(">", True, COLORS["text"])
        screen.blit(arrow, (rect.right - 30, rect.centery - 10))

    def handle_settings_click(self, pos):
        if self.ai_difficulty_btn.collidepoint(pos):
            return 'change_difficulty'
        elif self.board_size_btn.collidepoint(pos):
            return 'change_board_size'
        elif self.sound_btn.collidepoint(pos):
            return 'toggle_sound'
        elif self.back_btn.collidepoint(pos):
            return 'back'
        return None