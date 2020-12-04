import csv
import os
from abc import ABCMeta, abstractmethod
from enum import Enum
from random import randrange
from typing import Dict, List, NamedTuple, Type, Union

from .shiritori_client import ShiritoriClient
# from user import User


class Mode(NamedTuple):
    """ゲームの難易度(品詞)を格納する名前付きタプル"""

    id: int  # ユニークキー
    value: str  # 日本語での値
    number_of_words: int  # 制限時間内に解くべき語数(不正解はカウントしない実装をする)


class ReportType(Enum):
    """レポートゲームの難易度の列挙体"""

    EASY = Mode(0, "かんたん", 3)
    NORMAL = Mode(1, "ふつう", 5)
    DIFFICULT = Mode(2, "むずかしい", 10)


class ShiritoriType(Enum):
    """
    しりとりゲームの品詞の列挙体
    プレイできる品詞はAPIで取得できるようにしているが、
    こっち側のいい実装が思い浮かばないのでとりあえず決め打ち
    """

    NOUN = Mode(0, "名詞", 3)
    VERB = Mode(1, "動詞", 2)
    ADJECTIVE = Mode(2, "形容詞", 3)


class GameInfo:
    """
    ゲームの情報に関するクラス
    """

    def __init__(self, game_type: Union[Type[ReportType], Type[ShiritoriType]]) -> None:
        self.__type = game_type

    @property
    def type(self) -> Union[Type[ReportType], Type[ShiritoriType]]:
        return self.__type

    @property
    def mode(self) -> Mode:
        return self.__mode

    @mode.setter
    def mode(self, mode: Mode) -> None:
        self.__mode = mode


class JudgeResponse(NamedTuple):
    """
    正誤判定した際に使う名前付きタプル
    """

    correct: bool  # 正誤判定結果
    message: str  # # レポートゲームであれば正しい答え、しりとりならサーバ側からの判定メッセージ


class QuestionResponse(NamedTuple):
    """
    単語出題に使う名前付きタプル
    """

    word: str  # 穴あき単語もしくは頭文字
    describe: str  # 穴あき単語の説明もしくは品詞


class AGame(metaclass=ABCMeta):
    """
    ゲームロジックの抽象クラス
    レポートゲームとしりとりゲームに継承させる

    UI側で
    ReportもしくはShiritoriのインスタンス化し、set_modeで難易度(品詞)をセット
    その後、get_word()、judge_word(入力文字)、is_finish()をサイクルする
    is_finishがTrueの場合(もしくは制限時間が0になれば)リザルト画面に遷移させる
    """

    def __init__(self, game_type: Union[Type[ReportType], Type[ShiritoriType]]):
        # 継承先のインスタンスが生成されれば、ゲームのタイプが決まるので、
        # 先にGameInfoに対してゲームのタイプのみでインスタンス化
        self.game_info = GameInfo(game_type)
        self.number_of_corrects = 0

    @abstractmethod
    def set_mode(self, game_mode: Mode) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_word(self) -> QuestionResponse:
        """
        1単語返す
        """
        raise NotImplementedError()

    @abstractmethod
    def judge_word(self, word: str) -> JudgeResponse:
        """
        入力された単語wordが正しいか判定する
        """
        raise NotImplementedError()

    def get_mode(self) -> List[Mode]:
        """
        ゲームのタイプがセットされた状態のGameInfo(__init__でインスタンス化済み)を返す
        """
        return [i.value for i in self.game_info.type]

    def is_finish(self) -> bool:
        """
        self.number_of_correctが、そのモードの解くべき問題数に達するとTrueを返しそれ以外でFalseを返す
        """
        return self.game_info.mode.number_of_words == self.number_of_corrects


