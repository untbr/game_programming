import json
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


class ShiritoriClient:
    # host = "http://127.0.0.1:8000"
    host = "https://game-pbl-shiritori.df.r.appspot.com"

    def __init__(self) -> None:
        self.mode = 0
        self.host = ShiritoriClient.host + "/shiritori/"
        self.modes = None # self.request(self.host + "modes/")

    def request(self, url: str) -> Any:
        """
        urllibを使ってサーバにリクエストするメソッド
        辞書型にして返す
        """
        result = None
        try:
            with urlopen(url) as response:
                return json.load(response)
        except (HTTPError, URLError) as error:
            raise Exception("通信に失敗しました")

    def set_mode(self, mode: int) -> bool:
        """
        modeを引数に、しりとりで使う品詞の設定をするメソッド
        """
        if self.modes is not None and not str(mode) in self.modes.keys():
            return False
        self.mode = mode
        return True

    def get_head_word(self) -> Any:
        """
        最初の出題で使われるメソッド
        ランダムなひらがなの頭文字を取得する
        """
        return self.request(self.host + "head_word/")

    def shiritori(self, word: str, head_word: str) -> Any:
        """形態素解析のリクエストをするメソッド"""
        if head_word is None or len(head_word) != 1:
            raise Exception("一文字の頭文字が設定できていません")
        data = {"text": word, "head_word": head_word}
        url = self.host + str(self.mode) + "?" + urlencode(data)
        return self.request(url)
