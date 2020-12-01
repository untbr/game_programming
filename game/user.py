from enum import Enum
from typing import Generic, List, TypeVar, NamedTuple

"""
ゲーム本体から操作するモジュール
1, ゲーム立ち上げてユーザー名入力後、Userクラスをインスタンス化
2, ゲームの種類(レポートゲーム、しりとりゲーム)、モードの選択時にGameInfoクラスをインスタンス化
3, ゲームクリア時にUserクラスのadd_score()を呼ぶ
4, Userインスタンス.scores[-1]から最新のスコアを参照できる(Userインスタンス.scores[-1].clear_timeなど)
"""

class ModeTuple(NamedTuple):
    id: int # ユニークキー
    value: str # 日本語での値
    number_of_words: int # 制限時間内に解くべき語数(不正解はカウントしない実装をする)

class ReportMode(Enum):
    EASY = ModeTuple(0, "かんたん", 3)
    NORMAL = ModeTuple(1, "ふつう", 5)
    DIFFICULT = ModeTuple(2, "むずかしい", 10)


class ShiritoriMode(Enum):
    """
    プレイできる品詞はAPIで取得できるようにしているが、
    こっち側のいい実装が思い浮かばないのでとりあえず決め打ち
    """
    NOUN = ModeTuple(0, "名詞", 3)
    VERB = ModeTuple(1, "動詞", 2)
    ADJECTIVE = ModeTuple(2, "形容詞", 3)


class TypeMode(NamedTuple):
    T = TypeVar("T", ReportMode, ShiritoriMode)
    game_type: int
    game_mode: T


class GameType(Enum):
    REPORT = TypeMode(0, ReportMode)  # レポートゲーム
    SHIRITORI = TypeMode(1, ShiritoriMode)  # しりとりゲーム


class GameInfo:
    """
    ゲームの情報に関するクラス
    モードに関する定義は
    レポートでは難易度(ReportMode)、しりとりでは品詞の種類(ShiritoriMode)なので変数とした
    """

    T = TypeVar("T", ReportMode, ShiritoriMode)

    def __init__(self, game_type: GameType, mode: Generic[T]) -> None:
        self.__type = game_type
        self.__mode = mode

    @property
    def type(self) -> GameType:
        return self.__type

    @property
    def mode(self) -> Generic[T]:
        return self.__mode

    @mode.setter
    def mode(self, mode) -> None:
        self.__mode = mode

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
