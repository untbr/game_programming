import webbrowser
from typing import List
from urllib.parse import urlencode

from .game import Score


class User:
    """
    プレイするユーザの情報に関するクラス
    Scoreクラスを__scoresリストに持ち、ゲームクリア時にクリアの情報を追加する(add_score())
    Userは一回だけインスタンス化され、
    ゲーム起動中は同じUserインスタンスにスコアを追加していく
    """

    def __init__(self):
        self.__name = ""
        self.__scores: List[Score] = []

    def __str__(self):
        """最新のスコアを出力する"""
        if not self.scores:
            return ""
        latest_score = self.scores[-1]
        return "ユーザー名: {}\n正解数: {}\n不正解数: {}\n評価: {}".format(
            self.__name,
            latest_score.number_of_corrects,
            latest_score.number_of_incorrects,
            latest_score.grade
        )

    @property
    def name(self) -> str:
        """ユーザー名を返すプロパティ"""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """ユーザー名のsetter"""
        self.__name = name

    @property
    def scores(self) -> List[Score]:
        """スコアを返すプロパティ"""
        return self.__scores

    def add_score(self, score: Score) -> None:
        """スコアを__scoresに追加するメソッド"""
        score.set_grade()  # 評価の算出
        self.__scores.append(score)

