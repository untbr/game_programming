from enum import Enum
from typing import Generic, List, NamedTuple, TypeVar, Optional

"""
ゲーム本体から操作するモジュール
1, ゲーム立ち上げてユーザー名入力後、Userクラスをインスタンス化
2, ゲームの種類(レポートゲーム、しりとりゲーム)、モードの選択時にGameInfoクラスをインスタンス化
3, ゲームクリア時にUserクラスのadd_score()を呼ぶ
4, Userインスタンス.scores[-1]から最新のスコアを参照できる(Userインスタンス.scores[-1].clear_timeなど)
"""


class User:
    """
    プレイするユーザの情報に関するクラス
    Scoreを__scoresリストに持ち、ゲームクリア時にクリアの情報を追加する(add_score())
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

    def add_score(self, game_info: GameInfo, time: int, number_of_words: int) -> None:
        score = Score(game_info, time, number_of_words)
        self.__scores.append(score)
