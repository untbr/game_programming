"""
主要な状態における処理をまとめたモジュール
インスタンス作成後、順次メソッドを呼び出すことにより処理を行っていく
"""


import os
import sys
import typing
from enum import Enum

import pygame
from pygame.locals import *  # 定数読み込み

from . import events  # イベント処理に関するモジュール

sys.path.append(os.pardir)

from game import game


class States(Enum):
    """状態の定義"""

    TITLE = 0  # タイトル画面
    USER = 1
    TYPE = 2  # ゲームモードタイプ選択画面
    MODE = 3  # ゲームモード選択画面
    PLAY = 4  # プレイ画面
    RESULT = 5  # 結果画面


class State:
    def __init__(self):
        self.state = States.TITLE  # 立ち上げ時はタイトル画面を表示する
        self.is_running = False  # 状態遷移の有無によって画面の更新をするかどうかに使う
        self.exist_user = False  # ユーザー名が既に登録されているか
        self.game_type_key = None
        self.game_mode_key = None

    def transition(self):
        """キーダウンに応じた状態の遷移"""
        current_state = self.state
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタン押下
                pygame.quit()  # Pygame終了(ウィンドウを閉じる)
                sys.exit(0)  # 処理終了
            if self.state == States.TITLE:  # タイトル画面
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        if self.exist_user:
                            self.state = States.TYPE  # ゲームタイプ選択へ遷移
                        else:
                            self.state = States.USER  # ユーザー名登録へ遷移
                    if event.key == K_2:  # 終了
                        events.quit_game()  # 終了
            elif self.state == States.USER and event.type == pygame.USEREVENT:
                self.exist_user = True
                self.state = States.TYPE
            elif self.state == States.TYPE:  # ゲームタイプ選択
                if event.type == KEYDOWN:
                    if event.key in [K_1, K_2]:  # レポート or しりとり
                        self.game_type_key = int(pygame.key.name(event.key))
                        self.state = States.MODE  # モード選択へ遷移
            elif self.state == States.MODE:  # モード選択
                if event.type == KEYDOWN:
                    if event.key in [K_0, K_1, K_2]:
                        self.game_mode_key = int(pygame.key.name(event.key))
                        self.state = States.PLAY  # ゲームプレイへ遷移
            elif self.state == States.PLAY and event.type == pygame.USEREVENT:
                # ゲームプレイ画面で、問題が解き終わったら
                if event.is_finish:
                    self.state = States.RESULT  # リザルトへ遷移
            elif self.state == States.RESULT:
                if event.type == KEYDOWN:
                    self.state = States.TITLE  # キー入力検知で次の画面へ
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # エスケープが押されたら
                    self.state = States.TITLE
        if current_state != self.state:
            self.is_running = False
