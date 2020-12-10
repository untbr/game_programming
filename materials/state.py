"""
主要な状態における処理をまとめたモジュール
インスタンス作成後、順次メソッドを呼び出すことにより処理を行っていく
"""


import os
import sys
import textwrap
import typing
from time import sleep

import pygame
from pygame.locals import *  # 定数読み込み

from . import events  # イベント処理に関するモジュール
from .colors import Color  # 色に関するモジュール
from .drawer import Drawer
from .text import Text  # テキスト入力に関するモジュール

sys.path.append(os.pardir)
from game.game import Report, Shiritori  # ゲームの処理に関するモジュール
from game.user import User  # ユーザー情報に関するモジュール
from enum import Enum

from game import game


class States(Enum):
    """状態の定義"""

    TITLE = 0  # タイトル画面
    TYPE = 1  # ゲームモードタイプ選択画面
    MODE = 2  # ゲームモード選択画面
    PLAY = 3  # プレイ画面
    RESULT = 4  # 結果画面


class State:
    def __init__(self):
        self.state = States.TITLE
        self.is_running = False
        self.game_types = ["dummy", "Report", "Shiritori"]
        self.game_instance = None
        self.game_modes = None
        self.mode = None
        self.is_finish = False

    def transition(self):
        """キーダウンに応じた状態の遷移"""
        current_state = self.state
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタン押下
                events.quit_game()  # 終了
            if self.state == States.TITLE:  # タイトル画面
                if event.type == KEYDOWN:
                    if event.key == K_1:  # 開始
                        self.state = States.TYPE  # 次の画面へ
                    if event.key == K_2:  # 終了
                        events.quit_game()  # 終了
            elif self.state == States.TYPE:  # ゲームタイプ選択
                if event.type == KEYDOWN:
                    if event.key in [K_1, K_2]:  # 開始
                        cls = getattr(
                            game, self.game_types[int(pygame.key.name(event.key))]
                        )
                        self.game_instance = cls()
                        self.game_modes = self.game_instance.get_mode()
                        self.state = States.MODE
            elif self.state == States.MODE:
                if event.type == KEYDOWN:
                    if event.key in [K_0, K_1, K_2]:
                        key_name = int(pygame.key.name(event.key))
                        self.mode = self.game_modes[key_name]
                        self.state = States.PLAY
            elif self.state == States.PLAY and self.is_finish:
                self.state = States.RESULT
            elif self.state == States.RESULT:
                if event.type == KEYDOWN:
                    self.is_finish = False
                    self.state = States.TITLE  # キー入力検知で次の画面へ
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # エスケープが押されたら
                    self.is_finish = False
                    self.state = States.TITLE
        if current_state != self.state:
            self.is_running = False


class Draw(Drawer):
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
        self.user = User("test_user")  # ユーザー定義
        self.game = None  # ReportもしくはShiritoriのインスタンスを格納する変数
        self.game_mode = None
        self.is_running = True  # ゲームループの判定
        pygame.key.stop_text_input()

    def title(self) -> None:
        """タイトル画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Title")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_header("タイピングゲーム(仮)")
        subheader_list = ['開始: " 1 "を入力してください', '終了: " 2 "を入力してください']
        self.make_subheader(subheader_list)
        pygame.display.update()  # 画面更新

    def choose_type(self) -> None:
        """ゲーム選択画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Mode")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_header("ゲーム選択")
        subheader_list = ['レポートゲーム(仮): "1" を入力してください', 'しりとりゲーム(仮): "2"を入力してください']
        self.make_subheader(subheader_list)
        pygame.display.update()  # 画面更新

    def choose_mode(self) -> None:
        """モード選択画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Choose")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_header("モード選択")
        mode_list = [
            '{0}: " {1} "を入力してください'.format(i.value, i.id) for i in self.game_mode
        ]
        self.make_subheader(mode_list)
        pygame.display.update()  # 画面更新

    def play(self) -> None:
        """ゲームプレイ画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Play")  # キャプション設定
        while not self.game.is_finish():
            self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
            # 画面に表示するテキストの設定
            self.make_top_left_subheader("時間内に入力せよ")
            self.make_top_right_subheader("00:00")
            question = self.game.get_word()  # 出題をしてもらう

            used_height = self.make_header(question.word, -80)  # 取得した単語の表示
            description_list = textwrap.wrap(question.describe, 18)  # 18字ごとに区切る
            self.make_subheader(description_list, -used_height * 3)  # 取得した説明の表示

            pygame.display.update()  # 画面更新
            # 文字入力に必要な変数
            judge = self.game.judge_word(self.input_text())  # 正誤判定
            if not judge.correct:  # 不正解時
                # 上書き(塗りつぶし) rect値(x, y, width, height)
                self.screen.fill(
                    Color.BLACK.rgb,
                    (0.0, float(self.height - 30 * 2), float(self.width), float(30)),
                )
                pygame.display.update()  # 画面更新
                self.make_bottom_subheader(judge.message)
                pygame.display.update()  # 画面更新
                sleep(2)  # 不正解時のメッセージを見せるために2秒待機
        self.user.add_score(self.game.score)  # ユーザーの情報にスコアを追加

    def input_text(self):
        text = Text()  # Textクラスのインスタンス化
        while True:
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    events.quit_game()  # 閉じるボタン押下で終了
                elif event.type == KEYDOWN:
                    if not text.is_editing:  # 編集中(全角の変換前)でないとき
                        if event.key == K_BACKSPACE:  # BS時
                            self.text_box(text.delete())  # 確定した方から削除する
                        if event.key == K_LEFT:
                            self.text_box(text.move_cursor_left())  # 文字のカーソルを左に動かす
                        if event.key == K_RIGHT:
                            self.text_box(text.move_cursor_right())  # 文字のカーソルを右に動かす
                    if len(event.unicode) == 0:  # 確定時
                        if event.key == K_RETURN:
                            self.text_box("|")  # テキストボックスを空にする
                            return text.enter()  # 確定した文字の取得
                elif event.type == TEXTEDITING:  # 全角入力するときに必ず真
                    self.text_box(text.edit(event.text))
                elif event.type == TEXTINPUT:  # 半角入力するときに必ず使う(もしくは全角時enter)
                    self.text_box(text.input(event.text))
            pygame.display.update()

    def result(self):
        """リザルト画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Result")  # キャプション設定
        result = format(self.user).split("\n")
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        self.make_header("リザルト")
        self.make_subheader(result)
        self.make_subheader(["Please press any key...".format(0)], 150)
        pygame.display.update()  # 画面更新
