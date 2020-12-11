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

    def title(self) -> None:
        """タイトル画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Title")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_header("タイピングゲーム(仮)")
        subheader_list = ['開始: " 1 "を入力してください', '終了: " 2 "を入力してください']
        self.make_subheader(subheader_list)
        pygame.display.update()  # 画面更新

    def register(self):
        pygame.display.set_caption("タイピングゲーム(仮) | User")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        self.make_subheader(["ユーザー名を入力してください"])
        pygame.display.update()  # 画面更新
        return self.input_text()  # 文字入力

    def choose_type(self) -> None:
        """ゲーム選択画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Type")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_header("ゲーム選択")
        subheader_list = ['レポートゲーム(仮): "1" を入力してください', 'しりとりゲーム(仮): "2"を入力してください']
        self.make_subheader(subheader_list)
        pygame.display.update()  # 画面更新

    def choose_mode(self, game_modes) -> None:
        """モード選択画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Mode")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_header("モード選択")
        mode_list = ['{0}: " {1} "を入力してください'.format(i.value, i.id) for i in game_modes]
        self.make_subheader(mode_list)
        pygame.display.update()  # 画面更新

    def play(self, game) -> None:
        """ゲームプレイ画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Play")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_top_left_subheader("時間内に入力せよ")
        self.make_top_right_subheader("00:00")
        pygame.display.update()  # 画面更新
        question = game.get_word()
        used_height = self.make_header(question.word, -80)  # 取得した単語の表示
        description_list = textwrap.wrap(question.describe, 18)  # 18字ごとに区切る
        self.make_subheader(description_list, -used_height * 3)  # 取得した説明の表示
        pygame.display.update()  # 画面更新
        return self.input_text()  # 文字入力

    def correct_answer(self, judge):
        """回答した後、間違っていた際に正解を表示するメソッド"""
        self.fill_bottom_subheader()  # 塗りつぶし
        pygame.display.update()  # 画面更新
        self.make_bottom_subheader(judge.message)
        pygame.display.update()  # 画面更新
        sleep(2)  # 不正解時のメッセージを見せるために2秒待機

    def input_text(self):
        pygame.key.start_text_input()
        text = Text()  # Textクラスのインスタンス化
        input_text = ""
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
                            self.text_box("|")  # テキストボックスを空にする
                            # イベントキューにイベントを送って、入力が確定したことを知らせる
                            event = pygame.event.Event(pygame.USEREVENT)
                            pygame.event.post(event)
                            pygame.key.stop_text_input()
                            return text.enter()  # 確定した文字の取得
                elif event.type == TEXTEDITING:  # 全角入力するときに必ず真
                    input_text = text.edit(event.text)
                elif event.type == TEXTINPUT:  # 半角入力するときに必ず使う(もしくは全角時enter)
                    input_text = text.input(event.text)
                self.text_box(input_text)
                pygame.display.update()

    def result(self, user):
        """リザルト画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Result")  # キャプション設定
        result = format(user).split("\n")
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        self.make_header("リザルト")
        self.make_subheader(result)
        self.make_subheader(["Please press any key...".format(0)], 150)
        pygame.display.update()  # 画面更新
