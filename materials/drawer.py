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

    def make_header_outline(self, text):
        text_surface = self.font_large.render(text, True, Color.BLUE.rgb)
        align = Align(text_surface, self.width, self.height)
        top_start_pos = (100, 100)
        top_end_pos = (700, 100)
        bottom_start_pos = (100, 220)
        bottom_end_pos = (700, 220)
        pygame.draw.line(self.screen, Color.BLUE.rgb, top_start_pos, top_end_pos)
        pygame.draw.line(self.screen, Color.BLUE.rgb, bottom_start_pos, bottom_end_pos)

    def make_header_underline(self, text):
        text_surface = self.font_large.render(text, True, Color.BLACK.rgb)
        align = Align(text_surface, self.width, self.height)
        start_pos = (100, 110)
        end_pos = (700, 110)
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
                    (255, 255, 0),
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
            Color.WAKATAKE.rgb,
            (0.0, float(self.height - 30 * 2), float(self.width), float(30)),
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


class FocusSelector:
    """
    選択をする際に、小見出しのフォーカスする位置を決めるためのクラス
    """

    def __init__(self, length_of_list):
        self.length_of_list = length_of_list - 1
        self.focus_pos = 0

    def down(self):
        # リスト長よりself.focus_posが大きくならないようにする
        if self.focus_pos < self.length_of_list:
            self.focus_pos += 1
        return self.focus_pos

    def up(self):
        # self.focus_posが0より小さくならないようにする
        if self.focus_pos > 0:
            self.focus_pos -= 1
        return self.focus_pos

    @property
    def position(self):
        return self.focus_pos


class StateDraw(Drawer):
    """
    各画面を状態として捉えて処理を行うクラス
    インスタンス作成後、title→mode→...とメソッドを順次呼び出していく
    """

    def __init__(self) -> None:
        """
        コンストラクタ
        width: ウィンドウの横幅, height: ウィンドウの縦幅
        """
        super().__init__()
        pygame.key.stop_text_input()  # input, editingを止める

    def title(self, focus_index=0) -> None:
        """タイトル画面"""
        # print("a")
        pygame.display.set_caption("タイピングゲーム(仮) | Title")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        title = "タイピングゲーム(仮)"
        self.make_header(title)
        self.make_header_outline(title)
        subheader_list = ["開始", "終了"]
        self.make_subheader(subheader_list, 0, focus_index)
        pygame.display.update()  # 画面更新

    def register(self):
        pygame.display.set_caption("タイピングゲーム(仮) | User")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        title = "ユーザー名入力"
        self.make_header(title)
        self.make_header_outline(title)
        pygame.display.update()  # 画面更新
        user_name = self.input_text()  # 文字入力
        # 状態遷移を確実にするためにイベント処理に通知する
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, is_registered=True))
        return user_name

    def choose_type(self, focus_index=0) -> None:
        """ゲーム選択画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Type")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        title = "ゲーム選択"
        self.make_header(title)
        self.make_header_outline(title)
        subheader_list = ["レポートゲーム(仮)", "しりとりゲーム(仮)"]
        self.make_subheader(subheader_list, 0, focus_index)
        pygame.display.update()  # 画面更新

    def choose_mode(self, game_modes, focus_index=0) -> None:
        """モード選択画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Mode")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        title = "モード選択"
        self.make_header(title)
        self.make_header_outline(title)
        mode_list = [str(i.value) for i in game_modes]
        self.make_subheader(mode_list, 0, focus_index)
        pygame.display.update()  # 画面更新

    def play(self, game) -> None:
        """ゲームプレイ画面"""
        if game.is_finish():
            # 状態遷移を確実にするためにイベント処理に通知する
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, is_finish=True))
            return
        pygame.display.set_caption("タイピングゲーム(仮) | Play")  # キャプション設定
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_top_left_subheader("時間内に入力せよ")
        self.make_top_right_subheader("00:00")
        pygame.display.update()  # 画面更新
        question = game.get_word()
        used_height = self.make_header(question.word, -80)  # 取得した単語の表示
        description_list = textwrap.wrap(question.describe, 18)  # 18字ごとに区切る
        self.make_subheader(description_list, -used_height * 3)  # 取得した説明の表示
        self.make_header_underline(question.word)
        pygame.display.update()  # 画面更新
        input_text = self.input_text()  # 文字入力
        judge = game.judge_word(input_text)  # 判定
        if not judge.correct:
            self.fill_bottom_subheader()  # 塗りつぶし
            pygame.display.update()  # 画面更新
            self.make_bottom_subheader(judge.message)
            pygame.display.update()  # 画面更新
            sleep(2)  # 不正解時のメッセージを見せるために2秒待機
        self.play(game)

    def input_text(self):
        pygame.key.start_text_input()
        text = Text()  # Textクラスのインスタンス化
        input_text = "|"
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()  # Pygame終了
                    sys.exit(0)  # 処理終了
                elif event.type == KEYDOWN:
                    if not text.is_editing:  # 編集中(全角の変換前)でないとき
                        if event.key == K_BACKSPACE:  # BS時
                            input_text = text.delete()  # 確定した方から削除する
                        if event.key == K_LEFT:
                            input_text = text.move_cursor_left()  # 文字のカーソルを左に動かす
                        if event.key == K_RIGHT:
                            input_text = text.move_cursor_right()  # 文字のカーソルを右に動かす
                    if len(event.unicode) == 0:  # 確定時
                        if event.key == K_RETURN:
                            self.text_box("")
                            pygame.key.stop_text_input()
                            return text.enter()  # 確定した文字の取得
                elif event.type == TEXTEDITING:  # 全角入力するときに必ず真
                    input_text = text.edit(event.text, event.start)
                elif event.type == TEXTINPUT:  # 半角入力するときに必ず使う(もしくは全角時enter)
                    input_text = text.input(event.text)
                self.text_box(input_text)
                pygame.display.update()

    def result(self, user):
        """リザルト画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Result")  # キャプション設定
        result = format(user).split("\n")
        self.screen.fill(Color.WAKATAKE.rgb)  # ウィンドウを塗りつぶす
        title = "リザルト"
        self.make_header(title)
        self.make_header_outline(title)
        self.make_subheader(result)
        self.make_subheader(["Please press Enter..."], 150)
        pygame.display.update()  # 画面更新
