import sys
import textwrap
import pygame
from pygame.locals import *  # 定数読み込み
from materials.colors import Color  # 色に関するモジュール
from materials.align import Align  # オブジェクトの配置に関するモジュール
from materials import events  # イベント処理に関するモジュール
from materials.state import Drawer, States  # 状態


def main():
    """
    ゲームのサンプル
    ゲームはキーボードを適当に操作することにより進行、2回目のタイトル画面表示後終了する
    """
    game = Drawer(800, 600)  # インスタンス作成
    while True:
        current_state = game.state
        game.transition()
        # 状態遷移がされてなければ(同じ状態であるなら)、ループの頭に戻る
        if game.state == current_state:
            continue
        # 状態遷移がされていれば、描画を更新する
        if game.state == States.TITLE:
            game.title()
        if game.state == States.CHOOSE:
            game.choose()
        if game.state == States.PLAY:
            game.play()
        if game.state == States.RESULT:
            game.result()
    return 0


if __name__ == "__main__":
    main()
