from enum import Enum
from random import randrange
from typing import NamedTuple, Tuple

import MeCab
from katahira import KataHira
from pydantic import BaseModel


class WordClass(NamedTuple):
    class_id: int
    class_name: str


class Mode(Enum):
    NOUN = WordClass(0, "名詞")
    VERB = WordClass(1, "動詞")
    ADJECTIVE = WordClass(2, "形容詞")


class Response(BaseModel):
    word: str
    word_class: str
    is_correct: bool
    message: str
    next_head: str


class Shiritori:
    def __init__(self) -> None:
        self.katahira = KataHira()
        self.m = MeCab.Tagger()

    def make_initial_word(self) -> Response:
        """	
        ゲーム開始時に出題する頭文字を生成するメソッド	
        カタカナ、アスキーコードのァからロまでの間の値から一つ選び、	
        それをひらがなに直す(小文字を避けるため)	
        """
        return Response(
            word="",
            word_class = "",
            is_correct=False,
            message="",
            next_head=self.katahira.convert((chr(randrange(12449, 12526)))),
        )

    def is_correct_word(self, mode: str, text: str, head_word: str) -> Response:
        """	       
        入力された文字が単語であること、	        
        品詞がmodeと同じであることなどを判定するメソッド
        """
        node = self.m.parseToNode(text).next
        word = node.surface
        features = node.feature.split(",")
        word_class = features[0]
        response = Response(word=word, word_class=word_class, is_correct=False, message="", next_head=head_word)
        if len(features) < 7:
            response.message = "日本語以外が含まれている可能性があります。"
            return response

        word_reading_candicate = features[6]
        if len(word_reading_candicate) < 2:
            response.message = "一字以上のよみを入力してください。"
            return response

        if word_reading_candicate[-1] == "ー":
            word_reading_candicate = word_reading_candicate[:-1]
        # 一単語か判定
        judge_one_word = self.judge_one_word(node)
        # 品詞判定
        judge_word_class = self.judge_correct_word_class(mode, word_class)
        # 頭文字が期待さされている文字か判定
        judge_correct_head = self.judge_correct_head(head_word, word_reading_candicate)
        # 総合的に入力された文字textでよいか判定
        is_correct = (
            judge_word_class[0] and judge_correct_head[0] and judge_one_word[0]
        )
        message = judge_one_word[1] + judge_word_class[1] + judge_correct_head[1]
        # is_correctがTrueであれば言葉の尻を取る	
        # Falseであれば、同じhead_wordでやり直してもらう
        next_head = self.katahira.convert(word_reading_candicate[-1]) if is_correct else head_word
        response.is_correct = is_correct
        response.message = message
        response.next_head = next_head
        return response

    def judge_one_word(self, node: MeCab.Node) -> Tuple[bool, str]:
        """	
        文章ではなく単語1つのみであることの判定メソッド	
        """
        node = node.next # BOS/EOSであることが期待される
        # さらにその次はNoneであることが期待される
        if node.next: # Noneでない(パiースの結果がまだ存在する)とき
            return (False, "文章もしくは複数の単語が含まれています。")
        return (True, "")

    def judge_correct_word_class(self, mode: str, word_class:str) -> Tuple[bool, str]:
        """
        入力された単語がmodeで指定された品詞と一致しているかの判定メソッド	
        """
        if mode == word_class: # 単語が指定した品詞であるとき
            return (True, "")
        return (False, "{}が含まれていません。{}と判定されました。".format(mode, word_class))

    def judge_correct_head(self, correct_head: str, word: str) -> Tuple[bool, str]:
        """
        入力された単語が、指定された言葉から始まっているかの判定メソッド
        """
        hiragana_word = self.katahira.convert(word[0])
        if hiragana_word == correct_head:
            return (True, "")
        return (
            False,
            "頭文字は「{}」と判定されました。"\
            "「{}」から始まる単語ではないようです。".format(hiragana_word, correct_head),
        )
