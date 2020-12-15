class Text:
    def __init__(self):
        self.text = ["|"]  # 入力されたテキストを格納していく変数
        self.editing = []  # 全角の文字編集中(変換前)の文字を格納するための変数
        self.is_editing = False  # 編集中文字列の有無(全角入力時に使用)
        self.cursor_pos = 0  # 文字入力のカーソル(パイプ|)の位置

    def __str__(self):
        """self.textリストを文字列にして返す"""
        return "".join(self.text)

    def edit(self, text, editing_cursor_pos):
        """
        edit(編集中)であるときに呼ばれるメソッド
        全角かつ漢字変換前の確定していないときに呼ばれる
        """
        if text: # テキストがあるなら
            self.is_editing = True
            for x in text:
                self.editing.append(x)  # 編集中の文字列をリストに格納していく
            self.editing.insert(editing_cursor_pos, "|") # カーソル位置にカーソルを追加
            disp = "[" + "".join(self.editing) + "]"
        else:
            self.is_editing = False  # テキストが空の時はFalse
            disp = "|"
        self.editing = []  # 次のeditで使うために空にする
        # self.cursorを読み飛ばして結合する
        return (
            format(self)[0 : self.cursor_pos] + disp + format(self)[self.cursor_pos+1 :]
        )

    def input(self, text):
        """
        半角文字が打たれたとき、もしくは全角で変換が確定したときに呼ばれるメソッド
        """
        self.is_editing = False # 編集中ではなくなったのでFalseにする
        for x in text:
            self.text.insert(self.cursor_pos, x) # カーソル位置にテキストを追加
            # 現在のカーソル位置にテキストを追加したので、カーソル位置を後ろにずらす
            self.cursor_pos += 1
        return format(self)

    def delete(self):
        """
        確定している文字(半角なら文字入力後、全角なら変換確定後)を削除するためのメソッド
        """
        if len(self.text) > 1: # 1より大きいとき(カーソルを消さない)
            self.text.pop(self.cursor_pos - 1) # カーソル位置の一個前を消す
            self.cursor_pos -= 1 # カーソル位置を前にずらす
        return format(self)

    def enter(self):
        """入力文字が確定したときに呼ばれるメソッド"""
        # カーソルを読み飛ばす
        entered = (
            format(self)[0 : self.cursor_pos] + format(self)[self.cursor_pos + 1 :]
        )
        self.text = ["|"]  # 次回の入力で使うためにself.textを空にする
        self.cursor_pos = 0 # self.text[0] == "|"となる
        return entered

    def move_cursor_left(self):
        """inputされた文字のカーソル(パイプ|)の位置を左に動かすメソッド"""
        if self.cursor_pos > 0:
            # カーソル位置をカーソル位置の前の文字と交換する
            self.text[self.cursor_pos], self.text[self.cursor_pos - 1] = (
                self.text[self.cursor_pos - 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos -= 1  # カーソルが1つ前に行ったのでデクリメント
        return format(self)

    def move_cursor_right(self):
        """inputされた文字のカーソル(パイプ|)の位置を右に動かすメソッド"""
        if len(self.text) - 1 > self.cursor_pos:
            # カーソル位置をカーソル位置の後ろの文字と交換する
            self.text[self.cursor_pos], self.text[self.cursor_pos + 1] = (
                self.text[self.cursor_pos + 1],
                self.text[self.cursor_pos],
            )
            self.cursor_pos += 1  # カーソルが1つ後ろに行ったのでインクリメント
        return format(self)
