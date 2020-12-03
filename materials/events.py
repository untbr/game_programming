"""
Eventオブジェクトのtypeを受け取って何かしらの処理を行う関数群
試作中
"""


from enum import Enum
import sys
import pygame


def quit_game(event: int) -> None:
    """
    ウィンドウの終了ボタンが押下されたときにゲームの終了処理を行う関数
    Eventオブジェクトのtype属性を引数として渡す
    """
    if event == pygame.QUIT:  # 閉じるボタン押下
        pygame.quit()  # Pygame終了(ウィンドウを閉じる)
        sys.exit(0)  # 処理終了


def input_catch(event: int) -> str:
    """
    入力されたキーの値を表示する関数
    アルファベットと数字のみ
    引数にはkey属性を渡すこと
    """
    if (event >= 97)and(event <= 122):  # a-zが入力された場合
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # Shiftキーの検知
            return pygame.key.name(event).upper()  # 大文字
        else:
            return pygame.key.name(event)  # 小文字
    if (event >= 48)and(event <= 57):  # 0-9が入力された場合
        return pygame.key.name(event)


"""
# メモ

pygame.QUITとかpygame.K_aとかその辺の定数はint型らしい
だから引数のアノテーションはintでよさそう(てきとう)
"""