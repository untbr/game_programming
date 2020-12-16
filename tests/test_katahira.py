import os
import sys

sys.path.append(os.pardir)

from game.shiritori_server.katahira import KataHira


class TestKataHira:
    lower_hiragana = "ぁぃぅぇぉっゃゅょゎ"

    katakana = (
        "ァアィイゥウェエォオ"
        "カガキギクグケゲコゴ"
        "サザシジスズセゼソゾ"
        "タダチヂッツヅテデトド"
        "ナニヌネノ"
        "ハバパヒビピフブプヘベペホボポ"
        "マミムメモ"
        "ャヤュユョヨ"
        "ラリルレロ"
        "ヮワヰヱヲン"
    )
    # 小文字は大文字に変換済みの表
    hiragana = (
        "ああいいううええおお"
        "かがきぎくぐけげこご"
        "さざしじすずせぜそぞ"
        "ただちぢつつづてでとど"
        "なにぬねの"
        "はばぱひびぴふぶぷへべぺほぼぽ"
        "まみむめも"
        "ややゆゆよよ"
        "らりるれろ"
        "わわゐゑをん"
    )

    def test_lower_hiragana_list(self):
        """
        lower_hiragana_listのテスト
        """

        for i, word in enumerate(KataHira.lower_hiragana_list):
            assert word ==  ord(TestKataHira.lower_hiragana[i])

    def test_convert(self):
        """
        convertのテスト
        """

        conv = KataHira()
        conv_result = ""
        for x in TestKataHira.katakana:
            conv_result += conv.convert(x)
        assert conv_result == TestKataHira.hiragana

    def test_is_lower_hiragana(self):
        """
        is_lower_hiraganaのテスト
        """

        conv = KataHira()
        # TestKataHira.hiraganaはすべて大文字なのでFalseが期待される
        for x in TestKataHira.hiragana:
            is_lower_hiragana = conv.is_lower_hiragana(ord(x))
            assert is_lower_hiragana == False
        # TestKataHira.lower_hiraganaはすべて小文字なのでTrueが期待される
        for x in TestKataHira.lower_hiragana:
            is_lower_hiragana = conv.is_lower_hiragana(ord(x))
            assert is_lower_hiragana == True
