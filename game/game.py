import csv
import os
from abc import ABCMeta, abstractmethod
from enum import Enum
from random import randrange
from typing import Dict, List, NamedTuple, Type, Union

from .shiritori_client import ShiritoriClient


class Mode(NamedTuple):
    """ゲームの難易度(品詞)を格納する名前付きタプルの定義"""

    id: int  # モードのID
    value: str  # 日本語での値
    number_of_words: int  # 解くべき語数


class ReportType(Enum):
    """ボキャブラリーゲームの難易度の列挙体"""

    EASY = Mode(0, "かんたん", 3)
    NORMAL = Mode(1, "ふつう", 5)
    DIFFICULT = Mode(2, "むずかしい", 10)


class ShiritoriType(Enum):
    """しりとりゲームの品詞の列挙体"""

    NOUN = Mode(0, "名詞", 3)
    VERB = Mode(1, "動詞", 2)
    ADJECTIVE = Mode(2, "形容詞", 3)


class Score:
    """
    ゲームクリア時のスコアに関するクラス
    """

    def __init__(self, game_type: Union[Type[ReportType], Type[ShiritoriType]]):
       
        self.__game_type = game_type
        self.__mode = None
        self.__number_of_corrects = 0  # 正解した問題数
        self.__number_of_incorrects = 0  # 不正解だった問題数
        self.__grade = "-"  # 5段階評価の成績(S, A, B, C, D)

    @property
    def type(self) -> Union[Type[ReportType], Type[ShiritoriType]]:
        """ReportTypeもしくはShiritoriTypeを返すプロパティ"""
        return self.__game_type

    @property
    def mode(self) -> Mode:
        """Modeを返すプロパティ"""
        return self.__mode

    @mode.setter
    def mode(self, mode: Mode) -> None:
        """Modeのsetter"""
        self.__mode = mode

    @property
    def number_of_corrects(self) -> int:
        """正解数number_of_correctsを返すプロパティ"""
        return self.__number_of_corrects

    @number_of_corrects.setter
    def number_of_corrects(self, num) -> None:
        """正解数number_of_correctsのsetter"""
        self.__number_of_corrects = num

    @property
    def number_of_incorrects(self) -> int:
        """不正解数number_of_incorrectsを返すプロパティ"""
        return self.__number_of_incorrects

    @number_of_incorrects.setter
    def number_of_incorrects(self, num) -> None:
        """不正解数number_of_incorrectsのsetter"""
        self.__number_of_incorrects = num

    @property
    def grade(self) -> str:
        return self.__grade

    def set_grade(self) -> None:
        """
        成績は、
        不正解数 < 必要正解数 + nから算出される
        n=0  -> S
        n=3  -> A
        n=6  -> B
        n=9  -> C
        n=12 -> D
        実装は、
        不正解数 - 必要正回数 < n
        """
        # 不正解数とそのモードの解くべき問題数の差
        diff_between_incorrects_and_words = (
            self.number_of_incorrects - self.mode.number_of_words
        )
        # 差分と成績の辞書
        dict_n = {"S": 0, "A": 3, "B": 6, "C": 9, "D": 12}
        for k, v in dict_n.items():
            if diff_between_incorrects_and_words < v:
                self.__grade = k
                break


class JudgeResponse(NamedTuple):
    """
    正誤判定した際に使う名前付きタプルの定義
    """

    correct: bool  # 正誤判定結果
    message: str  # ボキャブラリーゲームであれば正しい答え、しりとりならサーバ側からの判定メッセージ


class QuestionResponse(NamedTuple):
    """
    問題の出題に使う名前付きタプル
    """

    word: str  # 穴あき単語もしくは頭文字
    describe: str  # 穴あき単語の説明もしくは品詞


class AGame(metaclass=ABCMeta):
    """
    ゲームロジックの抽象クラス
    ボキャブラリーゲームとしりとりゲームに継承させる

    利用側は
    ReportもしくはShiritoriのインスタンス化し、set_modeで難易度(品詞)をセット
    その後、get_word()、judge_word(入力文字)、is_finishをサイクルする
    is_finishがTrueの場合リザルト画面に遷移させる
    """

    def __init__(self, game_type: Union[Type[ReportType], Type[ShiritoriType]]):
        self.score = Score(game_type)  # Scoreクラスのインスタンス化

    @abstractmethod
    def set_mode(self, game_mode: Mode) -> None:
        """ゲームの難易度を設定する抽象メソッド"""
        raise NotImplementedError()

    @abstractmethod
    def get_word(self) -> QuestionResponse:
        """
        出題する問題を返す抽象メソッド
        """
        raise NotImplementedError()

    @abstractmethod
    def judge_word(self, word: str) -> JudgeResponse:
        """
        入力された単語wordが正しいか判定する抽象メソッド
        """
        raise NotImplementedError()

    def get_mode(self) -> List[Mode]:
        """
        セットされたゲームのタイプのModeを返すメソッド
        """
        return [i.value for i in self.score.type]

    @property
    def is_finish(self) -> bool:
        """
        self.number_of_correctが、そのモードの解くべき問題数に達するとTrueを返しそれ以外でFalseを返すメソッド
        """
        return self.score.mode.number_of_words == self.score.number_of_corrects

    @property
    def progress(self) -> str:
        return "{}/{}".format(
            self.score.number_of_corrects, self.score.mode.number_of_words
        )


