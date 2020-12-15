import os
import sys
import unittest

import pygame
from pygame.locals import *

sys.path.append(os.pardir)

from materials.state import SelectorFocus, State


class TestSelectorFocus(unittest.TestCase):
    """SelectorFocusの単体テストをするクラス"""

    def test_down(self):
        number_of_choices = 3  # 選択肢の数
        selector = SelectorFocus(number_of_choices)
        self.assertEqual(selector.position, 0)  # 初めは0番目にフォーカスする
        self.assertEqual(selector.down(), 1)
        self.assertEqual(selector.down(), 2)
        self.assertEqual(selector.down(), 2)  # 2で飽和

    def test_up(self):
        number_of_choices = 3  # 選択肢の数
        selector = SelectorFocus(number_of_choices)
        self.assertEqual(selector.up(), 0)  # 0番目より上の選択肢ないから0
        # 最後の選択肢にフォーカスする
        for i in range(number_of_choices - 1):
            selector.down()
        self.assertEqual(selector.position, 2)
        self.assertEqual(selector.up(), 1)
        self.assertEqual(selector.up(), 0)
        self.assertEqual(selector.up(), 0)  # 0で飽和


class TestState(unittest.TestCase):
    """Stateの単体テストをするクラス"""

    def test_transition(self):
        """状態遷移のメソッドのテスト"""
        state = State()
        # インスタンス化後の状態はstate.statesの0番目
        self.assertEqual(state.state, state.states[0])
        for x in state.states[1:]:
            state.transition()  # 状態遷移
            self.assertEqual(state.state, x)  # 状態遷移後
            self.assertEqual(state.is_running, False)  # 状態遷移後は必ずFalse

    def test_event(self):
        """
        イベント処理における状態遷移のテスト

        0, タイトル
        1, ユーザー名登録(最初の一回だけ)
        2, ゲームタイプ選択
        3, ゲームモード選択
        4, ゲームプレイ
        5, リザルト
        という遷移がサイクルすることのテスト
        """
        pygame.init()
        state = State()  # この時点での状態はTITLE
        self.assertEqual(state.selector.position, 0)  # フォーカスは一番上(「開始」)
        pygame.event.clear()  # 溜まっているイベントを削除する

        # 新たにエンターキーを押下し、ユーザー名の登録に遷移させたい
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RETURN))
        state.event()  # イベント処理
        self.assertEqual(state.state, state.states[1])  # USERに遷移
        state.has_user_name = True  # ユーザー名の登録をしたこととする

        # 新たにエンターキーを押下し、ゲームタイプ選択画面に遷移させたい
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RETURN))
        state.event()  # イベント処理
        self.assertEqual(state.state, state.states[2])  # TYPEに遷移

        # 新たにエンターキーを押下し、ゲームモード選択画面に遷移させたい
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RETURN))
        state.event()  # イベント処理
        self.assertEqual(state.state, state.states[3])  # MODEに遷移

        # 新たにエンターキーを押下し、ゲームプレイ画面に遷移させたい
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RETURN))
        state.event()  # イベント処理
        self.assertEqual(state.state, state.states[4])  # PLAYに遷移

        # 新たにエンターキーを押下し、リザルト画面に遷移させたい
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RETURN))
        state.event()  # イベント処理
        self.assertEqual(state.state, state.states[5])  # RESULTに遷移

        # 新たにエンターキーを押下し、タイトル画面に遷移させたい
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RETURN))
        state.event()  # イベント処理
        self.assertEqual(state.state, state.states[0])  # TITLEに遷移

        # 新たにエンターキーを押下し、ゲームタイプ選択画面に遷移させたい
        # ユーザー名の登録は済んでいるので飛ばされる
        pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RETURN))
        state.event()  # イベント処理
        self.assertEqual(state.state, state.states[2])  # TYPEに遷移


if __name__ == "__main__":
    unittest.main()
