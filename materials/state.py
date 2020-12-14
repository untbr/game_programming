"""
主要な状態における処理をまとめたモジュール
インスタンス作成後、順次メソッドを呼び出すことにより処理を行っていく
"""


import itertools
import sys
import typing
from enum import Enum
from typing import NamedTuple

import pygame
from pygame.locals import *  # 定数読み込み


class States(Enum):
    """状態の定義"""

    TITLE = 0  # タイトル画面
    USER = 1
    TYPE = 2  # ゲームモードタイプ選択画面
    MODE = 3  # ゲームモード選択画面
    PLAY = 4  # プレイ画面
    RESULT = 5  # 結果画面


class TupleState(NamedTuple):
    name: Enum
    number_of_choices: int  # 選択肢の数


class State:
    def __init__(self):
        self.is_running = False  # 状態遷移の有無によって画面の更新をするかどうかに使う
        self.exist_user = False # ユーザー名を既に登録しているか
        self.state = None # TupleStatesを格納する変数 
        self.states = [
            TupleState(States.TITLE, 2),
            TupleState(States.USER, 0),
            TupleState(States.TYPE, 2),
            TupleState(States.MODE, 3),
            TupleState(States.PLAY, 0),
            TupleState(States.RESULT, 0),
        ]
        self.iter_states = itertools.cycle(self.states)  # 無限ループのイテレータの生成
        self.transition()  # 状態遷移してself.stateをTITLEにする

    def transition(self):
        self.state = next(self.iter_states) # 次の状態に遷移する
        self.selector = FocusSelector(self.state.number_of_choices)
        self.is_running = False # 再描画の必要を知らせる

    def event(self):
        """キーダウンに応じた状態の遷移"""
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタン押下
                pygame.quit()  # Pygame終了(ウィンドウを閉じる)
                sys.exit(0)  # 処理終了
            elif event.type == USEREVENT:
                self.transition()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    # 終了を選択したとき
                    if self.state.name == States.TITLE and self.selector.position == 1:
                        pygame.event.post(pygame.event.Event(QUIT))
                        continue
                    self.transition()  # 次に遷移する
                    # ユーザー名が既に登録されているならユーザー入力画面を飛ばす
                    if self.state.name == States.USER and self.exist_user:
                        self.transition()
                # 選択画面の矢印キー操作
                elif self.state.name in [States.TITLE, States.TYPE, States.MODE]:
                    if event.key == K_DOWN:  # 下矢印キーが押されたら
                        self.selector.down()
                        self.is_running = False
                    elif event.key == K_UP:  # 上矢印が押されたら
                        self.selector.up()
                        self.is_running = False


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
