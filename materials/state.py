"""
主要な状態における処理をまとめたモジュール
インスタンス作成後、順次メソッドを呼び出すことにより処理を行っていく
"""


import sys
import typing
from enum import Enum

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


class State:
    def __init__(self):
        self.state = States.TITLE  # 立ち上げ時はタイトル画面を表示する
        self.is_running = False  # 状態遷移の有無によって画面の更新をするかどうかに使う
        self.exist_user = False  # ユーザー名が既に登録されているか
        self.game_type_key = None
        self.game_mode_key = None
        self.selector = None

    def transition(self):
        """キーダウンに応じた状態の遷移"""
        current_state = self.state
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタン押下
                pygame.quit()  # Pygame終了(ウィンドウを閉じる)
                sys.exit(0)  # 処理終了
            if self.state == States.TITLE and event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if self.selector.position == 1:
                        pygame.event.post(pygame.event.Event(QUIT))
                        continue
                    self.state = States.TYPE if self.exist_user else States.USER
            elif self.state == States.USER and event.type == USEREVENT:
                if event.is_registered:
                    self.exist_user = True
                    self.state = States.TYPE
            elif self.state == States.TYPE and event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.game_type_key = self.selector.position
                    self.state = States.MODE  # モード選択へ遷移
            elif self.state == States.MODE and event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.game_mode_key = self.selector.position
                    self.state = States.PLAY  # ゲームプレイへ遷移
            elif self.state == States.PLAY and event.type == USEREVENT:
                # ゲームプレイ画面で、問題が解き終わったら
                if event.is_finish:
                    self.state = States.RESULT  # リザルトへ遷移
            elif self.state == States.RESULT and event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.state = States.TITLE  # キー入力検知で次の画面へ
            if (
                self.state in [States.TITLE, States.TYPE, States.MODE]
                and event.type == KEYDOWN
            ):
                if event.key == K_DOWN:  # 下矢印キーが押されたら
                    self.selector.down()
                    self.is_running = False
                elif event.key == K_UP:  # 上矢印が押されたら
                    self.selector.up()
                    self.is_running = False
        if current_state != self.state:  # 上記で状態遷移されたら
            self.is_running = False
            self.selector = None
