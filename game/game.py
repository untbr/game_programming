from abc import ABCMeta, abstractmethod
from enum import Enum
from random import randrange
from typing import NamedTuple
import csv

from shiritori_client import ShiritoriClient
from user import GameInfo, GameType, ReportMode, ShiritoriMode, User


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
    ReportもしくはShiritoriのインスタンス化し、set_modeも難易度(品詞)をセット
    その後、get_word()、judge_word(入力文字)、is_finish()をサイクルする
    is_finishがTrueの場合(もしくは制限時間が0になれば)リザルト画面に遷移させる
    """

    def __init__(self, game_type):
        # 継承先のインスタンスが生成されれば、ゲームのタイプが決まるので、
        # 先にGameInfoに対してゲームのタイプのみでインスタンス化
        self.game_info = GameInfo(game_type, None)
        self.number_of_corrects = 0

    @abstractmethod
    def set_mode(self, game_mode: Enum):
        raise NotImplementedError()

    @abstractmethod
    def get_word(self) -> QuestionResponse:
        """
        1単語返す
        """
        raise NotImplementedError()

    @abstractmethod
    def judge_word(self, word: str):
        """
        入力された単語wordが正しいか判定する
        """
        raise NotImplementedError()

    def get_mode(self):
        """
        ゲームのタイプがセットされた状態のGameInfo(__init__でインスタンス化済み)を返す
        """
        # UI側で、get_mode().type.value.game_modeでそのタイプのモードがわかる
        return self.game_info

    def is_finish(self) -> bool:
        """
        self.number_of_correctが、そのモードの解くべき問題数に達するとTrueを返しそれ以外でFalseを返す
        """
        return self.game_info.mode.value.number_of_words == self.number_of_corrects


class Shiritori(AGame):
    def __init__(self) -> None:
        super().__init__(GameType.SHIRITORI)
        self.client = ShiritoriClient()
        self.head_word = None  # 頭文字に使う変数

    def set_mode(self, game_mode: Enum) -> None:
        self.game_info.mode = game_mode
        self.client.set_mode(game_mode.value.id)

    def get_word(self) -> QuestionResponse:
        # ゲーム開始時は頭文字が設定されてないので、
        # クライアントを通して取得する
        if self.head_word is None:
            self.head_word = self.client.get_head_word()["next_head"]
        # 上でhead_wordがNoneでないことが保証される
        description = "「{}」で始まる{}を入力してください".format(
            self.head_word, self.game_info.mode.value.value
        )
        # QuestionResponseを頭文字とdescriptionでタプルを生成して返す
        return QuestionResponse(self.head_word, description)

    def judge_word(self, word: str) -> JudgeResponse:
        """
        判定結果が真ならself.head_wordを設定する
        """
        # mode_id = self.game_info.mode.value.id
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
        super().__init__(GameType.REPORT)
        self.words = []  # LIFO

    def set_mode(self, game_mode: Enum) -> None:
        """
        モードをセットすれば解くべき問題数がわかるので、
        それを使ってファイルから問題数分の単語を拾ってself.wordsに格納する
        """
        self.game_info.mode = game_mode
        number_of_words = game_mode.value.number_of_words  # 解くべき語数
        self.add_words(number_of_words)  # self.wordsに単語追加するメソッドを呼ぶ

    def add_words(self, number_of_words):
        """
        set_mode時や、不正解時にself.wordsに単語を追加するメソッド
        """

        with open("./words.csv", mode="r", encoding="shift_jis") as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
            len_rows = len(rows)
 
            for i in range(number_of_words):
                line_number = randrange(len_rows) # 行数分のうちランダムに数値を取る
                word = rows[line_number]
                dict_word = {
                    "question": word[0],
                    "answer": word[1],
                    "description": word[2].strip(","),
                }
                self.words.append(dict_word)

    def hole(self, word: list) -> str:
        """
        単語を穴あきにするメソッド
        """
        hole_pos = randrange(len(word))
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
        q_word = self.words[-1]
        correct = False
        if q_word["answer"] == word:  # 正解
            correct = True
            self.number_of_corrects += 1  # 正解数(解いた数)を更新する
        self.words.pop()  # 削除
        message = ""
        if not correct:  # 間違っていたら
            self.add_words(1)  # 1単語追加する
            message = "正解は{}です".format(q_word["answer"])
        return JudgeResponse(correct, message)
