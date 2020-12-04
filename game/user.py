from enum import Enum
from typing import Generic, List, NamedTuple, TypeVar, Optional

"""
ゲーム本体から操作するモジュール
1, ゲーム立ち上げてユーザー名入力後、Userクラスをインスタンス化
2, ゲームの種類(レポートゲーム、しりとりゲーム)、モードの選択時にGameInfoクラスをインスタンス化
3, ゲームクリア時にUserクラスのadd_score()を呼ぶ
4, Userインスタンス.scores[-1]から最新のスコアを参照できる(Userインスタンス.scores[-1].clear_timeなど)
"""


class Score:
    """
    ゲームクリア時のスコアに関するクラス
    """

    def __init__(self, game_info: GameInfo, time: int, number_of_words: int):
        self.__game_info = game_info
        self.__clear_time = time
        self.__number_of_words = number_of_words

    @property
    def game_info(self) -> GameInfo:
        return self.__game_info

    @property
    def clear_time(self) -> int:
        return self.__clear_time

    @property
    def number_of_words(self) -> int:
        return self.__number_of_words


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
