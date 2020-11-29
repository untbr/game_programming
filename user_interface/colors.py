"""
ウェブカラーをRGBで表現した定数
データ型はタプル型(Red, Green, Blue)
"""
WHITE = (255, 255, 255)  # color code: ffffff
SILVER = (192, 192, 192)  # color code: c0c0c0
GRAY = (128, 128, 128)  # color code: 808080
BLACK = (0, 0, 0)  # color code: 000000
RED = (255, 0, 0)  # color code: ff0000
MAROON = (128, 0, 0)  # color code: 800000
YELLOW = (255, 255, 0)  # color code: ffff00
OLIVE = (128, 128, 0)  # color code: 808000
LIME = (0, 255, 0)  # color code: 00ff00
GREEN = (0, 128, 0)  # color code: 008000
AQUA = (0, 255, 255)  # color code: 00ffff
TEAL = (0, 128, 128)  # color code: 008080
BLUE = (0, 0, 255)  # color code: 0000ff
NAVY = (0, 0, 128)  # color code: 000080
FUCHSIA = (255, 0, 255)  # color code: ff00ff
PURPLE = (128, 0, 128)  # color code: 800080


def comp_color(color: tuple) -> tuple:
    """
    補色を求める関数
    引数(元の色)と返り値(補色)はタプル型(Red, Green, Blue)
    """
    value = max(color) + min(color)  # RGB値の最大, 最小の和
    tmp = list(color)  # 計算をするのでリスト型にする
    for i, clr_value in enumerate(color):
        tmp[i] = value - clr_value  # valueからそれぞれのRGB値を引くことにより補色が求まる
    return tuple(tmp)  # タプル型にして返す