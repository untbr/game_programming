import sys
import textwrap
import pygame
from pygame.locals import *  # 定数読み込み
from materials.colors import Color  # 色に関するモジュール
from materials.align import Align  # オブジェクトの配置に関するモジュール
from materials import events  # イベント処理に関するモジュール
from materials.state import State  # 状態
from materials.game import Report, Shiritori
from materials.user import User


def main():
    """
    ゲームのサンプル
    """
    game = State(800, 600)  # インスタンス作成
    while(True):
        game.title()  # タイトル画面
        game.mode()  # ゲーム選択画面
        game.choose()  # モード選択
        game.play()  # ゲームプレイ画面
        game.result()  # リザルト画面


if __name__ == '__main__':
    main()
