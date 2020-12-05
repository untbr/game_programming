import sys
import textwrap
import pygame
from pygame.locals import *  # 定数読み込み
from materials.colors import Color  # 色に関するモジュール
from materials.align import Align  # オブジェクトの配置に関するモジュール
from materials import events  # イベント処理に関するモジュール
from materials.state import State  # 状態


def main():
    """
    ゲームのサンプル
    ゲームはキーボードを適当に操作することにより進行、2回目のタイトル画面表示後終了する
    """
    game = State(800, 600)  # インスタンス作成
    game.title()  # タイトル画面
    game.choose()  # 難易度選択
    game.play()  # ゲームプレイ画面
    game.result()  # リザルト画面
    game.title()  # タイトル画面
    return 0


if __name__ == '__main__':
    main()