class Shiritori(AGame):
    def __init__(self) -> None:
        super().__init__(ShiritoriType)
        self.client = ShiritoriClient()
        self.head_word = ""  # 頭文字に使う変数

    def set_mode(self, game_mode: Mode) -> None:
        self.game_info.mode = game_mode
        self.client.set_mode(game_mode.id)

    def get_word(self) -> QuestionResponse:
        # ゲーム開始時は頭文字が設定されてないので、
        # クライアントを通して取得する
        if not self.head_word:
            self.head_word = self.client.get_head_word()["next_head"]
        # 上でhead_wordがNoneでないことが保証される
        description = "「{}」で始まる{}を入力してください".format(
            self.head_word, self.game_info.mode.value
        )
        # QuestionResponseを頭文字とdescriptionでタプルを生成して返す
        return QuestionResponse(self.head_word, description)

    def judge_word(self, word: str) -> JudgeResponse:
        """
        判定結果が真ならself.head_wordを設定する
        """
        if self.head_word is None:
            raise Exception("頭文字が設定されていません")
        result = self.client.shiritori(word, self.head_word)
        correct = result["is_correct"]  # 正誤の判定結果
        if correct:
            self.head_word = result["next_head"]  # 正解なら次の頭文字を更新する
            self.number_of_corrects += 1  # 正解数を更新する
        # 正しいときはmessageは空で、間違っているときはメッセージが含まれるように
        # サーバ側で処理している
        message = result["message"]
        # JudgeResponseを正誤判定とメッセージでタプルを生成して返す
        return JudgeResponse(correct, message)


class Report(AGame):
    def __init__(self) -> None:
        super().__init__(ReportType)
        self.words: List[Dict[str, str]] = []  # 出題する問題を格納するリスト
        self.file_path = os.path.dirname(__file__) + "/words.csv"

    def set_mode(self, game_mode: Mode) -> None:
        """
        モードをセットすれば解くべき問題数がわかるので、
        それを使ってファイルから問題数分の単語を拾ってself.wordsに格納する
        """
        self.game_info.mode = game_mode
        number_of_words = game_mode.number_of_words  # 解くべき語数
        self.add_words(number_of_words)  # self.wordsに単語追加するメソッドを呼ぶ

    def add_words(self, number_of_words: int) -> None:
        """
        set_mode時や、不正解時にself.wordsに単語を追加するメソッド
        """
        with open(self.file_path, mode="r", encoding="shift_jis") as f:
            reader = csv.reader(f)
            rows = [row for row in reader]  # 行をリストに格納していく
            len_rows = len(rows)
            for i in range(number_of_words):
                line_number = randrange(len_rows)  # 行数分のうちランダムに数値を取る
                word = rows[line_number]
                dict_word = {
                    "question": word[0],
                    "answer": word[1],
                    "description": word[2],
                }
                self.words.append(dict_word)

    def hole(self, word: List[str]) -> str:
        """
        単語を穴あきにするメソッド
        """
        hole_pos = randrange(len(word))  # 0~word長内でランダムな値を生成
        word[hole_pos] = "○"
        return "".join(word)

    def get_word(self) -> QuestionResponse:
        """
        self.wordsから単語を返す
        """
        word = self.words[-1]  # 最後の要素
        return QuestionResponse(self.hole(list(word["question"])), word["description"])

    def judge_word(self, word: str) -> JudgeResponse:
        """
        入力された単語の正誤を判定する
        正誤にかかわらず、出題されたself.wordsは削除される
        ただし、不正解であれば削除したのち、新たに1問分self.wordsに追加する
        (正解時のみself.wordsのlengthが減っていく)
        """
        q_word = self.words[-1]  # 最後の要素を出題していたので、判定元も最後の要素
        correct = False  # 正誤用の変数の初期値をFalseとしておく
        if q_word["answer"] == word:  # 正解
            correct = True
            self.number_of_corrects += 1  # 正解数(解いた数)を更新する
        self.words.pop()  # 削除
        message = ""
        if not correct:  # 間違っていたら
            self.add_words(1)  # 1単語追加する
            message = "正解は{}です".format(q_word["answer"])
        return JudgeResponse(correct, message)
