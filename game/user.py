from typing import List

from .game import Score


class User:
    """
    プレイするユーザの情報に関するクラス
    Scoreクラスを__scoresリストに持ち、ゲームクリア時にクリアの情報を追加する(add_score())
    Userは一回だけインスタンス化され、
    ゲーム起動中は同じUserインスタンスにスコアを追加していく
    """

    def __init__(self, name: str):
        self.__name = name
        self.__scores: List[Score] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def scores(self) -> List[Score]:
        return self.__scores

    def add_score(self, score: Score) -> None:
        self.__scores.append(score)
