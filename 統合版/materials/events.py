"""主にイベント処理で利用する関数をまとめたモジュール"""


import sys
from typing import Union
import pygame
from pygame.locals import *  # 定数読み込み


def quit_game() -> None:
    """ゲームの終了処理を行う関数"""
    pygame.quit()  # Pygame終了(ウィンドウを閉じる)
    sys.exit(0)  # 処理終了


def input_key(key: int) -> Union[str, None]:
    """
    入力されたキーに対応する文字を返す関数
    扱えないキーが入力された場合はNoneを返す
    引数keyにはkey属性を渡すこと
    扱える文字は以下の通り
    アルファベット(大/小), 数字, スペース' ', カンマ',', マイナス(ハイフン)'-', ピリオド'.', スラッシュ'/'
    """
    if (key >= K_a) and (key <= K_z):  # a-zが入力された場合
        if pygame.key.get_mods() & KMOD_SHIFT:  # Shiftキーの検知
            return pygame.key.name(key).upper()  # 大文字
        else:
            return pygame.key.name(key)  # 小文字
    elif (key >= K_0) and (key <= K_9):  # 0-9が入力された場合
        if pygame.key.get_mods() & KMOD_SHIFT:  # Shiftキーの検知
            return None
        else:
            return pygame.key.name(key)
    elif (key >= K_COMMA) and (key <= K_SLASH):  # ,-./が入力された場合
        if pygame.key.get_mods() & KMOD_SHIFT:  # Shiftキーの検知
            return None
        else:
            return pygame.key.name(key)
    elif key == K_SPACE:  # スペースが入力された場合
        return " "
    else:  # 上記以外の入力
        return None
