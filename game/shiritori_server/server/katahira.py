class KataHira:
    """	
    カタカナからひらがなへ変換するためのクラス	
    """	

    # 小文字のひらがなのユニコード値リスト
    lower_hiragana_list = [
        0x3041,
        0x3043,
        0x3045,
        0x3047,
        0x3049,
        0x3063,
        0x3083,
        0x3085,
        0x3087,
        0x308E,
    ]
    # カタカナとひらがなのユニコード値の差分
    kata_hira_diff = 96

    def convert(self, katakana: str) -> str:
        """	
        カタカナの文字をひらがなに変換するメソッド	
        ただし、ひらがなにしたものが小文字であれば大文字(例: ぁ => あ)にする	
        """	
        # 差分を引いてひらがなにする
        hiragana = ord(katakana) - KataHira.kata_hira_diff
        # ひらがなが文字か判定してから返す
        return (
            chr(hiragana) if not self.is_lower_hiragana(hiragana) else chr(hiragana + 1)
        )

    def is_lower_hiragana(self, hiragana_ord: int) -> bool:
        """	
        引数のひらがなが小文字なのかを判定するメソッド	
        KataHira直下に定義したlower_hiragana_listを使って、	
        マッチすればTrue、しなければFalseを返す	
        """
        if hiragana_ord in KataHira.lower_hiragana_list:
            return True
        return False
