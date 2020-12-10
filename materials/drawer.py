import pygame
from pygame.locals import *  # 定数読み込み

from .align import Align  # オブジェクトの配置に関するモジュール
from .colors import Color  # 色に関するモジュール


class Drawer:
    def __init__(self):
        pygame.init()  # Pygame初期化
        self.width, self.height = (800, 600)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font_small = pygame.font.SysFont("yumincho", 15)
        self.font_medium = pygame.font.SysFont("yumincho", 30)
        self.font_large = pygame.font.SysFont("yumincho", 60)

    def make_header(self, text, height_correction=0):
        """
        ヘッダーを表示するメソッド
        height_correctionで表示するy座標を補正できる
        """
        text_surface = self.font_large.render(text, True, Color.WHITE.rgb)
        align = Align(text_surface, self.width, self.height)
        used_height = height_correction + align.middle() - text_surface.get_height() * 2
        self.screen.blit(text_surface, [align.center(), used_height])
        return used_height

    def make_subheader(self, text_list, height_correction=0):
        """
        小見出しを表示するためのメソッド
        各小見出しをリストで貰う
        """
        for i, text in enumerate(text_list):
            text_surface = self.font_medium.render(text, True, Color.WHITE.rgb)
            align = Align(text_surface, self.width, self.height)
            used_height = align.middle() + text_surface.get_height() * i
            self.screen.blit(
                text_surface, [align.center(), used_height + height_correction]
            )

    def make_top_left_subheader(self, text):
        """画面右上に文字を表示するメソッド"""
        text_surface = self.font_medium.render(text, True, Color.WHITE.rgb)
        align = Align(text_surface, self.width, self.height)
        self.screen.blit(text_surface, [align.left() + 10, align.top() + 10])

    def make_top_right_subheader(self, text):
        """画面左上に文字を表示するメソッド"""
        text_surface = self.font_medium.render(text, True, Color.WHITE.rgb)
        align = Align(text_surface, self.width, self.height)
        self.screen.blit(text_surface, [align.right() - 10, align.top() + 10])

    def make_bottom_subheader(self, text):
        """画面中央下に文字を表示するメソッド"""
        text_surface = self.font_medium.render(text, True, Color.RED.rgb)
        align = Align(text_surface, self.width, self.height)
        self.screen.blit(
            text_surface, [align.center(), align.bottom() - text_surface.get_height()]
        )

    def fill_bottom_subheader(self):
        """画面中央下を塗りつぶすメソッド"""
        self.screen.fill(
            Color.BLACK.rgb,
            (0.0, float(self.height - 30 * 2), float(self.width), float(30)),
        )

    def text_box(self, text):
        """
        入力文字を表示するためのメソッド
        """
        text_surface = self.font_medium.render(text, True, (255, 255, 255))
        self.screen.fill(
            (0, 0, 0),
            (
                0,
                self.height - text_surface.get_height() * 2,
                self.width,
                text_surface.get_height(),
            ),
        )
        self.screen.blit(
            text_surface,
            [
                ((self.width / 2) - (text_surface.get_width() / 2)),
                (self.height - text_surface.get_height() * 2),
            ],
        )
