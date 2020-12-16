from enum import Enum


class Color(Enum):
    """
    色をRGBで表現した列挙型
    RGB値はタプル型(Red, Green, Blue)
    名前はname, 値はvalueで取得可能
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
    WAKATAKE = (112, 225, 112)

    @property
    def rgb(self) -> tuple:
        """Color(列挙型)のメンバー値を返すメソッド"""
        return self.value

    @property
    def comp(self) -> tuple:
        """
        補色を求めるメソッド
        引数(元の色)と返り値(補色)はタプル型(Red, Green, Blue)
        """
        value = max(self.value) + min(self.value)  # RGB値の最大, 最小の和
        tmp = list(self.value)  # 計算をするのでリスト型にする
        for i, clr_value in enumerate(self.value):
            tmp[i] = value - clr_value  # valueからそれぞれのRGB値を引くことにより補色が求まる
        return tuple(tmp)  # タプル型にして返す