class Shiritori(AGame):
    def __init__(self) -> None:
        super().__init__(ShiritoriType)
        self.client = ShiritoriClient()  # サーバとやりとりをするためのクラスインスタンス
        self.head_word = ""  # 頭文字に使う変数

    def __str__(self):
        return "しりとりゲーム: " + self.score.mode.value

    def set_mode(self, game_mode: Mode) -> None:
        """しりとりゲームの品詞を設定する具象メソッド"""
        self.score.mode = game_mode
        self.client.set_mode(game_mode.id)

    def get_word(self) -> QuestionResponse:
        """出題する問題を返す具象メソッド"""
        # ゲーム開始時は頭文字が設定されてないので、
        # クライアントを通して取得する
        if not self.head_word:
            head = self.client.get_head_word()
            self.head_word = head["next_head"]
        # 上でhead_wordがNoneでないことが保証される
        description = "「{}」で始まる{}を入力してください".format(
            self.head_word, self.score.mode.value
        )
        # QuestionResponseを頭文字とdescriptionでタプルを生成して返す
        return QuestionResponse(self.head_word, description)

    def judge_word(self, word: str) -> JudgeResponse:
        """
        入力された単語wordが正しいか判定する具象メソッド
        判定結果が真ならself.head_wordを設定する
        """
        if self.head_word is None:
            raise Exception("頭文字が設定されていません")
        result = self.client.shiritori(word, self.head_word)
        correct = result["is_correct"]  # 正誤の判定結果
        # 言葉の尻が「ん」であったとき
        if result["next_head"] == "ん":
            correct = False
            result["message"] = "最後が「ん」になっています"
        # しりとりが成立しているとき
        if correct:
            self.head_word = result["next_head"]  # 正解なら次の頭文字を更新する
            self.score.number_of_corrects += 1  # 正解数を更新する
        # しりとりが成立していないとき
        else:
            self.score.number_of_incorrects += 1  # 不正解数を更新する
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

    def __str__(self):
        return "ボキャブラリーゲームゲーム: " + self.score.mode.value

    def set_mode(self, game_mode: Mode) -> None:
        """
        ボキャブラリーゲームの難易度を設定する具象メソッド
        モードをセットすれば解くべき問題数がわかるので、
        それを使ってファイルから問題数分の単語を拾ってself.wordsに格納する
        """
        self.score.mode = game_mode
        self.add_words(game_mode.number_of_words)  # self.wordsに単語追加するメソッドを呼ぶ

    def add_words(self, number_of_words: int) -> None:
        """
        set_mode時や、不正解時にself.wordsに単語を追加するメソッド
        """
        with open(self.file_path, mode="r", encoding="shift_jis") as f:
            reader = csv.reader(f)
            rows = [row for row in reader]  # 行をリストに格納していく
            len_rows = len(rows)  # csvの行数
            for i in range(number_of_words):  # 出題する問題数分だけループ
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
        """出題する問題を返す具象メソッド"""
        word = self.words[-1]  # 最後の要素
        return QuestionResponse(self.hole(list(word["question"])), word["description"])

    def judge_word(self, word: str) -> JudgeResponse:
        """
        入力された単語wordが正しいか判定する具象メソッド
        正誤にかかわらず、出題されたself.wordsは削除される
        ただし、不正解であれば削除したのち、新たに1問分self.wordsに追加する
        (正解時のみself.wordsのlengthが減っていく)
        """
        q_word = self.words[-1]  # 最後の要素を出題していたので、判定元も最後の要素
        correct = False  # 正誤用の変数の初期値をFalseとしておく
        self.words.pop()  # 削除
        message = ""
        if q_word["answer"] == word:  # 正解のとき
            correct = True
            self.score.number_of_corrects += 1  # 正解数を更新する
        else:  # 不正解の時
            self.score.number_of_incorrects += 1  # 不正解数を更新する
            self.add_words(1)  # 1単語追加する
            message = "正解は{}です".format(q_word["answer"])
        return JudgeResponse(correct, message)
