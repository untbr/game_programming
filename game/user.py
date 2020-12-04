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

    def __str__(self):
        """最新のスコアを出力する"""
        if not self.scores:
            return ""
        return "ユーザー名: {}\n制限時間内に正解するべき問題数: {}\n正解数: {}\n不正解数: {}".format(
            self.__name,
            self.scores[-1].game_info.mode.number_of_words,
            self.scores[-1].number_of_corrects,
            self.scores[-1].number_of_incorrects,
        )

    def name(self) -> str:
        return self.__name

    @property
    def scores(self) -> List[Score]:
        return self.__scores

    def add_score(self, score: Score) -> None:
        self.__scores.append(score)
