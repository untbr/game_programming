import sys
import textwrap
from time import sleep

import pygame
from pygame.locals import *  # 定数読み込み

from .align import Align  # オブジェクトの配置に関するモジュール
from .colors import Color  # 色に関するモジュール
from .text import Text


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
        text_surface = self.font_large.render(text, True, Color.BLACK.rgb)
        align = Align(text_surface, self.width, self.height)
        used_height = height_correction + align.middle() - text_surface.get_height() * 2
        self.screen.blit(text_surface, [align.center(), used_height])
        return used_height

    def make_header_outline(self):
        """ヘッダーの枠を表示するメソッド"""
        top_start_pos, top_end_pos = (100, 100), (700, 100)
        bottom_start_pos, bottom_end_pos = (100, 220), (700, 220)
        pygame.draw.line(self.screen, Color.BLUE.rgb, top_start_pos, top_end_pos)
        pygame.draw.line(self.screen, Color.BLUE.rgb, bottom_start_pos, bottom_end_pos)

    def make_header_underline(self):
        """ヘッダーのアンダーラインを表示するメソッド"""
        start_pos, end_pos = (100, 110), (700, 110)
        pygame.draw.line(self.screen, Color.BLACK.rgb, start_pos, end_pos)

    def make_subheader(self, text_list, height_correction=0, focus_index=None):
        """
        小見出しを表示するためのメソッド
        各小見出しをリストで貰う
        """
        for i, text in enumerate(text_list):
            text_surface = self.font_medium.render(text, True, Color.BLACK.rgb)
            align = Align(text_surface, self.width, self.height)
            used_height = align.middle() + text_surface.get_height() * i
            if i == focus_index:
                pygame.draw.rect(
                    self.screen,
                    Color.TEAL.rgb,
                    Rect(
                        align.center(),
                        used_height,
                        text_surface.get_width(),
                        text_surface.get_height(),
                    ),
                )
            self.screen.blit(
                text_surface, [align.center(), used_height + height_correction]
            )

    def make_top_left_subheader(self, text):
        """画面右上に文字を表示するメソッド"""
        text_surface = self.font_medium.render(text, True, Color.BLACK.rgb)
        align = Align(text_surface, self.width, self.height)
        self.screen.blit(text_surface, [align.left() + 10, align.top() + 10])

    def make_top_right_subheader(self, text):
        """画面左上に文字を表示するメソッド"""
        text_surface = self.font_medium.render(text, True, Color.BLACK.rgb)
        align = Align(text_surface, self.width, self.height)
        self.screen.blit(text_surface, [align.right() - 10, align.top() + 10])

    def make_bottom_subheader(self, text, color=Color.RED.rgb):
        """画面中央下に文字を表示するメソッド"""
        text_surface = self.font_medium.render(text, True, color)
        align = Align(text_surface, self.width, self.height)
        self.screen.blit(
            text_surface, [align.center(), align.bottom() - text_surface.get_height()]
        )

    def fill_bottom_subheader(self):
        """画面中央下を塗りつぶすメソッド"""
        self.screen.fill(
            Color.WAKATAKE.rgb,
            (0, self.height - 40 * 2, self.width, 45),
        )

    def text_box(self, text):
        """
        入力文字を表示するためのメソッド
        """
        text_surface = self.font_medium.render(text, True, Color.BLACK.rgb)
        self.screen.fill(
            Color.WAKATAKE.rgb,
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


class StateDraw(Drawer):
    """
    各画面を状態として捉えて処理を行うクラス
    インスタンス作成後、title→mode→...とメソッドを順次呼び出していく
    """

    def __init__(self) -> None:
        super().__init__()
        pygame.key.stop_text_input()  # input, editingを止める

    def title(self, focus_index) -> None:
        """タイトル画面"""
        # print("a")
        pygame.display.set_caption("タイピングゲーム | Title")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        title = "タイピングゲーム"
        self.make_header(title)
        self.make_header_outline()
        subheader_list = ["開始", "終了"]
        self.make_subheader(subheader_list, 0, focus_index)
        # Presents for: untbr(グループ1)
        pygame.display.update()  # 画面更新

    def register(self):
        """ユーザー名入力画面"""
        pygame.display.set_caption("タイピングゲーム | User")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        title = "ユーザー名入力"
        self.make_header(title)
        self.make_header_outline()
        pygame.display.update()  # 画面更新
        user_name = self.input_text()  # 文字入力
        pygame.event.post(pygame.event.Event(USEREVENT))
        return user_name

    def choose_type(self, focus_index) -> None:
        """ゲーム選択画面"""
        pygame.display.set_caption("タイピングゲーム | Type")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        title = "ゲーム選択"
        self.make_header(title)
        self.make_header_outline()
        subheader_list = ["ボキャブラリーゲーム", "しりとりゲーム"]
        self.make_subheader(subheader_list, 0, focus_index)
        pygame.display.update()  # 画面更新

    def choose_mode(self, game_modes_list, focus_index) -> None:
        """モード選択画面"""
        pygame.display.set_caption("タイピングゲーム | Mode")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        title = "モード選択"
        self.make_header(title)
        self.make_header_outline()
        self.make_subheader(game_modes_list, 0, focus_index)
        pygame.display.update()  # 画面更新

    def play(self, mode_info, progress) -> None:
        """
        ゲームプレイ画面
        しりとりの場合に出題する頭文字の取得に時間がかかるので、
        先に描画できるものは描画して、あとから出題する
        """
        pygame.display.set_caption("タイピングゲーム | Play")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_top_left_subheader(mode_info)
        self.make_top_right_subheader(progress)
        pygame.display.update()  # 画面更新
        question = yield
        used_height = self.make_header(question.word, -80)  # 取得した単語の表示
        description_list = textwrap.wrap(question.describe, 18)  # 18字ごとに区切る
        self.make_subheader(description_list, -used_height * 3)  # 取得した説明の表示
        self.make_header_underline()
        pygame.display.update()  # 画面更新
        judge = yield self.input_text()  # 入力を戻し、判定してもらう
        if not judge.correct:
            self.fill_bottom_subheader()  # 塗りつぶし
            pygame.display.update()  # 画面更新
            self.make_bottom_subheader(judge.message)
            pygame.display.update()  # 画面更新
            sleep(2)  # 不正解時のメッセージを見せるために2秒待機

    def input_text(self):
        """テキスト入力をするメソッド"""
        pygame.key.start_text_input()
        text = Text()  # Textクラスのインスタンス化
        input_text = "|"
        self.text_box(input_text)
        pygame.display.update()
        call_trigger = {
            K_BACKSPACE: text.delete,
            K_LEFT: text.move_cursor_left,
            K_RIGHT: text.move_cursor_right,
            K_RETURN : text.enter
        }
        while True:
            event = pygame.event.poll()
            if event.type == NOEVENT:
                continue
            if event.type == QUIT:
                pygame.quit()  # Pygame終了
                sys.exit(0)  # 処理終了
            # 半角入力中(もしくは全角入力の確定時)の矢印もしくはエンターキー押下時の処理
            elif event.type == KEYDOWN and not text.is_editing:
                if event.key in call_trigger.keys():
                    input_text = call_trigger[event.key]()
                if event.unicode in ("\r", "") and event.key == K_RETURN:
                    break
            elif event.type == TEXTEDITING:  # 全角入力するときに必ず真
                input_text = text.edit(event.text, event.start)
            elif event.type == TEXTINPUT:  # 半角入力するときに必ず使う(もしくは全角時enter)
                input_text = text.input(event.text)
            if event.type in [KEYDOWN, TEXTEDITING, TEXTINPUT]:
                self.text_box(input_text)
                pygame.display.update()
        pygame.key.stop_text_input()
        return input_text

    def result(self, user):
        """リザルト画面"""
        pygame.display.set_caption("タイピングゲーム | Result")  # キャプション設定
        result = user.split("\n")
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        title = "リザルト"
        self.make_header(title)
        self.make_header_outline()
        self.make_subheader(result)
        self.make_bottom_subheader("Please press Enter...", Color.BLUE.rgb)
        pygame.display.update()  # 画面更新
