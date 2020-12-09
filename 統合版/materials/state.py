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
from .text import Draw, Text  # テキスト入力に関するモジュール
from .drawer import Drawer

sys.path.append(os.pardir)
from game.game import Report, Shiritori  # ゲームの処理に関するモジュール
from game.user import User  # ユーザー情報に関するモジュール


class State(Drawer):
    """
    各画面を状態として捉えて処理を行うクラス
    インスタンス作成後、title→mode→...とメソッドを順次呼び出していく
    """

    def __init__(self, width: int, height: int) -> None:
        """
        コンストラクタ
        width: ウィンドウの横幅, height: ウィンドウの縦幅
        """
        super().__init__(width, height)
        self.user = User("test_user")  # ユーザー定義
        self.game = None  # ReportもしくはShiritoriのインスタンスを格納する変数
        self.game_mode = None
        self.is_running = True  # ゲームループの判定

    def title(self) -> None:
        """タイトル画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Title")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_header("タイピングゲーム(仮)")
        subheader_list = ['開始: " 1 "を入力してください', '終了: " 2 "を入力してください']
        self.make_subheader(subheader_list)
        pygame.display.update()  # 画面更新
        self.is_running = True
        while self.is_running:
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:  # 閉じるボタン押下
                    events.quit_game()  # 終了
                if event.type == KEYDOWN:
                    if event.key == K_1:  # 開始
                        self.is_running = False  # 次の画面へ
                    if event.key == K_2:  # 終了
                        events.quit_game()  # 終了

    def mode(self) -> None:
        """ゲーム選択画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Mode")  # キャプション設定
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        # 画面に表示するテキストの設定
        self.make_header("ゲーム選択")
        subheader_list = ['レポートゲーム(仮): "1" を入力してください', 'しりとりゲーム(仮): "2"を入力してください']
        self.make_subheader(subheader_list)
        pygame.display.update()  # 画面更新
        self.is_running = True
        while self.is_running:
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    events.quit_game()  # 閉じるボタン押下で終了
                if event.type == KEYDOWN:
                    if event.key == K_1:  # 「レポートゲーム(仮)」を選択
                        self.game = Report()
                        self.is_running = False
                    elif event.key == K_2:  # 「しりとりゲーム(仮)」を選択
                        self.game = Shiritori()
                        self.is_running = False
        self.game_mode = self.game.get_mode()  # 難易度(品詞)を取得

    def choose(self) -> None:
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

        self.is_running = True
        while self.is_running:
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    events.quit_game()  # 閉じるボタン押下で終了
                if event.type == KEYDOWN:
                    if event.key in [K_0, K_1, K_2]:
                       key_name = int(pygame.key.name(event.key)) 
                       self.game.set_mode(self.game_mode[key_name])  # 難易度/品詞の設定
                       self.is_running = False

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
            text_give = ""
            text = Text()  # Textクラスのインスタンス化
            drawer = Draw((self.width, self.height), self.screen)
            self.is_running = True
            while self.is_running:
                # イベント処理
                for event in pygame.event.get():
                    if event.type == QUIT:
                        events.quit_game()  # 閉じるボタン押下で終了
                    elif event.type == KEYDOWN:
                        if not text.is_editing:  # 編集中(全角の変換前)でないとき
                            if event.key == K_BACKSPACE:  # BS時
                                drawer.draw(text.delete())  # 確定した方から削除する
                            if event.key == K_LEFT:
                                drawer.draw(text.move_cursor_left())  # 文字のカーソルを左に動かす
                            if event.key == K_RIGHT:
                                drawer.draw(text.move_cursor_right())  # 文字のカーソルを右に動かす
                        if len(event.unicode) == 0:  # 確定時
                            if event.key == K_RETURN:
                                text_give = text.enter()  # 確定した文字の取得
                                drawer.draw("|")  # テキストボックスを空にする
                                self.is_running = False
                    elif event.type == TEXTEDITING:  # 全角入力するときに必ず真
                        drawer.draw(text.edit(event.text))
                    elif event.type == TEXTINPUT:  # 半角入力するときに必ず使う(もしくは全角時enter)
                        drawer.draw(text.input(event.text))
                pygame.display.update()
            judge = self.game.judge_word(text_give)  # 正誤判定
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

    def result(self):
        """リザルト画面"""
        pygame.display.set_caption("タイピングゲーム(仮) | Result")  # キャプション設定
        result = format(self.user).split("\n")
        self.screen.fill(Color.BLACK.rgb)  # ウィンドウを塗りつぶす
        self.make_header("リザルト")
        self.make_subheader(result)
        self.make_subheader(["Please press any key...".format(0)], 150)
        pygame.display.update()  # 画面更新
        self.is_running = True
        while self.is_running:
            # イベント処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    events.quit_game()  # 閉じるボタン押下で終了
                if event.type == KEYDOWN:
                    self.is_running = False  # キー入力検知で次の画面へ
