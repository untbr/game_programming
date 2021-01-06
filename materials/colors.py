from enum import Enum


class Color(Enum):
    """
    色をRGBで表現した列挙型
    RGB値はタプル型(Red, Green, Blue)
    名前はname, 値はvalueで取得可能
    """

    BLACK = (0, 0, 0)  # color code: 000000
    RED = (255, 0, 0)  # color code: ff0000
    TEAL = (0, 128, 128)  # color code: 008080
    BLUE = (0, 0, 255)  # color code: 0000ff
    WAKATAKE = (112, 225, 112) # color code: 70e170

    @property
    def rgb(self) -> tuple:
        """Color(列挙型)のメンバー値を返すメソッド"""
        return self.value

    @property
    def comp(self) -> tuple:
        """補色を求めるメソッド"""
        value = max(self.value) + min(self.value)  # RGB値の最大, 最小の和
        tmp = list(self.value)  # 計算をするのでリスト型にする
        for i, clr_value in enumerate(self.value):
            tmp[i] = value - clr_value  # valueからそれぞれのRGB値を引くことにより補色が求まる
        return tuple(tmp)  # タプル型にして返す
